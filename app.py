import streamlit as st

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

# Título do dashboard
st.title("Cientistas e Divulgação Científica: Opiniões e Práticas")

# Abas

tabs = st.tabs([
    "Sobre a Pesquisa",
    "Questionário",
    "Contato",
                ])

# Aba 1: Sobre a Pesquisa
with tabs[0]:
    st.header("Sobre a Pesquisa")

    st.write('''
             Este painel de dados apresenta para o público os resultados do _survey_ online realizado com o objetivo de entender as percepções e opiniões dos
             cientistas brasileiros em relação à divulgação científica. A pesquisa focou em bolsistas de produtividade em pesquisa (PQ) do Conselho Nacional de 
             Desenvolvimento Científico e Tecnológico (CNPq), uma população conhecida por sua alta atividade na produção científica.  \n
             Para navegar entre os resultados, utilize o menu lateral à esquerda. \n
             A coleta de informações foi feita a partir de um questionário online autoaplicado, que continha 51 perguntas organizadas em sete seções, abordando desde temas de interesse 
             e hábitos culturais até atividades de divulgação científica e opiniões sobre ciência e tecnologia na sociedade.  \n
             A coleta foi realizada entre janeiro e março de 2023, logo após o fim das medidas restritivas adotadas em função da pandemia de COVID-19. No total, foram 
             coletadas 1934 respostas. A amostra foi estratificada, garantindo que a distribuição dos respondentes fosse proporcional à distribuição dos bolsistas PQ 
             por área de conhecimento, sexo, região geográfica e categoria da bolsa PQ.  \n
             ''')
    
    st.write('''
             Outros estudos que exploram e analisam a mesma base de dados podem ser encontrados em:
            ''')
    st.write('''
            Pereira, M., Castelfranchi, Y., & Massarani, L. (2024). Científicos brasileños y divulgación científica: Una propuesta de clasificación. **Revista Iberoamericana De Ciencia, Tecnología Y Sociedad - CTS**. 
             Retrieved from https://ojs.revistacts.net/index.php/CTS/article/view/779  \n
            Pereira, M. **Ciência, sociedade, divulgação científica: a visão dos cientistas**. 2023. 167 p. Dissertação de Mestrado em Sociologia - Universidade Federal de Minas Gerais, 
             Belo Horizonte, 2023. http://hdl.handle.net/1843/55328
             ''')

# Aba 2: Questionário
with tabs[1]:
    st.header("Questionário")

    

# Aba 3: Contato
with tabs[2]:
    st.header("Contato")

    st.write(''':e-mail: [mapereira@ufmg.br](mailto:mapereira@ufmg.br)''')
    st.write('''Acesse o perfil do pesquisador no [ResearchGate](https://www.researchgate.net/profile/Marcelo-Pereira-44)''')

st.markdown("---")
st.markdown("Dashboard desenvolvido por [Marcelo Pereira](https://marcelo-pereira.notion.site/)")


