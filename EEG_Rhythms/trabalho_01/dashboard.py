import argparse

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output

global view_time
view_time = 1000

global file
file = 'data.csv'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
colors = {
    'color': [
        'rgb(102, 194, 165)',  # Verde-água
        'rgb(252, 141, 98)',   # Laranja
        'rgb(141, 160, 203)',  # Azul-claro
        'rgb(231, 138, 195)',  # Rosa
        'rgb(166, 216, 84)'    # Verde-claro
    ]
}


def get_last_row(df):
    return df.tail(1)[['delta', 'theta', 'alpha', 'beta', 'gamma']].mean()

navbar = dbc.NavbarSimple(
    children=[
        html.Div('Trabalho 01 - Processamento de sinais EEG', className='navbar-brand')
    ],
    brand_href='#',
    sticky='top',
    color='primary',
    dark=True,
)

card_bar_chart = dbc.Card(
    dbc.CardBody([
        html.H4('Média dos Sinais', className='card-title'),
        dcc.Graph(id='bar-chart'),
    ])
)

card_last_bar_chart = dbc.Card(
    dbc.CardBody([
        html.H4('Último sinal interpretado', className='card-title'),
        dcc.Graph(id='last-bar-chart'),
    ])
)

card_table = dbc.Card(
    dbc.CardBody([
        html.H4('Dados do arquivo CSV', className='card-title'),
        dash_table.DataTable(
            id='table',
            page_size=10,
        )
    ])
)

app.layout = html.Div([
    navbar,
    dbc.Container(
        dbc.Row([
            dbc.Col(html.Div([card_bar_chart]), width=6),
            dbc.Col(html.Div([card_last_bar_chart]), width=6),
        ]),
        fluid=True,
    ),
    dbc.Container(
        dbc.Row([
            dbc.Col(html.Div([card_table]), width=12),
        ]),
        fluid=True,
    ),
    dcc.Interval(
        id='interval-component',
        interval=view_time,
        n_intervals=0
    ),
])

@app.callback(
    [Output('bar-chart', 'figure'), Output('last-bar-chart', 'figure')],
    [Input('interval-component', 'n_intervals')])
def update_charts(n):
    df = pd.read_csv(file)
    grouped = df[['delta', 'theta', 'alpha', 'beta', 'gamma']].mean()
    last_row = get_last_row(df)
    
    bar_chart_figure = {
        'data': [
            {'x': ['delta', 'theta', 'alpha', 'beta', 'gamma'], 'y': grouped, 'type': 'bar', 'marker': colors}
        ],
        'layout': {
            'title': 'Faixas de frequência (média)',
            'yaxis': {'title': 'Amplitude'},
            'xaxis': {'title': 'Faixa de frequência'},
            'transition': {'duration': 1000}
        }
    }
    
    last_bar_chart_figure = {
        'data': [
            {'x': ['delta', 'theta', 'alpha', 'beta', 'gamma'], 'y': last_row, 'type': 'bar', 'marker': colors}
        ],
        'layout': {
            'title': 'Faixas de frequência (último valor)',
            'yaxis': {'title': 'Amplitude'},
            'xaxis': {'title': 'Faixa de frequência'},
            'transition': {'duration': 1000}
        }
    }
    
    return bar_chart_figure, last_bar_chart_figure


@app.callback(
    [Output('table', 'data'), Output('table', 'columns')],
    [Input('interval-component', 'n_intervals')])
def update_table(n):
    df = pd.read_csv(file)
    table_data = df.to_dict('records')
    table_columns = [{'name': i, 'id': i} for i in df.columns]
    
    return table_data, table_columns


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dashboard de Análise de EEG')
    parser.add_argument('input_file', type=str, help='Arquivo de dados CSV')
    parser.add_argument('--debug', action='store_true', help='Ativa modo de debug')
    parser.add_argument('--view_time', type=float, default=1, help='Tempo de visualização em segundos')
    args = parser.parse_args()

    file = args.input_file

    view_time = int(args.view_time * 1000) if args.view_time > 0 else 1000

    app.run_server(debug=args.debug)