import re
from copy import deepcopy

import numpy as np
from scipy import signal
from sklearn.preprocessing import minmax_scale

FS = 250

# determinação das faixas de frequências para cada rítmo
delta = (0, 4)
theta = (4, 8)   # meditação, imaginação e criatividade
alpha = (8, 12)  # relaxamento e alerta, mas não focados em algo; calma, criatividade e meditação
beta = (12, 30)  # alerta e foco em atividade específica
gamma = (30, 100)

# determinação das faixas de frequências específicas da onda Beta
beta1 = (12, 15) # foco moderado, aparece em leitura, escrita, etc
beta2 = (15, 20) # foco intenso, aparece quando solucionamos problemas e tomada de decisões
beta3 = (20, 30) # estresse e ansiedade, atividades mentais excessivas e hiperatividade

def butter_bandpass(data, lowcut, highcut, fs=FS, order=4):
    nyq = fs * 0.5
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='bandpass')
    
    return signal.filtfilt(b, a, data)


def butter_lowpass(data, lowcut, fs=FS, order=4):
    nyq = fs * 0.5
    low = lowcut / nyq
    b, a = signal.butter(order, low, btype='lowpass')
    
    return signal.filtfilt(b, a, data)


def butter_highpass(data, highcut, fs=FS, order=4):
    nyq = fs * 0.5
    high = highcut / nyq
    b, a = signal.butter(order, high, btype='highpass')
    
    return signal.filtfilt(b, a, data)


def butter_notch(data, cutoff, var=1, fs=FS, order=4):
    nyq = fs * 0.5
    low = (cutoff - var) / nyq
    high = (cutoff + var) / nyq
    b, a = signal.iirfilter(order, [low, high], btype='bandstop', ftype='butter')
    
    return signal.filtfilt(b, a, data)


def filter_data(data, fs=FS, notchs=[60, 120], lowpass=30., highpass=3.):
    data = deepcopy(data)
    for i in range(10):
        for notch in notchs:
            data = butter_notch(data, notch, fs=fs)
        data = butter_lowpass(data, lowpass, fs=fs)
        data = butter_highpass(data, highpass, fs=fs)

    return data


def calculate_avarage(data):
    return np.average(data, axis=0)


def get_features(data):
    features = list()
    for mi, ma in [delta, theta, alpha, beta, gamma]:
        features.append(data[mi:ma])
    features = [np.average(f) for f in features]
    y = ('delta', 'theta', 'alpha', 'beta', 'gamma')

    return features, y


def segment_array(array, buffer_size, overlap=0):
    if buffer_size <= 0:
        raise ValueError('buffer_size devem ser maiores que zero.')

    array = array.T
    step_size = buffer_size - overlap
    num_buffers = int(np.ceil((array.shape[0] - overlap) / float(step_size)))
    for i in range(num_buffers):
        start_index = i * step_size
        end_index = start_index + buffer_size
        buffer = array[start_index:end_index, :]
        yield buffer.T 


def load_openbci_output_file(filename):
    with open(filename) as arquivo:
        linhas = arquivo.readlines()

    data = list()
    for i, linha in enumerate(linhas):
        res = re.search('^\d{1,3},((\ -?.+?,){8})', linha)
        if res:
            cols = res.group(1)
            data.append([float(d[1:]) for d in cols.split(',') if d])

    data = np.array(data[1:])

    return data.T


