# Projeto de Análise de EEG

Este projeto foi desenvolvido para analisar sinais de eletroencefalograma (EEG) e extrair informações relevantes de diferentes faixas de frequência. Os arquivos de entrada podem ser no formato `.txt`, gerado pelo OpenBCI, ou no formato `.npy`, que representa um arquivo numpy já processado.

## Utilizando o arquivo `run.py`

Para executar a análise do EEG, utilize o arquivo `run.py`. Você deve fornecer um arquivo de entrada (`.txt` ou `.npy`) e diversos parâmetros opcionais. O arquivo de saída será um CSV contendo informações sobre as faixas de frequência ao longo do tempo.

### Parâmetros

- `input_file`: arquivo de entrada (`.txt` gerado pelo OpenBCI ou `.npy` já processado).
- `--fs`: taxa de amostragem (padrão: 250).
- `--update_time`: tempo de atualização em segundos (padrão: 1).
- `--buffer_size`: tamanho do buffer em segundos (padrão: 5).
- `--view_time`: tempo de visualização em segundos (necessário ativar a simulação).
- `--nperseg`: tamanho da janela (padrão: None).
- `--noverlap`: sobreposição da janela (padrão: None).
- `--scale`: escalar os dados (padrão: None).
- `--simulation`: ativar simulação.
- `--output`: arquivo de saída (CSV) (padrão: `output.csv`).
- `--debug`: ativar modo de debug da dashboard.

### Exemplo de uso

```sh
python3 run.py input_file.txt --fs 250 --update_time 1 --buffer_size 5 --simulation --view_time 1 --output output.csv
```

Este comando irá processar o arquivo `input_file.txt`, com uma taxa de amostragem de 250 Hz, um tempo de atualização de 1 segundo e um buffer de 5 segundos. A simulação será ativada, permitindo a visualização dos dados a cada 1 segundo. O resultado será salvo no arquivo `output.csv`.

## Dependências

Certifique-se de instalar as dependências necessárias listadas abaixo antes de executar o projeto:

- NumPy
- pandas
- SciPy
- scikit-learn

Você pode instalá-las usando o pip:

```sh
pip install numpy pandas scipy scikit-learn
```

## Licença

Este projeto é licenciado sob a licença MIT.