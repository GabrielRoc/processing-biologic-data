import argparse

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output

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
    return df.tail(1)[['alpha', 'beta', 'delta', 'theta', 'gamma']].mean()

navbar = dbc.NavbarSimple(
    children=[
        html.Div("Trabalho 01 - Processamento de sinais EEG", className="navbar-brand")
    ],
    brand_href="#",
    sticky="top",
    color="primary",
    dark=True,
)

card_bar_chart = dbc.Card(
    dbc.CardBody([
        html.H4("Média dos Sinais", className="card-title"),
        dcc.Graph(id='bar-chart'),
    ])
)

card_last_bar_chart = dbc.Card(
    dbc.CardBody([
        html.H4("Último sinal interpretado", className="card-title"),
        dcc.Graph(id='last-bar-chart'),
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
    dcc.Interval(
        id='interval-component',
        interval=1500,
        n_intervals=0
    ),
])

@app.callback(
    [Output('bar-chart', 'figure'), Output('last-bar-chart', 'figure')],
    [Input('interval-component', 'n_intervals')])
def update_charts(n):
    df = pd.read_csv(file)
    grouped = df[['alpha', 'beta', 'delta', 'theta', 'gamma']].mean()
    last_row = get_last_row(df)
    
    bar_chart_figure = {
        'data': [
            {'x': ['alpha', 'beta', 'delta', 'theta', 'gamma'], 'y': grouped, 'type': 'bar', 'marker': colors}
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
            {'x': ['alpha', 'beta', 'delta', 'theta', 'gamma'], 'y': last_row, 'type': 'bar', 'marker': colors}
        ],
        'layout': {
            'title': 'Faixas de frequência (último valor)',
            'yaxis': {'title': 'Amplitude'},
            'xaxis': {'title': 'Faixa de frequência'},
            'transition': {'duration': 1000}
        }
    }
    
    return bar_chart_figure, last_bar_chart_figure

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dashboard de Análise de EEG")
    parser.add_argument("input_file", type=str, help="Arquivo de dados CSV")
    parser.add_argument("--debug", action="store_true", help="Ativa modo de debug")
    args = parser.parse_args()

    global file 
    file = args.input_file

    app.run_server(debug=args.debug)