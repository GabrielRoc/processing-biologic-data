import argparse
import os
import time
from copy import deepcopy

import numpy as np
import pandas as pd
from dashboard import app
from scipy.signal import welch
from sklearn.preprocessing import minmax_scale
from utils import (FS, calculate_avarage, filter_data, get_features,
                   load_openbci_output_file, segment_array)


def process_data(data, fs, scale, nperseg=None, noverlap=None):
    filtered_data = filter_data(data, fs=fs)
    f, Pxx = welch(filtered_data, fs, nperseg=nperseg, noverlap=noverlap)
    averaged_data = calculate_avarage(Pxx)
    features, y = get_features(averaged_data)
    if scale:
        features = list(minmax_scale(features, feature_range=(0, scale)))
    duration = filtered_data.shape[1] / fs
    
    return features, y, duration


def print_process_data(start_seconds, end_seconds, features, y):
    os.system('clear') if os.name == 'posix' else os.system('cls')
    print(f'Início: {start_seconds:.0f}s - Fim: {end_seconds:.0f}s')
    for feature, value in zip(y, features):
        print(f'  {feature.capitalize()}: {value:.3f}')
    print()


def main(input_file, fs, update_time, buffer_size, scale, nperseg, noverlap, simulation, view_time, output_file):
    if not os.path.exists(input_file):
        raise Exception('Arquivo de entrada não existe.')

    if input_file.endswith('.npy'):
        data = np.load(input_file)
    elif input_file.endswith('.txt'):
        data = load_openbci_output_file(input_file)
    else:
        raise Exception('Formato de arquivo não suportado.')

    buffer_points = int(buffer_size * fs)
    overlap = int((buffer_size - update_time) * fs)

    last_end_seconds = 0

    df = pd.DataFrame(columns=['inicio', 'fim', 'delta', 'theta', 'alpha', 'beta', 'gamma'])

    for buffer in segment_array(data, buffer_points, overlap):
        features, y, duration = process_data(buffer, fs, scale)
        start_seconds = last_end_seconds
        end_seconds = start_seconds + duration
        last_end_seconds += update_time
        result = pd.Series([start_seconds, end_seconds] + features, index=df.columns)
        df = pd.concat([df, result.to_frame().T], ignore_index=True)
        if simulation:
            print_process_data(start_seconds, end_seconds, features, y)
            df.to_csv(output_file, index=False) 
            time.sleep(view_time)


    df.to_csv(output_file, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Análise de EEG')
    parser.add_argument('input_file', type=str, help='Arquivo de entrada (npy)')
    parser.add_argument('--fs', type=int, default=FS, help='Taxa de amostragem')
    parser.add_argument('--update_time', type=float, default=1, help='Tempo de atualização (em segundos)')
    parser.add_argument('--buffer_size', type=float, default=5, help='Tamanho do buffer (em segundos)')
    parser.add_argument('--view_time', type=float, default=None, help='Tempo de visualização (em segundos')
    parser.add_argument('--nperseg', type=int, default=None, help='Tamanho da janela (default: None)')
    parser.add_argument('--noverlap', type=int, default=None, help='Sobreposição da janela (default: None)')
    parser.add_argument('--scale', type=float, default=None, help='Escalar os dados (default: None)')
    parser.add_argument('--simulation', action='store_true', help='Ativar simulação')
    parser.add_argument('--output', type=str, default='output.csv', help='Arquivo de saída (CSV)')
    args = parser.parse_args()

    if args.view_time and not args.simulation:
        raise Exception('A simulação deve estar ativa para visualização dos dados.')
    
    if args.update_time > args.buffer_size:
        raise Exception('O tempo de atualização deve ser menor que o tamanho do buffer.')

    view_time = args.view_time if args.view_time else args.update_time

    main(args.input_file, args.fs, args.update_time, args.buffer_size, args.scale, args.nperseg, args.noverlap, args.simulation, view_time, args.output)
