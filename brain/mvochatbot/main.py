from mvochatbot.init import *
from mvochatbot.data import *
from mvochatbot.tokens import *
from mvochatbot.train import *
from mvochatbot.model import *
from mvochatbot.evaluate import *
import numpy as np
import random
import time
import datetime
import math
import importlib
import sys

def as_minutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

def time_since(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (as_minutes(s), as_minutes(rs))

def create_model(config_file, USE_CUDA):
    # Initialize configs
    attn_model, hidden_size, n_layers, dropout, optimizer_name, criterion_name, learning_rate, decoder_learning_ratio = init_config_model(config_file)

    # read_datas
    load_training, encoderpath, decoderpath = init_config_load(config_file)
    MIN_LENGTH, MAX_LENGTH, TRIM_MIN_COUNT, DELAY, USE_QACORPUS, CREATE_QAPAIRS, corpuspaths, qapairspath = init_config_data(config_file)
    if (USE_QACORPUS and not(CREATE_QAPAIRS)):
        input_lang, output_lang, pairs = read_qapairs('context', 'answer', qapairspath)
    else:
        input_lang, output_lang, pairs = prepare_data('context', 'answer', corpuspaths, MIN_LENGTH, MAX_LENGTH, DELAY)
    
    # trim pairs
    input_lang.trim(TRIM_MIN_COUNT)
    output_lang.trim(TRIM_MIN_COUNT)
    pairs = trimpairs(input_lang, output_lang, pairs)
    
    # USE GPU ?
    if (USE_CUDA):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device("cpu")
    #torch.cuda.set_device(1)

    # Initialize models
    encoder = EncoderRNN(input_lang.n_words, hidden_size, n_layers, dropout=dropout).to(device)
    decoder = LuongAttnDecoderRNN(attn_model, hidden_size, output_lang.n_words, n_layers, dropout=dropout).to(device)

    # Initialize optimizers and criterion
    if optimizer_name == 'Adam':
        encoder_optimizer = optim.Adam(encoder.parameters(), lr=learning_rate)
        decoder_optimizer = optim.Adam(decoder.parameters(), lr=learning_rate * decoder_learning_ratio)
    elif optimizer_name == 'SGD':
        encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
        decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate * decoder_learning_ratio)
    
    if criterion_name == 'NLLLoss':
        criterion = nn.NLLLoss()
    elif criterion_name == 'CrossEntropyLoss':
        criterion = nn.CrossEntropyLoss()

    # Move models to GPU if necessary
    if device == 'cuda':
        encoder.cuda()
        decoder.cuda()
    
    if load_training:
        load(USE_CUDA, encoderpath, encoder, encoder_optimizer)
        load(USE_CUDA, decoderpath, decoder, decoder_optimizer)
        
    return (input_lang, output_lang, pairs, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion, USE_QACORPUS, MAX_LENGTH)

if __name__ == "__main__":
    # parse arguments
    config_file = 'config.ini'
    args = sys.argv[1:]
    if (len(args) > 1):
        print('Usage : python', sys.argv[0], '[config_file.ini]')
        quit()
    if (len(args) == 1):
        if args[0].endswith('.ini'):
            config_file = args[0]
        else:
            print('Usage : python', sys.argv[0], '[config_file.ini]')
            quit()
    
    # Get Settings | Parameters 
    mode, USE_CUDA = init_config_getSettings(config_file)
    input_lang, output_lang, pairs, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion, USE_QACORPUS, MAX_LENGTH = create_model(config_file, USE_CUDA)
    MAX_LENGTH_EVAL, temp_module_name, temp_function_name, n_words_vocab = init_config_eval(config_file)
    batch_size, clip, teacher_forcing_ratio, iteration, n_iterations, save_every, print_every, evaluate_every, encoderpath, decoderpath = init_config_training(config_file)
        
    if mode == 'eval':
        try:
            temperature_module = importlib.import_module(temp_module_name)
            temperature_fun = getattr(temperature_module, temp_function_name)
        except ImportError as err:
            print('Error:', err)
            quit()
        test_chatbot(encoder, decoder, input_lang, output_lang, USE_CUDA, MAX_LENGTH_EVAL, temperature_fun, USE_QACORPUS, n_words_vocab)
             
    elif mode == 'train':
        # Keep track of time elapsed and running averages
        start = time.time()
        print_loss_total = 0 # Reset every print_every

        # Begin!
        ecs = []
        dcs = []
        eca = 0
        dca = 0

        while iteration < n_iterations:
            iteration += 1

            # Get training data for this cycle
            input_batches, input_lengths, target_batches, target_lengths = random_batch(input_lang, output_lang, batch_size, pairs)

            # Run the train function
            loss, ec, dc = train(
                input_batches, input_lengths, target_batches, target_lengths, batch_size,
                encoder, decoder,
                encoder_optimizer, decoder_optimizer, criterion, clip, MAX_LENGTH
            )

            # Keep track of loss
            print_loss_total += loss
            eca += ec
            dca += dc

            if iteration % print_every == 0:
                print_loss_avg = print_loss_total / print_every
                print_loss_total = 0
                print_summary = '%s (%d %d%%) %.4f' % (time_since(start, iteration / n_iterations), iteration, iteration / n_iterations * 100, print_loss_avg)
                print(print_summary)

            if iteration % evaluate_every == 0:
                evaluate_randomly(encoder, decoder, pairs, input_lang, output_lang, USE_CUDA, MAX_LENGTH_EVAL, temperature_fun)
            
            if iteration % save_every == 0:
                save(encoderpath+str(iteration), encoder, encoder_optimizer)
                save(decoderpath+str(iteration), decoder, decoder_optimizer)
                
        save(encoderpath+'end', encoder, encoder_optimizer)
        save(decoderpath+'end', decoder, decoder_optimizer)
