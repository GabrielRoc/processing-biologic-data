import argparse
import os
import subprocess
import webbrowser


def build_arg_list(args, arg_map):
    arg_list = []
    for key, value in arg_map.items():
        if isinstance(value, str):
            arg_value = getattr(args, value)
            if arg_value is not None:
                if arg_value is True:
                    arg_list.append(key)
                else:
                    arg_list.extend([key, str(arg_value)])
    return arg_list


def process_arg_list(args):
    arg_map = {
        '--fs': 'fs',
        '--update_time': 'update_time',
        '--buffer_size': 'buffer_size',
        '--view_time': 'view_time',
        '--nperseg': 'nperseg',
        '--noverlap': 'noverlap',
        '--scale': 'scale',
        '--simulation': 'simulation',
        '--output': 'output'
    }
    return [args.input_file] + build_arg_list(args, arg_map)


def dashboard_arg_list(args):
    arg_map = {
        '--debug': 'debug',
        '--view_time': 'view_time'
    }
    return [args.output] + build_arg_list(args, arg_map)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Projeto de Análise de EEG')
    parser.add_argument('input_file', type=str, help='Arquivo de entrada (npy)')
    parser.add_argument('--fs', type=int, default=None, help='Taxa de amostragem')
    parser.add_argument('--update_time', type=float, default=None, help='Tempo de atualização (em segundos)')
    parser.add_argument('--buffer_size', type=float, default=None, help='Tamanho do buffer (em segundos)')
    parser.add_argument('--view_time', type=float, default=None, help='Tempo de visualização (em segundos')
    parser.add_argument('--nperseg', type=int, default=None, help='Tamanho da janela (default: None)')
    parser.add_argument('--noverlap', type=int, default=None, help='Sobreposição da janela (default: None)')
    parser.add_argument('--scale', type=float, default=None, help='Escalar os dados (default: None)')
    parser.add_argument('--simulation', action='store_true', help='Ativar simulação')
    parser.add_argument('--output', type=str, default='output.csv', help='Arquivo de saída (CSV)')
    parser.add_argument('--debug', action='store_true', help='Ativa modo de debug')
    args = parser.parse_args()

    process_script = 'process.py'
    dashboard_script = 'dashboard.py'

    python_executable = 'python' if os.name == 'nt' else 'python3'

    if args.simulation:
        dashboard_process = subprocess.Popen([python_executable, dashboard_script] + dashboard_arg_list(args))
    process_process = subprocess.Popen([python_executable, process_script] + process_arg_list(args))

    webbrowser.open('http://localhost:8050')

    if args.simulation:
        dashboard_process.wait()
    process_process.wait()

    os.system('python')