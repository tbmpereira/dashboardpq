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


def render_dashboard(df, varmap, codigo_variaveis, ordered_categories=None, prefix='odc1', key=""):
    valor_selecionado = st.pills("Valor", list(codigo_variaveis.values()), default=None, key=f'valor_selecionado_dashboard{key}')
    tema_selecionado = st.pills("Tema", [varmap[key] for key in varmap if key.startswith(prefix)], default=None, key=f'tema_selecionado_dashboard{key}')
    
    if valor_selecionado and tema_selecionado:
        key = [key for key, value in codigo_variaveis.items() if value == valor_selecionado][0]
        var1 = [key for key, value in varmap.items() if value == tema_selecionado][0]
        df[var1] = pd.Categorical(df[var1], categories=ordered_categories, ordered=True)
        
        # Gráfico de mosaico
        p, fig_mosaic, num_rows = plot_mosaic_with_residuals(df, 
                                                var1=var1, 
                                                var2=key,
                                                ordered_categories=ordered_categories,
                                                figsize=(7, 5))
        
        buf = BytesIO()
        fig_mosaic.savefig(buf, format="png", bbox_inches="tight", dpi=100)
        buf.seek(0)

        st.image(buf, width=1000)

# Example usage
# ordered_categories = ["Concordo totalmente", "Concordo em parte", "Discordo em parte", "Discordo totalmente", "Não sei"][::-1]
# render_dashboard(df, varmap, codigo_variaveis, ordered_categories, prefix='odc1')