from dash import Dash, dcc, html, Input, Output, callback
from scipy.stats import chi2_contingency, chi2
import pandas as pd
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pickle
from statsmodels.graphics.mosaicplot import mosaic
from scipy.stats import chi2_contingency
import numpy as np
import plotly.express as px
from io import BytesIO
import base64
import matplotlib

matplotlib.use('Agg')  # Use o backend 'Agg' para renderizar a imagem sem interface gráfica
load_figure_template("plotly_dark")

# Carregar o mapeamento de variáveis
with open("varmap.pkl", "rb") as f:
    varmap = pickle.load(f)

df = pd.read_csv("data_tratado.csv")

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN, dbc.icons.FONT_AWESOME, dbc_css], 
           title="Atividade de divulgação científica de bolsistas produtividade CNPq",
           suppress_callback_exceptions=True)

header = html.Div(
    dbc.Row(
        dbc.Col(
            html.H1("Atividade de divulgação científica de bolsistas produtividade CNPq"),
            className="bg-primary text-white p-2 mb-2 text-center",
            width=12
        )
    ),
    className="bg-primary"
)

titulo_controls = html.H4("Use os controles abaixo para filtrar os dados", className="text-left bg-primary text-white p-2 mb-2 rounded", style={"margin": "-15"})

idade_slider = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Label("Idade:"),
                dcc.RangeSlider(
                    id="idade_slider",
                    min=20,
                    max=90,
                    step=1,
                    marks={i: str(i) for i in range(20, 91, 10)},
                    value=[20, 90]
                ),
                html.Div(id="idade_output", className="mt-2")
            ]
        )
    ],
    className="border-primary border-3 rounded mb-4",
)

sexo_radio = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Label("Sexo:"),
                dcc.Dropdown(
                    id="sexo_radio",
                    options=[
                        {"label": "Masculino", "value": "Masculino"},
                        {"label": "Feminino", "value": "Feminino"}
                    ],
                    value=[
                        "Masculino",
                        "Feminino"
                    ],
                    multi=True,
                    style={"zIndex": "1", "position": "relative"}
                    )
        ],
                className="mb-4",
        )
    ],
    className="border-primary border-3 rounded mb-4",
)

cores = sorted(list(df.CE04.unique())[1:])

cor_racial_checklist = dbc.Card(
    dbc.CardBody(
        dbc.Row(
            [
                dbc.Label("Cor/raça:"),
                dcc.Dropdown(
                    cores,
                    cores,
                    id="cor_racial_dropdown",
                    multi=True,
                    style={"zIndex": "1", "position": "relative"}
                )
            ]
        )
    ),
    className="border-primary border-3 rounded mb-4"
)

ideologias = sorted(list(df.CE07.unique())[1:])

ideologia_checklist = dbc.Card(
    dbc.CardBody(
        dbc.Row(
            [
                dbc.Label("Ideologia política:"),
                dcc.Dropdown(
                    ideologias,
                    ideologias,
                    multi=True,
                    id="ideologia_dropdown",
                    style={"zIndex": "1", "position": "relative"}
                )
            ]
        )
    ),
    className="border-primary border-3 rounded mb-4"
)

produtividade_checklist = dbc.Card(
    dbc.CardBody(
        dbc.Row(
            [
                dbc.Label("Produtividade:"),
                dcc.Dropdown(
                    options=[
                        {"label": "1A", "value": "1A"},
                        {"label": "1B", "value": "1B"},
                        {"label": "1C", "value": "1C"},
                        {"label": "1D", "value": "1D"},
                        {"label": "2", "value": "2"},
                        {"label": "Senior", "value": "Senior"},
                    ],
                    value=['1A', '1B', '1C', '1D', '2', 'Senior'],
                    multi=True,
                    id="produtividade_dropdown",
                    style={"zIndex": "1", "position": "relative"}
                )
            ]
        )
    ),
    className="border-primary border-3 rounded mb-4"
)

areas = areas = sorted(list(df.CE11.unique())[1:])

gde_area_checklist = dbc.Card(
    dbc.CardBody(
        dbc.Row(
            [
                dbc.Label("Grande área do conhecimento:"),
                dcc.Dropdown(
                    areas, 
                    areas,
                    id="gde_area_checklist", 
                    multi=True,
                    style={"zIndex": "1", "position": "relative"}
                )
            ]
        )
    ),
    className="border-primary border-3 rounded mb-4"
)

regiao_checklist = dbc.Card(
    dbc.CardBody(
        dbc.Row(
            [
                dbc.Label("Região:"),
                dcc.Dropdown(
                    ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'], 
                    value=['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'],
                    id="regiao_checklist", 
                    multi=True,
                    style={"zIndex": "1", "position": "relative"}
                )
            ]
        )
    ),
    className="border-primary border-3 rounded mb-4"
)
                                        
controls = dbc.Card(
    [titulo_controls, idade_slider, sexo_radio, gde_area_checklist, regiao_checklist, cor_racial_checklist, produtividade_checklist,
     ideologia_checklist], body=True
)

sobre_content = dbc.Tab(
    [
        html.H2("Sobre os dados"),
        html.P('''Os dados apresentados neste painel foram coletados por meio de um questionário aplicado a bolsistas de produtividade do CNPq. 
               A coleta foi realizada entre janeiro e março de 2023 através de convites enviados a uma amostra estratificada de bolsistas.'''),
    ],
    label="Sobre",
    tab_id="sobre",
)

atividades = [value for key, value in varmap.items() if "adc1[SQ" in key]

atividades_dropdown = dcc.Dropdown(
                    id="atividades_dropdown",
                    options=[{"label": atividade, "value": atividade} for atividade in atividades],
                    value= atividades[0] if atividades else None,
                    style={"zIndex": "1", "position": "relative"}
                )

variables = ['CE01', 'CE02', 'CE03', 'CE04', 'CE05', 'CE10', 'CE07', 'CE08', 'CE11', 'CE13', 'CE15']
interest_var = {key: value for key, value in varmap.items() if key in variables}


variaveis_dropdown = dcc.Dropdown(
    id="variaveis_dropdown",
    options=[{"label": value, "value": key} for key, value in interest_var.items()],
    value="CE02",
    style={"zIndex": "1", "position": "relative"}
)

mosaic_tab = dbc.Tab(
    [
        html.H2("Gráfico de mosaico"),
        html.P('''O gráfico de mosaico é uma forma de visualização que permite comparar a distribuição de uma variável categórica em diferentes grupos.
                Cada bloco no gráfico representa uma categoria da variável categórica e o tamanho do bloco é proporcional à frequência da categoria.
                A cor do bloco é determinada pelo residual de Pearson, que indica a diferença entre a frequência observada e a frequência esperada para aquela categoria.
               Selecione abaixo a atividade de divulgação científica e a variável de interesse para visualizar o gráfico de mosaico.'''),
        html.Div(
            [
                html.Div(
                    [html.H3("Atividade de divulgação científica:"), atividades_dropdown],
                    style={'flex': 1, 'margin-right': '10px', 'display': 'flex', 'flex-direction': 'column'}
                ),
                html.Div(
                    [html.H3("Variável de interesse:"), variaveis_dropdown],
                    style={'flex': 1, 'display': 'flex', 'flex-direction': 'column'}
                )
            ],
            style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'width': '100%'}
        ),
        html.Img(id="mosaic_output", style={'width': '100%', 'height': 'auto'})
    ],
    label="Gráfico de mosaico",
    tab_id="mosaic"
)

def wrap_labels(labels, width=30):
    """
    Quebra os rótulos em várias linhas se excederem a largura especificada.

    Parâmetros:
    labels: Lista de rótulos do eixo x.
    width: Comprimento máximo de caracteres antes de quebrar a linha.

    Retorna:
    labels: Lista de rótulos ajustados com quebras de linha.
    """
    return ['\n'.join([label[i:i+width] for i in range(0, len(label))]) for label in labels]


def plot_mosaic(df, activity_col, interest_var):

    ordered_categories = ['Nenhuma vez', '1 vez', '2 vezes', '3 vezes', '4 vezes', '5 vezes', 'mais de 5 vezes']

    # Verificar e aplicar categorias ordenadas
    if ordered_categories:
        df[activity_col] = pd.Categorical(df[activity_col], categories=ordered_categories, ordered=True)

    # Criar uma nova coluna que representa a ordem das categorias
    df['activity_order'] = df[activity_col].apply(lambda x: ordered_categories.index(x))

    # Ordenar o DataFrame pela nova coluna
    df = df.sort_values('activity_order')

    # Criar tabela de contingência
    contingency_table = pd.crosstab(df[activity_col], df[interest_var])

    # Calcular o teste de qui-quadrado e obter os resíduos de Pearson
    chi2_stat, p, dof, expected = chi2_contingency(contingency_table)
    residuals = (contingency_table - expected) / np.sqrt(expected)

    # Pontos de corte para o esquema de coloração
    cutoff_05 = 2
    cutoff_001 = 4

    # Função para mapear a cor dos blocos com base nos resíduos de Pearson
    def residual_color(key):
        if key[1] in residuals.index and key[0] in residuals.columns:
            value = residuals.loc[key[1], key[0]]  # Ajusta para o eixo correto
            if value >= cutoff_001:
                return {'color': 'red'}
            elif value >= cutoff_05:
                return {'color': 'lightcoral'}  # Substituindo por uma cor mais intensa
            elif value <= -cutoff_001:
                return {'color': 'blue'}
            elif value <= -cutoff_05:
                return {'color': 'dodgerblue'}  # Substituindo por uma cor mais intensa
            else:
                return {'color': 'lightgrey'}  # Cor neutra para resíduos não significativos
        else:
            return {'color': 'lightgrey'}  # Cor padrão para valores fora da tabela

    # Criar uma nova figura com tamanho aumentado
    fig, ax = plt.subplots(figsize=(14, 10))  # Ajuste o tamanho conforme necessário

    # Criar o gráfico de mosaico
    mosaic(df, [interest_var, activity_col], properties=residual_color, ax=ax, gap=0.02, labelizer=lambda k: '')

    # Adicionar a legenda para as cores dos resíduos de Pearson
    bounds = [-cutoff_001, -cutoff_05, cutoff_05, cutoff_001]
    cmap = plt.cm.RdBu_r  # Colormap invertido para ter azul para valores negativos e vermelho para positivos
    norm = plt.Normalize(vmin=-cutoff_001, vmax=cutoff_001)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    # Configurando a barra de cores com ticks personalizados
    cbar = plt.colorbar(sm, ax=ax, ticks=[-cutoff_001, -cutoff_05, cutoff_05, cutoff_001])
    cbar.ax.set_yticklabels(['<= -4', '-2', '2', '>= 4'])  # Labels nos limites de ±2 e ±4

    # Adicionar valor de p abaixo da barra de cores
    cbar.ax.text(0.5, -0.1, f'p-valor: {p:.3f}', transform=cbar.ax.transAxes, fontsize=12, 
                 verticalalignment='top', horizontalalignment='center', 
                 bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    # Atualiza os rótulos do eixo x com quebras de linha
    xtick_labels = [tick.get_text() for tick in ax.get_xticklabels()]
    ax.set_xticklabels(wrap_labels(xtick_labels), rotation=45, ha='right')

    # Adicionar título ao gráfico
    # ax.set_title(f'Relação entre {activity_col} e {interest_var}', fontsize=16)

    # Reposicionar a barra de legenda
    fig.subplots_adjust(left=0.1, right=0.8, top=0.95, bottom=0.15)
    cbar.ax.set_position([0.85, 0.15, 0.03, 0.8])  # left, bottom, width, height

    # Salvar em um buffer temporário
    buf = BytesIO()
    plt.savefig(buf, format="png")
    # Embutir o resultado na saída HTML
    data = base64.b64encode(buf.getbuffer()).decode("utf8")
    fig_mosaic_matplotlib = f'data:image/png;base64,{data}'

    return fig_mosaic_matplotlib

list_of_activities = [value for key, value in varmap.items() if "adc1[SQ" in key]

def create_bar_plot(df, ordered_categories):
    """
    Gera um gráfico de barras baseado nos dados fornecidos e nas categorias ordenadas.

    Parâmetros:
    df: DataFrame contendo os dados
    ordered_categories: lista de categorias ordenadas para a variável 'Frequência'

    Retorna:
    fig: Gráfico de barras gerado pelo Plotly Express
    """
    # Filtra e transforma os dados
    df_melted = df.melt(value_vars=[col for col in df.columns if col.startswith('adc1')],
                        var_name='Atividade', value_name='Frequência')

    # Converte a coluna 'Frequência' para um tipo categórico com as categorias ordenadas
    df_melted['Frequência'] = pd.Categorical(df_melted['Frequência'], categories=ordered_categories, ordered=True)

    # Substitui os nomes das atividades pelos valores correspondentes em varmap
    # df_melted['Atividade'] = df_melted['Atividade'].map(varmap)

    # Mapeia as atividades do DataFrame para a lista de atividades
    activity_map = {activity: list_of_activities[idx] for idx, activity in enumerate(df_freq['Atividade'].unique())}

    df_freq['Atividade'] = df_freq['Atividade'].map(activity_map)

    # Agrega os dados
    df_freq = df_melted.groupby(['Atividade', 'Frequência']).size().reset_index(name='Contagem')

    # Define a paleta de cores com base no tema LUMEN
    color_palette = px.colors.qualitative.T10  # Ajuste a paleta conforme necessário

    # Cria o gráfico de barras ordenado com a paleta de cores personalizada
    fig = px.bar(df_freq, x='Atividade', y='Contagem', color='Frequência',
                 category_orders={'Frequência': ordered_categories},
                 title='Distribuição das Respostas por Atividade',
                 template='simple_white', color_discrete_sequence=color_palette)
    
    # Aplica a quebra de linha nos rótulos do eixo x e rotaciona 45 graus
    fig.update_layout(
         xaxis=dict(
            tickmode='array',
            tickvals=list(activity_map.values()),
            ticktext=wrap_labels(list(activity_map.values()), width=20)
        ),
        xaxis_title='',  # Remove o rótulo do eixo x
        yaxis_title='',  # Remove o rótulo do eixo y
    )

    # Rotaciona os rótulos do eixo x
    fig.update_xaxes(tickangle=45)

    return fig

# Cria o gráfico utilizando a função

ordered_categories = ['Nenhuma vez', '1 vez', '2 vezes', '3 vezes', '4 vezes', '5 vezes', 'mais de 5 vezes']

fig = create_bar_plot(df, ordered_categories=ordered_categories)

# Define a tab que contém o gráfico
graph_tab = dbc.Tab(
    label="Gráfico de Barras",
    tab_id="graph_tab",
    children=[
        html.H3("Distribuição das Respostas por Atividade"),
        dcc.Graph(figure=fig)  # Insere o gráfico na tab
    ]
)

tabs = dbc.Tabs([graph_tab, mosaic_tab, sobre_content], id="tabs", active_tab="graph_tab")

card_n = dbc.Card(
    dbc.CardBody(
        [
            html.H4(f"Total da amostra: {len(df)}"),
            html.H5(id="n_filtrado"),
        ],
        className="text-center"
    ),
    color="primary",
    inverse=True
)


footer = html.Footer(
    dbc.Container(
        dbc.Row(
            dbc.Col(
                [html.P(
                    [
                        " Dashboard desenvolvido por ",
                        html.A("Marcelo Pereira", href="https://marcelo-pereira.notion.site/", target="_blank"),
                        " ",
                        html.I(className="fa-brands fa-creative-commons"),
                        ', 2024'
                    ],
                    className="text-center"
                ),
                ]
            )
        ),
        fluid=True,
        className="py-3"
    ),
    className="footer bg-light text-dark mt-auto"
)

app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col(controls, width=3),
                dbc.Col([tabs, card_n], width=9),
            ],
            className="mt-4",
        ),
        footer
    ],
    fluid=True,
    className="dbc dbc-ag-grid",
)

@app.callback(
    Output("mosaic_output", "src"),
    [Input("atividades_dropdown", "value"), 
     Input("variaveis_dropdown", "value")]
)
def update_mosaic(selected_activity, selected_interest_var):
    # Mapeia o valor do Dropdown de volta para a chave do DataFrame
    activity_key = {v: k for k, v in varmap.items()}.get(selected_activity)
    interest_var_key = selected_interest_var  # Já é a chave correta do DataFrame

    # Verifica se as chaves mapeadas existem no DataFrame
    if activity_key in df.columns and interest_var_key in df.columns:
        fig = plot_mosaic(df, activity_key, interest_var_key)
        return fig
    else:
        # Retorna uma figura vazia ou um gráfico de aviso em caso de erro
        return {}

@app.callback(
    Output("idade_output", "children"),
    Input("idade_slider", "value")
)
def update_idade_output(value):
    return f"Idade selecionada: {value[0]} - {value[1]}"

if __name__ == '__main__':
    app.run(debug=True)