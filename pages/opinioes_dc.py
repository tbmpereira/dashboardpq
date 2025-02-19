import streamlit as st
import plotly.express as px
from data_process import df, codigo_variaveis, varmap
from estrutura import plot_bar_chart_facets, render_dashboard
from graphs import plot_mosaic_with_residuals
from io import BytesIO
import pandas as pd


# Configuração inicial do Streamlit
st.set_page_config(
    page_title="Cientistas e Divulgação Científica: Opiniões e Práticas",
    layout="wide"
)

# Menu de Navegação entre as páginas
with st.sidebar:
    st.page_link("app.py", label="Página Inicial")
    st.page_link("pages/atividades.py", label="Atividades de Divulgação Científica")
    st.page_link("pages/opinioes_ct.py", label="Opiniões sobre Ciência e Tecnologia")
    st.page_link("pages/opinioes_dc.py", label="Opiniões sobre Divulgação Científica")
    st.page_link("pages/motivacoes.py", label="Motivações e Obstáculos")
    st.page_link("pages/sociodemografico.py", label="Perfil Sociodemográfico")

st.title("Opiniões sobre Divulgação Científica")	

tabs = st.tabs(["Modelos", "Importância", "Públicos"])

with tabs[0]:
    st.subheader("As afirmações que seguem contêm várias posições que podem ter consequências para a comunicação entre a ciência e o público. Qual a sua opinião sobre cada afirmação?")
    plot_bar_chart_facets(df, varmap, prefix='odc1', ordered_categories=None, title='', height=800)

    # Gráfico de mosaico
    with st.container(border=True):
        render_dashboard(df, 
                         varmap, 
                         varset1=codigo_variaveis, 
                         varset2="odc1[SQ", 
                         ordered_categories2=["Concordo totalmente", "Concordo em parte", "Discordo em parte", "Discordo totalmente", "Não sei"][::-1],
                         key="1",
                         pills1="Variável Sociodemográfica",
                         pills2="Opinião",
                         width=1000)

with tabs[1]:
    st.subheader("Considerando todas as atividades do seu trabalho, que importância você atribui à comunicação com o público não-especialista?")

    # Gráfico de barras
    # Contar a frequência de cada valor na coluna 'odc2'
    odc2_counts = df['odc2'].value_counts().reset_index()
    odc2_counts.columns = ['Valores', 'Frequência']

    # Criar o gráfico de barras
    fig = px.bar(odc2_counts, x='Valores', y='Frequência', title='')
    fig.update_layout(xaxis_title='', yaxis_title='')
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de mosaico
    with st.container(border=True):
        st.subheader("Selecione uma variável sociodemográfica.")
        valor_selecionado = st.pills("Variável Sociodemográfica", list(codigo_variaveis.values()), default=None)
        if valor_selecionado:
            key = [key for key, value in codigo_variaveis.items() if value == valor_selecionado][0]
            ordered_categories = ["Muito importante", "Importante", "Pouco importante", "Nada importante", "Não sei"][::-1]
            df.odc2 = pd.Categorical(df.odc2, categories=ordered_categories, ordered=True)
            # Gráfico de mosaico
            p, fig_mosaic, num_rows = plot_mosaic_with_residuals(df, 
                                                    var1="odc2", 
                                                    var2=key,
                                                    ordered_categories=ordered_categories,
                                                    # title=f"Visão da ciência brasileira entre os respondentes segundo {valor_selecionado}",
                                                    figsize=(7, 5))
            
            buf = BytesIO()
            fig_mosaic.savefig(buf, format="png", bbox_inches="tight", dpi=100)
            buf.seek(0)

            st.image(buf, width=1000)

with tabs[2]:
    st.subheader("Considerando o seu trabalho atual, qual importância você atribui à comunicação com os seguintes públicos não especialistas:")
    # Gráfico de barras
    odc3_columns = [col for col in df.columns if col.startswith('odc3')]
    odc3_counts = df[odc3_columns].apply(pd.Series.value_counts).fillna(0).reset_index()
    odc3_counts = odc3_counts.melt(id_vars='index', var_name='Variável', value_name='Frequência')
    odc3_counts.columns = ['Valores', 'Variável', 'Frequência']

    ordered_categories = ["Muito importante", "Importante", "Um pouco importante", "Nada importante", "Não sei"][::-1]
    odc3_counts['Valores'] = pd.Categorical(odc3_counts['Valores'], categories=ordered_categories, ordered=True)
    odc3_counts = odc3_counts.sort_values('Valores')

    fig = px.bar(odc3_counts, 
                 y='Valores', 
                 x='Frequência', 
                 facet_col='Variável', 
                 facet_col_wrap=2, 
                 title='',
                 height=800)
    fig.for_each_annotation(lambda a: a.update(
    text=f"<b>{'<br>'.join(' '.join(varmap[a.text.split('=')[1]].split(' ')[i:i+18]) for i in range(0, len(varmap[a.text.split('=')[1]].split(' ')), 18))}</b>"
    ))

    # Remover títulos dos eixos x e y em todos os facets
    fig.update_xaxes(title_text='')  # Remove título do eixo x e mantém os rótulos
    fig.update_yaxes(title_text='')  # Remove título do eixo y e mantém os rótulos

    fig.update_layout(xaxis_title='', 
                      yaxis_title='',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de mosaico
    with st.container(border=True):
        valor_selecionado = st.pills("Variável Sociodemográfica", list(codigo_variaveis.values()), default=None, key='valor_selecionado2')
        tema_selecionado = st.pills("Tipo de público", [varmap[key] for key in varmap if key.startswith("odc3[SQ")], default=None, key='publico_selecionado')
        if valor_selecionado and tema_selecionado:
            key = [key for key, value in codigo_variaveis.items() if value == valor_selecionado][0]
            var1 = [key for key, value in varmap.items() if value == tema_selecionado][0]
            ordered_categories = ["Muito importante", "Importante", "Um pouco importante", "Nada importante", "Não sei"][::-1]
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



st.markdown("---")
st.markdown("Dashboard desenvolvido por [Marcelo Pereira](https://marcelo-pereira.notion.site/)")