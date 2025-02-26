import streamlit as st
from estrutura import plot_bar_chart_facets, plot_bar_chart_simplecounts, render_dashboard, explicacao_mosaico
from data_process import df, varmap, codigo_variaveis

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

st.title("Motivações e Obstáculos")

tabs = st.tabs(["Motivações", "Obstáculos", "Formação e Eventos"])

with tabs[0]:
    st.subheader("Marque os elementos mais importantes que, para você pessoalmente, são uma motivação para comunicar seu trabalho a um público não-especialista:")
    st.write("Escolha no máximo 3 respostas")
    plot_bar_chart_simplecounts(df, "MO01", varmap)
    render_dashboard(df, 
                     varmap, 
                     varset1=codigo_variaveis, 
                     varset2='MO01',
                     key="MO1",
                     pills1="Variável Sociodemográfica",
                     pills2="Motivação")
    explicacao_mosaico()

with tabs[1]:
    st.subheader("Marque os elementos mais importantes que, para você pessoalmente, são um obstáculo para comunicar seu trabalho a um público não-especialista:")    
    st.write("Escolha no máximo 3 respostas")
    plot_bar_chart_simplecounts(df, "MO02", varmap)
    render_dashboard(df, 
                     varmap, 
                     varset1=codigo_variaveis, 
                     varset2='MO02', 
                     key="MO2",
                     pills1="Variável Sociodemográfica",
                     pills2="Obstáculo")
    explicacao_mosaico()

with tabs[2]:
    st.subheader("Você conhece ou participou de alguma destas iniciativas de formação em divulgação científica?")
    ordered_categories = ["Não conheço", "Conheço mas não participei", "Participei como aluno", "Participei como docente"]
    plot_bar_chart_facets(df, varmap, "MO04", ordered_categories=ordered_categories)
    ordered_categories2 = ["Conheço mas não participei", "Participei como aluno", "Participei como docente", "Não conheço"]
    render_dashboard(df, 
                     varmap, 
                     varset1=codigo_variaveis,
                     varset2='MO04',
                     key="MO4",
                     pills1="Variável Sociodemográfica",
                     pills2="Formação")
    explicacao_mosaico()

st.markdown("---")
st.markdown("Dashboard desenvolvido por [Marcelo Pereira](https://marcelo-pereira.notion.site/)")