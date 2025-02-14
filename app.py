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
    st.page_link("pages/opinioes_dc.py", label="Opiniãos sobre Divulgação Científica")
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
             Este _survey_ online foi realizado com o objetivo de entender as percepções e opiniões dos cientistas brasileiros em relação à divulgação científica. 
             A pesquisa focou em bolsistas de produtividade em pesquisa (PQ) do Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq), uma população 
             conhecida por sua alta atividade na produção científica.  \n
             Para coletar as informações, foi elaborado um questionário online autoaplicado, que continha 51 perguntas organizadas em sete seções, abordando desde temas de interesse 
             e hábitos culturais até atividades de divulgação científica e opiniões sobre ciência e tecnologia na sociedade.  \n
             Os participantes foram convidados por e-mail. Apesar das limitações inerentes a métodos quantitativos, que podem não capturar a complexidade de algumas percepções, 
             o estudo busca oferecer _insights_ significativos sobre as dinâmicas de comunicação científica entre cientistas e o público. Esse esforço é crucial para o 
             desenvolvimento de estratégias mais eficazes de divulgação da ciência, moldadas pela compreensão das opiniões e experiências dos próprios cientistas.
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

st.markdown("---")
st.markdown("Dashboard desenvolvido por [Marcelo Pereira](https://marcelo-pereira.notion.site/)")


