import random
from mvochatbot.tokens import *
from mvochatbot.model import *
from mvochatbot.train import indexes_from_sentence
from mvochatbot.data import normalize_string, normalize_input, postProcess
import torch
import torch.nn as nn
from torch.autograd import Variable
from torch import optim
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_packed_sequence, pack_padded_sequence#, masked_cross_entropy
from mvochatbot.masked_cross_entropy import *
import numpy as np
import readline

def alan_answer(input_string, encoder, decoder, input_lang, output_lang, USE_CUDA, max_length, temperature_fun, USE_QACORPUS=False, n_words=100):
    input_string = normalize_input(input_string, USE_QACORPUS)
    output_words, attentions, confidence = evaluate(encoder, decoder, input_string, input_lang, output_lang, USE_CUDA, max_length, temperature_fun, n_words)
    output_sentence = ' '.join(output_words)
    output_sentence = postProcess(output_sentence, USE_QACORPUS)
    return output_sentence, confidence

def test_chatbot(encoder, decoder, input_lang, output_lang, USE_CUDA, max_length, temperature_fun, USE_QACORPUS=False, n_words=100):
    print("Alan est prêt à vous recevoir.")
    while 1:
        print()
        context = str(input('')).strip()
        context = normalize_input(context, USE_QACORPUS)
        if context == 'quit':
            break
        output_words, attentions, confidence = evaluate(encoder, decoder, context, input_lang, output_lang, USE_CUDA, max_length, temperature_fun, n_words)
        output_sentence = ' '.join(output_words)
        output_sentence = postProcess(output_sentence, USE_QACORPUS)
        print('< ', output_sentence)
        print('Je me sens confiant à : ', confidence, '%')
        output_words, attentions = evaluateBest(encoder, decoder, context, input_lang, output_lang, USE_CUDA, max_length)
        output_sentence = ' '.join(output_words)
        output_sentence = postProcess(output_sentence, USE_QACORPUS)
        print('BEST : ', output_sentence)
    
def indexHigh(lname, x):
    for i in range(len(lname)):
        if x <= lname[i]:
            return i

def evaluate(encoder, decoder, input_seq, input_lang, output_lang, USE_CUDA, max_length, temperature_fun, n_words=100):

    with torch.no_grad():
        confidence = 1.0
        input_seqs = [indexes_from_sentence(input_lang, input_seq)]
        input_lengths = [len(input_seqs[0])]
        input_batches = Variable(torch.LongTensor(input_seqs)).transpose(0, 1)

        if USE_CUDA:
            input_batches = input_batches.cuda()

        # Set to not-training mode to disable dropout
        encoder.train(False)
        decoder.train(False)

        # Run through encoder
        encoder_outputs, encoder_hidden = encoder(input_batches, input_lengths, None)

        # Create starting vectors for decoder
        decoder_input = Variable(torch.LongTensor([SOS_token])) # SOS
        decoder_hidden = encoder_hidden[:decoder.n_layers] # Use last (forward) hidden state from encoder

        if USE_CUDA:
            decoder_input = decoder_input.cuda()

        # Store output words and attention states
        decoded_words = []
        decoder_attentions = torch.zeros(max_length + 1, max_length + 1)

        # Run through decoder
        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs, USE_CUDA
            )
            decoder_attentions[di,:decoder_attention.size(2)] += decoder_attention.squeeze(0).squeeze(0).cpu().data

            # Choose top word from output
            #print(max_length)
            topv, topi = decoder_output.data.topk(n_words)
            ni = topi[0][0]
            if ni == EOS_token and di != 0:
                break
            sum_nv = [0 for i in range(n_words)]
            current_ni = [0 for i in range(n_words)]
            current_nv = [0 for i in range(n_words)]
            for i in range(n_words):
                current_ni[i] = topi[0][i]
                current_nv[i] = np.exp((topv[0][i]).item() / temperature_fun(di, max_length))
                if i == 0:
                    sum_nv[i] = current_nv[i]
                else:
                    for j in range(1, i + 1):
                        sum_nv[i] = sum_nv[i - 1] + current_nv[j]
            allsum = sum(current_nv)
            normalized_sum = [sum_nv[i]/allsum for i in range(len(sum_nv))]
            sum_ns = [normalized_sum[i].item() for i in range(len(normalized_sum))]
            rndnum = random.uniform(0, 1)
            ih = indexHigh(sum_ns, rndnum)
            ni = topi[0][ih]
            confidence *= (current_nv[ih]/allsum)

            #print(output_lang.index2word[ni.item()])
            if di == 0:
                while ni == EOS_token:
                    rndnum = random.uniform(0, 1)
                    ni = topi[0][indexHigh(sum_ns, rndnum)]
            elif ni == EOS_token:
                break
            decoded_words.append(output_lang.index2word[ni.item()])

            # Next input is chosen word
            decoder_input = Variable(torch.LongTensor([ni]))
            if USE_CUDA:
                decoder_input = decoder_input.cuda()

        # Set back to training mode
        encoder.train(True)
        decoder.train(True)
    return decoded_words, decoder_attentions[:di+1, :len(encoder_outputs)], confidence

def evaluateBest(encoder, decoder, input_seq, input_lang, output_lang, USE_CUDA, max_length):

    with torch.no_grad():
        input_seqs = [indexes_from_sentence(input_lang, input_seq)]
        input_lengths = [len(input_seqs[0])]
        input_batches = Variable(torch.LongTensor(input_seqs)).transpose(0, 1)

        if USE_CUDA:
            input_batches = input_batches.cuda()

        # Set to not-training mode to disable dropout
        encoder.train(False)
        decoder.train(False)

        # Run through encoder
        encoder_outputs, encoder_hidden = encoder(input_batches, input_lengths, None)

        # Create starting vectors for decoder
        decoder_input = Variable(torch.LongTensor([SOS_token])) # SOS
        decoder_hidden = encoder_hidden[:decoder.n_layers] # Use last (forward) hidden state from encoder

        if USE_CUDA:
            decoder_input = decoder_input.cuda()

        # Store output words and attention states
        decoded_words = []
        decoder_attentions = torch.zeros(max_length + 1, max_length + 1)

        # Run through decoder
        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs, USE_CUDA
            )
            decoder_attentions[di,:decoder_attention.size(2)] += decoder_attention.squeeze(0).squeeze(0).cpu().data

            # Choose top word from output
            topv, topi = decoder_output.data.topk(1)
            ni = topi[0][0]
            if ni == EOS_token:
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(output_lang.index2word[ni.item()])

            # Next input is chosen word
            decoder_input = Variable(torch.LongTensor([ni]))
            if USE_CUDA: decoder_input = decoder_input.cuda()
                
        # Set back to training mode
        encoder.train(True)
        decoder.train(True)

    return decoded_words, decoder_attentions[:di+1, :len(encoder_outputs)]

def myeval(encoder, decoder, input_sentence, input_lang, output_lang, USE_CUDA, max_length, temperature_fun, target_sentence=None):
    output_words, attentions = evaluateBest(encoder, decoder, input_sentence, input_lang, output_lang, USE_CUDA, max_length)
    output_sentence = ' '.join(output_words)
    print('>', input_sentence)
    if target_sentence is not None:
        print('=', target_sentence)
    print('<', output_sentence[:-1])

def evaluate_randomly(encoder, decoder, pairs, input_lang, output_lang, USE_CUDA, max_length, temperature_fun):
    for i in range(10):
        [input_sentence, target_sentence] = random.choice(pairs)
        myeval(encoder, decoder, input_sentence, input_lang, output_lang, USE_CUDA, max_length, temperature_fun, target_sentence)

def alan_eval(encoder, decoder, input_sentence, max_length, target_sentence=None, debug=False):
    if debug:
        output_words, attentions = evaluateBest(encoder, decoder, input_sentence, input_lang, output_lang, USE_CUDA, max_length)
        output_sentence = ' '.join(output_words)
        return(output_sentence[:-6])
    else:
        output_words, attentions = evaluate(encoder, decoder, input_sentence, input_lang, output_lang, USE_CUDA, max_length, temperature_fun)
        output_sentence = ' '.join(output_words)
        return(output_sentence[:-1])
