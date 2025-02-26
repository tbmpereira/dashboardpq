import streamlit as st
from data_process import df, perguntas_socio, codigo_variaveis, varmap
from estrutura import plot_bar_chart, render_dashboard, explicacao_mosaico

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

st.title("Perfil Sociodemográfico")

variavel_selecionada = st.pills("Pergunta do Questionário", 
         list(perguntas_socio.values()), 
         default=None, 
         key='valor_selecionado_sociodemografico')

st.subheader("Distribuição das respostas")
if variavel_selecionada:
    column_name = [key for key, value in perguntas_socio.items() if value == variavel_selecionada][0]
    plot_bar_chart(df, column_name, categorical=False, orientation="v", height=400)

render_dashboard(df, 
                 varmap, 
                 codigo_variaveis, 
                 codigo_variaveis, 
                 key="1",
                 pills1="Primeira Variável",
                 pills2="Segunda Variável")
explicacao_mosaico()

st.markdown("---")
st.markdown("Dashboard desenvolvido por [Marcelo Pereira](https://marcelo-pereira.notion.site/)")