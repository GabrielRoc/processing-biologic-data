import argparse
import os
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


def main(input_file, fs, update_time, scale, simulation, real_time, output_file="output.csv"):
    if not os.path.exists(input_file):
        raise Exception("Arquivo de entrada não existe.")

    if input_file.endswith(".npy"):
        data = np.load(input_file)
    elif input_file.endswith(".txt"):
        data = load_openbci_output_file(input_file)
    else:
        raise Exception("Formato de arquivo não suportado.")

    last_end_seconds = 0

    if os.path.exists(output_file):
        df = pd.read_csv(output_file)
    else:
        df = pd.DataFrame(columns=['inicio', 'fim', 'delta', 'theta', 'alpha', 'beta', 'gamma'])

    if not df.empty:
        last_end_seconds = df.iloc[-1]['fim']

    if simulation:
        for buffer in segment_array(data, int(update_time * fs), update_time, real_time):
            features, y, duration = process_data(buffer, fs, scale)
            start_seconds = last_end_seconds
            end_seconds = start_seconds + duration
            last_end_seconds = end_seconds
            result = pd.Series([start_seconds, end_seconds] + features, index=df.columns)
            df = pd.concat([df, result.to_frame().T], ignore_index=True)
            df.to_csv(output_file, index=False)
    else:
        features, y, duration = process_data(data, fs, scale)
        start_seconds = last_end_seconds
        end_seconds = start_seconds + duration
        result = pd.Series([start_seconds, end_seconds] + features, index=df.columns)
        df = pd.concat([df, result.to_frame().T], ignore_index=True)
        df.to_csv(output_file, index=False)

    # df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Análise de EEG")
    parser.add_argument("input_file", type=str, help="Arquivo de entrada (npy)")
    parser.add_argument("update_time", type=float, help="Tempo de atualização (em segundos)")
    parser.add_argument("--fs", type=int, default=FS, help="Taxa de amostragem")
    parser.add_argument("--scale", type=float, default=None, help="Escalar os dados (default: None)")
    parser.add_argument("--simulation", action="store_true", help="Ativar simulação")
    parser.add_argument("--real_time", type=lambda x: x.lower() in ['true', 't', '1', 'yes', 'y'], default=True, help="Simulação em tempo real")
    parser.add_argument("--output", type=str, default="output.csv", help="Arquivo de saída (CSV)")
    args = parser.parse_args()

    if(args.real_time and not args.simulation):
        raise ValueError("Real-time simulation only available in simulation mode")

    main(args.input_file, args.fs, args.update_time, args.scale, args.simulation, args.real_time, args.output)
