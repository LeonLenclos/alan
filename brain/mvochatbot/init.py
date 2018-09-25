import configparser

def init_config_model(config_name):
    config = configparser.ConfigParser()
    config.read(config_name)
    attn_model = config['model']['attn_model']
    hidden_size = int(config['model']['hidden_size'])
    n_layers = int(config['model']['n_layers'])
    dropout = float(config['model']['dropout'])
    optimizer_name = config['model']['optimizer']
    criterion_name = config['model']['criterion']
    learning_rate = float(config['model']['learning_rate'])
    decoder_learning_ratio = float(config['model']['decoder_learning_ratio'])
    
    return (attn_model, hidden_size, n_layers, dropout, optimizer_name, criterion_name, learning_rate, decoder_learning_ratio)

def init_config_training(config_name):
    config = configparser.ConfigParser()
    config.read(config_name)
    batch_size = int(config['training']['batch_size'])
    clip = float(config['training']['clip'])
    teacher_forcing_ratio = float(config['training']['teacher_forcing_ratio'])
    iteration = int(config['training']['iteration'])
    n_iterations = int(config['training']['n_iterations'])
    save_every = int(config['training']['save_every'])
    print_every = int(config['training']['print_every'])
    evaluate_every = int(config['training']['evaluate_every'])
    save_encoderpath = config['training']['save_encoderpath']
    save_decoderpath = config['training']['save_decoderpath']
    
    return (batch_size, clip, teacher_forcing_ratio, iteration, n_iterations, save_every, print_every, evaluate_every, save_encoderpath, save_decoderpath)

def init_config_load(config_name):
    config = configparser.ConfigParser()
    config.read(config_name)
    load_training = config['load'].getboolean('load_training')
    load_encoderpath = config['load']['load_encoderpath']
    load_decoderpath = config['load']['load_decoderpath']
    
    return (load_training, load_encoderpath, load_decoderpath)
    

def init_config_eval(config_name):
    config = configparser.ConfigParser()
    config.read(config_name)
    MAX_LENGTH = int(config['eval']['max_length'])
    temp_module_name = config['eval']['temperature_module_name']
    temp_function_name = config['eval']['temperature_function_name']
    n_best_words = int(config['eval']['n_best_words'])
    
    return (MAX_LENGTH, temp_module_name, temp_function_name, n_best_words)

def init_config_data(config_name):
    config = configparser.ConfigParser()
    config.read(config_name)
    corpuspaths = []
    qapairspath = []
    MIN_LENGTH = int(config['data']['min_length'])
    MAX_LENGTH = int(config['data']['max_length'])
    DELAY = int(config['data']['delay'])
    TRIM_MIN_COUNT = int(config['data']['trim_min_count'])
    
    USE_QACORPUS = config['data'].getboolean('use_qacorpus')
    CREATE_QAPAIRS = config['data'].getboolean('create_qapairs')
    if (not(USE_QACORPUS)):
        corpuspaths = config['data']['corpuspaths'].split(',')
    else:
        if CREATE_QAPAIRS:
            corpuspaths = config['data']['qacorpuspaths'].split(',')
        else:
            qapairspath = config['data']['qapairspath']
    
    return (MIN_LENGTH, MAX_LENGTH, TRIM_MIN_COUNT, DELAY, USE_QACORPUS, CREATE_QAPAIRS, list(map(str.strip, corpuspaths)), qapairspath)

def init_config_getSettings(config_name):
    config = configparser.ConfigParser()
    config.read(config_name)
    mode = config['init']['mode']
    use_cuda = config['init'].getboolean('use_cuda')
    
    return mode, use_cuda