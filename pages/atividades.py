import streamlit as st
import pickle
from data_process import varmap, codigo_variaveis, df, ordered_categories, ordered_activities, dff_freq, codigo_atividades, tabela_estilizada
import plotly.express as px
from graphs import plot_mosaic_with_residuals
from io import BytesIO
from estrutura import plot_bar_chart_facets, plot_bar_chart, render_dashboard, define_categories
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

# Carregar o mapeamento de variáveis
with open("varmap.pkl", "rb") as f:
    varmap = pickle.load(f)

dict_atividades = {key: value for key, value in varmap.items() if "adc1[SQ" in key}
dict_variaveis = codigo_variaveis

tabs = st.tabs([
    "Frequência por Tipo de Atividade",
    "Mosaico da Atividade por Variáveis Sociodemográficas",
    "Relação com profissionais de divulgação científica",
                ])

# Aba 1: Frequência por Tipo de Atividade
with tabs[0]:
    # st.header("Frequência por Tipo de Atividade")

    st.subheader("Entre as seguintes atividades de divulgação científica, nos últimos 12 meses quantas vezes você...")

    # Gráfico de barras
    # Criar o gráfico com a ordem específica das atividades
    fig_freq = px.bar(
        dff_freq, 
        x='Atividade', 
        y='Contagem', 
        color='Frequência', 
        title='Distribuição das Respostas por Atividade',
        labels={'Contagem': 'Frequência', 'Atividade': 'Atividade'},
        category_orders={
            'Frequência': ordered_categories,  # Ordem das categorias de frequência
            'Atividade': ordered_activities    # Ordem das atividades
        }
    )
    st.plotly_chart(fig_freq, use_container_width=True)

    with st.container(border=True):
        st.subheader("Selecione uma atividade para ver em detalhe.")
        atividade_selecionada = st.pills("Atividade", list(codigo_atividades.values()), default=None)
        if atividade_selecionada:
            dff_filtrado = dff_freq[dff_freq['Atividade'] == atividade_selecionada]
            fig_filtrado = px.bar(
                dff_filtrado, 
                x='Frequência', 
                y='Contagem', 
                title=f'Distribuição das Respostas para a atividade "{atividade_selecionada}"',
                labels={'Contagem': '', 'Frequência': ''},
                category_orders={
                    'Frequência': ordered_categories  # Ordem das categorias de frequência
                }
            )
            st.plotly_chart(fig_filtrado, use_container_width=True)



    st.write("**Legenda das respostas**")
    dicionario = {
    'palestra público geral': 'Deu uma palestra pública num debate para o público em geral',
    'curso público externo': 'Participou de curso de formação a um público externo à sua Universidade ou instituto de pesquisa',
    'aula oficina escola básica': 'Deu uma aula ou oficina numa escola da Educação Básica',
    'comissão técnica ou conselho prof.': 'Participou em evento numa comissão técnica ou conselho profissional (exterior à Universidade ou instituto de pesquisa)',
    'Pint of Science': 'Participou de uma atividade do “Pint of Science”',
    'Dia Ciência Semana Nacional C&T': 'Participou de uma atividade do Dia da Ciência ou da Semana Nacional de Ciência e Tecnologia',
    'evento ONG movimento social': 'Participou em evento numa associação, ONG ou movimento social',
    'artigo revista público geral': 'Escreveu um artigo numa revista para o público em geral',
    'entrevista jornal revista público geral': 'Foi entrevistado para um jornal ou revista para o público em geral',
    'livro ou capítulo de divulgação': 'Escreveu um livro ou capítulo de livro de divulgação científica',
    'release programa TV rádio': 'Escreveu um release para a imprensa ou participou de um programa de TV ou rádio',
    'audiência pública': 'Participou de uma audiência pública no poder legislativo (Câmara, Assembléia, Congresso Nacional)',
    'visita guiada museu': 'Conduziu uma visita guiada num (ou em colaboração com um) museu',
    'programa mídias digitais': 'Participou de um programa em mídias digitais (blog, YouTube, podcast, live no Instagram, etc.)',
    'midias digitais canal próprio': 'Produziu conteúdo para seu canal próprio em mídias digitais (blog, YouTube, podcast, live no Instagram, etc.)'
    }
    # Criando uma lista de dicionários para a tabela
    tabela = []
    for chave, valor in dicionario.items():
        tabela.append({"Atividade": chave, "Descrição": valor})

    # Exibindo a tabela no Streamlit
    st.table(tabela)  # Ou use st.dataframe(tabela) para uma tabela interativa

# Aba 2: Mosaico da Atividade por Variáveis Sociodemográficas
with tabs[1]:
    st.header("Mosaico da Atividade por Variáveis Sociodemográficas")

    # Seleção de variáveis para o mosaico
    col1, col2 = st.columns(2)
    with col1:
        #st.subheader("Tipo de atividade")
        atividade_selected = st.pills("Tipo de atividade", list(codigo_atividades.values()), default="palestra público geral")
    with col2:
        #st.subheader("Variável sociodemográfica")
        variavel_selected = st.pills("Variável sociodemográfica", list(codigo_variaveis.values()), default="Ciencia_BasicaXAplicada")
    
    key_atividade = [key for key, value in codigo_atividades.items() if value == atividade_selected][0]
    key_variavel = [key for key, value in codigo_variaveis.items() if value == variavel_selected][0]
    
    # Gráfico de mosaico
    p, fig_mosaic, num_rows = plot_mosaic_with_residuals(df, 
                                            var1=key_atividade, 
                                            var2=key_variavel, 
                                            ordered_categories=ordered_categories,
                                            #title=f"Mosaico da relação entre {atividade_selected} e {variavel_selected}",
                                            figsize=(7, 5))
    
    buf = BytesIO()
    fig_mosaic.savefig(buf, format="png", bbox_inches="tight", dpi=100)
    buf.seek(0)

    st.image(buf, width=1000)

    with st.container(border=True):
        st.write(f"$N = {num_rows}$")
        if p < 0.05:
            st.write(f"Valor de $p = {p:.4f}$")
        else:
            st.write(f"Valor de $p = {p:.4f}$.  \nNão há significância estatística para o relacionamente entre as variáveis.")
    
    st.subheader("O que é um gráfico de mosaico?")
    st.write('''
        O gráfico de mosaico é uma forma de visualização de dados categóricos que exibe a relação entre duas variáveis.
        A altura de cada bloco é proporcional à frequência da atividade, enquanto a largura é proporcional à cada categoria 
        da variável sociodemográfica. Se a cor do bloco for diferente de cinza, isso indica que a correlação de Pearson entre a 
        atividade e a variável é significativa (p < 0,05). Assim, quanto mais vermelha significa que esta frequência é maior do que
        o esperado para aquela categoria, enquanto que azul significa que a frequência é menor do que o esperado.
        ''')
    
# Aba 3: Relação com profissionais de divulgação científica
with tabs[2]:
    st.subheader("Quando você conclui uma pesquisa, você entra em contato com a mídia para comunicar os resultados?")
    ordered_categories = ["Em geral, sim", 'Frequentemente', 'Raramente', 'Em geral, não', 'Não se aplica a mim']
    plot_bar_chart(df, 'adc2', ordered_categories=ordered_categories, orientation='v', height=400)
    st.subheader("No seu caso, qual importância tem os seguintes profissionais para a sua comunicação com o público não-especialista:")
    ordered_categories_adc3 = ["Muito importante", "Importante", "Pouco importante", "Nada importante", "Não sei"]
    plot_bar_chart_facets(df, varmap, prefix='adc3', ordered_categories=ordered_categories_adc3, height=600)
    st.subheader("Em geral, de que modo você é solicitado/a pela mídia?")
    ordered_categories_adc6 = ["Nunca", "Raramente", "Frequentemente", "Não se aplica a mim"]
    plot_bar_chart_facets(df, varmap, prefix="adc6", ordered_categories=ordered_categories_adc6, height=600)
    

st.markdown("---")
st.markdown("Dashboard desenvolvido por [Marcelo Pereira](https://marcelo-pereira.notion.site/)")