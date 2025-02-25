import pandas as pd
import streamlit as st
import plotly.express as px
from io import BytesIO
from graphs import plot_mosaic_with_residuals

def plot_bar_chart_facets(df, varmap, prefix='odc1', ordered_categories=None, title='', height=800):
    if ordered_categories is None:
        ordered_categories = ["Concordo totalmente", "Concordo em parte", "Discordo em parte", "Discordo totalmente", "Não sei"][::-1]

    columns = [col for col in df.columns if col.startswith(prefix)]
    counts = df[columns].apply(pd.Series.value_counts).fillna(0).reset_index()
    counts = counts.melt(id_vars = "index", var_name='Pergunta', value_name='Contagem')
    counts.columns = ['Resposta', 'Pergunta', 'Contagem']
    counts = counts.sort_values('Contagem')
    counts['Resposta'] = pd.Categorical(counts['Resposta'], categories=ordered_categories, ordered=True)


    fig = px.bar(counts, 
                 x='Contagem', 
                 y='Resposta', 
                 facet_col='Pergunta', 
                 facet_col_wrap=2, 
                 title=title,
                 height=height)
    fig.for_each_annotation(lambda a: a.update(
        text=f"<b>{'<br>'.join(' '.join(varmap[a.text.split('=')[1]].split(' ')[i:i+18]) for i in range(0, len(varmap[a.text.split('=')[1]].split(' ')), 18))}</b>"
    ))

    fig.update_xaxes(title_text='')  # Remove título do eixo x e mantém os rótulos
    fig.update_yaxes(title_text='')  # Remove título do eixo y e mantém os rótulos

    fig.update_layout(xaxis_title='', 
                      yaxis_title='',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

# Example usage
# plot_bar_chart(df, varmap)

def plot_bar_chart(df, column, ordered_categories=None, title='', height=800, categorical=True, orientation='h'):
    if categorical:
        if ordered_categories is None:
            ordered_categories = ["Concordo totalmente", "Concordo em parte", "Discordo em parte", "Discordo totalmente", "Não sei"][::-1]

        counts = df[column].value_counts().reindex(ordered_categories).fillna(0).reset_index()
        counts.columns = ['Valores', 'Frequência']
        counts['Valores'] = pd.Categorical(counts['Valores'], categories=ordered_categories, ordered=True)
        counts = counts.sort_values('Valores')
    else:
        counts = df[column].value_counts().reset_index()
        counts.columns = ['Valores', 'Frequência']

    fig = px.bar(counts, 
                 x='Valores', 
                 y='Frequência', 
                 title=title,
                 height=height,
                 orientation=orientation)
    
    fig.update_xaxes(title_text='')  # Remove título do eixo x e mantém os rótulos
    fig.update_yaxes(title_text='')  # Remove título do eixo y e mantém os rótulos

    fig.update_layout(xaxis_title='', 
                      yaxis_title='',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

# Example usage
# plot_bar_chart(df, 'column_name', categorical=True)

def plot_bar_chart_simplecounts(df, prefix, varmap, title='', height=800):
    columns = [col for col in df.columns if col.startswith(prefix)]
    counts = df[columns].apply(lambda x: x == "Sim").sum().reset_index()
    counts.columns = ['Pergunta', 'Contagem']
    counts['Pergunta'] = counts['Pergunta'].map(varmap)
    counts = counts.sort_values('Contagem', ascending=True)


    # Criar o gráfico de barras horizontal
    fig = px.bar(counts, 
                x='Contagem', 
                y='Pergunta', 
                orientation='h', 
                title='')

    # Atualizar os rótulos dos eixos
    fig.update_layout(xaxis_title='Frequência', yaxis_title='Variável')
    
    fig.update_xaxes(title_text='')  # Remove título do eixo x e mantém os rótulos
    fig.update_yaxes(title_text='')  # Remove título do eixo y e mantém os rótulos

    fig.update_layout(xaxis_title='', 
                      yaxis_title='',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

def define_categories(prefix):
    if prefix == "CE02":
        return ["Masculino", "Feminino"]
    elif prefix == "CE03":
        return ["Não frequentou escola", "Ensino Fundamental Incompleto", "Ensino Fundamental", "Ensino Médio Incompleto", "Ensino Médio", "Ensino Superior Incompleto", "Ensino Superior"]
    elif prefix == "CE04":
        return ["Branca", "Preta", "Amarela", "Parda", "Indígena"]
    # elif prefix == "CE05":
    #     return ["Cristã católica", 
    #             "Cristã evangélica Pentecostal e Neopentecostal",
    #             "Cristã Protestantes históricas",
    #             "Espírita",
    #             "Matrizes africanas",
    #             "Religiões Orientais",
    #             "Judaísmo",
    #             "Islamismo",
    #             "Tradições indígenas",
    #             "Ateu ou agnóstico",
    #             "Não tenho religião",
    #             "Outros"
    #     ]
    elif prefix == "CE06":
        return ["Muito importante", "Importante", "Pouco importante", "Nada importante"]
    elif prefix == "CE07":
        return ["De esquerda", "De centro", "Liberal", "Conservador", "De direita", "Nenhuma dessas"]
    elif prefix == "CE08":
        return ["Sênior", "1A", "1B", "1C", "1D", "2"]
    elif prefix == "CE10":
        return ["ciência aplicada", "ciência básica", "tanto ciência básica como aplicada", "não se aplica"]
    elif prefix == "CE11":
        return ["Ciências Exatas e da Terra", "Ciências Biológicas", "Engenharias", "Ciências da Saúde", 
                "Ciências Agrárias", "Ciências Sociais Aplicadas", "Ciências Humanas", "Linguística, Letras e Artes"]
    elif prefix == "CE13":
        return ["Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"]
    elif prefix == "CE14":
        return ["Até 5 anos", "6 a 10 anos", "11 a 20 anos", "21 a 35 anos", "Acima de 35 anos"]
    


def render_dashboard(df, varmap, varset1, varset2, ordered_categories1=None, ordered_categories2=None, key="", pills1 = "", pills2 = "", width=1000):
    if not isinstance(varset1, dict):
        st.error("varset1 precisa ser um dicionário.")
        return
    
    if not isinstance(varset2, (dict, str)):
        st.error("varset2 precisa ser um dicionário ou uma string.")
        return
        
    default1 = list(varset1.values())[0]

    if isinstance(varset2, dict):
        default2 = list(varset2.values())[0]
    else:
        default2 = [value for key, value in varmap.items() if key.startswith(varset2)][0]

    valor_selecionado = st.pills(pills1, list(varset1.values()), default=default1, key=f'valor_selecionado_dashboard{key}')
    
    if isinstance(varset2, dict):
        tema_selecionado = st.pills(pills2, list(varset2.values()), default=default2, key=f'tema_selecionado_dashboard{key}')
    else:
        tema_selecionado = st.pills(pills2, [varmap[key] for key in varmap if key.startswith(varset2)], default=default2, key=f'tema_selecionado_dashboard{key}')
    
    if valor_selecionado == tema_selecionado:
        st.error("Selecione valores diferentes para as variáveis.")
        return

    if not valor_selecionado and not tema_selecionado:
        st.error("Selecione um valor e um tema para visualizar o dashboard.")
    
    elif valor_selecionado and tema_selecionado:
        if isinstance(varset2, dict):
            var2 = [key for key, value in varset2.items() if value == tema_selecionado][0]
        elif isinstance(varset2, str):
            var2 = [key for key, value in varmap.items() if value == tema_selecionado][0]

        var1 = [key for key, value in varset1.items() if value == valor_selecionado][0]

    if not ordered_categories1:
        ordered_categories1 = define_categories(var1)

    if ordered_categories1:
        df[var1] = pd.Categorical(df[var1], categories=ordered_categories1, ordered=True)
    if ordered_categories2:
        df[var2] = pd.Categorical(df[var2], categories=ordered_categories2, ordered=True)

    # Gráfico de mosaico
    fig_mosaic, num_rows = plot_mosaic_with_residuals(df, 
                                            var1=var1, 
                                            var2=var2,
                                            figsize=(12, 10))
    
    buf = BytesIO()
    fig_mosaic.savefig(buf, format="png", bbox_inches="tight", dpi=100)
    buf.seek(0)

    st.image(buf, width=width)

# Example usage
# ordered_categories = ["Concordo totalmente", "Concordo em parte", "Discordo em parte", "Discordo totalmente", "Não sei"][::-1]
# render_dashboard(df, varmap, codigo_variaveis, ordered_categories, prefix='odc1')