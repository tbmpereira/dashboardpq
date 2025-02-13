import streamlit as st
# from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px
import pickle
from graphs import plot_mosaic_with_residuals
from matplotlib import pyplot as plt
from data_process import df, varmap, ordered_categories, ordered_activities, dff_freq, tabela_estilizada, codigo_variaveis, codigo_atividades
from io import BytesIO

# Carregar o mapeamento de variáveis
with open("varmap.pkl", "rb") as f:
    varmap = pickle.load(f)

dict_atividades = {key: value for key, value in varmap.items() if "adc1[SQ" in key}
dict_variaveis = codigo_variaveis

# Configuração inicial do Streamlit
st.set_page_config(
    page_title="Atividade de divulgação científica de bolsistas produtividade CNPq",
    layout="wide"
)

# Título do dashboard
st.title("Atividade de divulgação científica de bolsistas produtividade CNPq")

# Abas

tabs = st.tabs([
    "Frequência por Tipo de Atividade",
    "Mosaico da Atividade por Variáveis Sociodemográficas",
    "Correlações entre Atividades e Variáveis Sociodemográficas",
    "Sobre a Pesquisa",
    "Metodologia",
    "Sobre o Autor"
                ])

# Aba 1: Frequência por Tipo de Atividade
with tabs[0]:
    st.header("Frequência por Tipo de Atividade")

    # Gráfico de barras
    # Criar o gráfico com a ordem específica das atividades
    fig_freq = px.bar(
        dff_freq, 
        x='Atividade', 
        y='Contagem', 
        color='Frequência', 
        title='Distribuição das Respostas por Atividade',
        labels={'Contagem': 'Frequência', 'Atividade': ''},
        category_orders={
            'Frequência': ordered_categories,  # Ordem das categorias de frequência
            'Atividade': ordered_activities    # Ordem das atividades
        }
    )
    st.plotly_chart(fig_freq, use_container_width=True)

# Aba 2: Mosaico da Atividade por Variáveis Sociodemográficas
with tabs[1]:
    st.header("Mosaico da Atividade por Variáveis Sociodemográficas")

    # Seleção de variáveis para o mosaico
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tipo de atividade")
        atividade_selected = st.radio("", list(codigo_atividades.values()))
    with col2:
        st.subheader("Variável sociodemográfica")
        variavel_selected = st.radio("", list(codigo_variaveis.values()))
    
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

# Aba 3: Correlações entre Atividades e Variáveis Sociodemográficas
with tabs[2]:
    st.header("Correlações entre Atividades e Variáveis Sociodemográficas")

    st.dataframe(tabela_estilizada)

    # st.write('''
    #     A tabela acima mostra o valor de p para o teste Qui-quadrado de independência entre cada atividade e variável sociodemográfica.
    #     Quando há significância estatística (p < 0,05), a célula é destacada em amarelo. Isso indica que a atividade e a variável de interesse
    #     estão correlacionadas.
    # ''')

# Aba 4: Sobre a Pesquisa
with tabs[3]:
    st.header("Sobre a Pesquisa")

    st.write('''
             Este survey online foi realizado com o objetivo de entender as percepções e opiniões dos cientistas brasileiros em relação à divulgação científica. 
             A pesquisa focou em bolsistas de produtividade em pesquisa (PQ) do Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq), uma população 
             conhecida por sua alta atividade na produção científica.  \n
             Para coletar as informações, foi elaborado um questionário online autoaplicado, que continha 51 perguntas organizadas em sete seções, abordando desde temas de interesse 
             e hábitos culturais até atividades de divulgação científica e opiniões sobre ciência e tecnologia na sociedade.  \n
             Os participantes foram convidados por e-mail. Apesar das limitações inerentes a métodos quantitativos, que podem não capturar a complexidade de algumas percepções, 
             o estudo busca oferecer insights significativos sobre as dinâmicas de comunicação científica entre cientistas e o público. Esse esforço é crucial para o 
             desenvolvimento de estratégias mais eficazes de divulgação da ciência, moldadas pela compreensão das opiniões e experiências dos próprios cientistas.
             ''')

# Aba 5: Metodologia
with tabs[4]:
    st.header("Metodologia")

# Aba 6: Sobre o Autor
with tabs[5]:
    st.header("Sobre o Autor")

st.markdown("---")
st.markdown("Dashboard desenvolvido por [Marcelo Pereira](https://marcelo-pereira.notion.site/)")

# # Sidebar com controles de filtro
# st.sidebar.header("Filtros")

# # Filtro de idade
# idade_range = st.sidebar.slider("Idade:", 20, 90, (20, 90))
# st.sidebar.write(f"Idade selecionada: {idade_range[0]} - {idade_range[1]}")

# # Filtro de sexo
# sexo_options = ["Masculino", "Feminino"]
# sexo_selected = st.sidebar.multiselect("Sexo:", sexo_options, default=sexo_options)

# # Filtro de cor/raça
# cores = sorted(list(df.CE04.unique())[1:])
# cor_selected = st.sidebar.multiselect("Cor/Raça:", cores, default=cores)

# # Filtro de ideologia política
# ideologias = sorted(list(df.CE07.unique())[1:])
# ideologia_selected = st.sidebar.multiselect("Ideologia Política:", ideologias, default=ideologias)

# # Filtro de produtividade
# produtividade_options = ["1A", "1B", "1C", "1D", "2", "Senior"]
# produtividade_selected = st.sidebar.multiselect("Produtividade:", produtividade_options, default=produtividade_options)

# # Filtro de grande área do conhecimento
# areas = sorted(list(df.CE11.unique())[1:])
# area_selected = st.sidebar.multiselect("Grande Área do Conhecimento:", areas, default=areas)

# # Filtro de região
# regiao_options = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
# regiao_selected = st.sidebar.multiselect("Região:", regiao_options, default=regiao_options)



