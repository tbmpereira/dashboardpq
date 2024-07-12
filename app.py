from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from plotly.subplots import make_subplots

load_figure_template("plotly_dark")

df - pd.read_csv("data_tratado.csv")

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.UNITED, dbc.icons.FONT_AWESOME, dbc_css], title="Atividade de divulgação científica de bolsistas produtividade CNPq")

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

titulo_controls = html.H4("Use os controles abaixo para filtrar os dados", className="text-left bg-primary text-white p-2 mb-2", style={"margin": "-15"})

