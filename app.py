import streamlit as st
from PIL import Image
from estrutura import rodape

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

st.write("""
Este dashboard apresenta os resultados de um _survey_ realizado com cientistas sobre suas percepções e atividades de divulgação científica.
""")

# Abas

tabs = st.tabs([
    "Sobre a Pesquisa",
    "Questionário",
    "Gráfico de Mosaico",
    "Contato",
                ])

# Aba 1: Sobre a Pesquisa
with tabs[0]:
    st.markdown("## Sobre a Pesquisa")

    col1, col2 = st.columns([2, 1])
    with col1:

        st.write('''
                Esta pesquisa foi realizada com o objetivo de compreender as percepções e opiniões dos cientistas brasileiros em relação à divulgação científica. 
                Especificamente, convidamos para participar os bolsistas de produtividade em pesquisa (PQ) do Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq), 
                uma população conhecida por sua alta atividade na produção científica.  \n
                A coleta de informações foi feita a partir de um questionário _online_ autoaplicado, que continha 51 perguntas organizadas em sete seções, abordando desde temas de interesse 
                e hábitos culturais até atividades de divulgação científica e opiniões sobre ciência e tecnologia na sociedade.  \n
                A coleta foi realizada entre janeiro e março de 2023. No total, foram coletadas 1934 respostas, o que significa cerca de 12% da população de bolsistas PQ na época. 
                A amostragem foi feita de forma estratificada, garantindo que a distribuição dos 
                respondentes fosse proporcional à distribuição dos bolsistas PQ por área de conhecimento, sexo, região geográfica e categoria da bolsa PQ.  \n
                ''')
        
        st.markdown('''
                ### Para saber mais:
                ''')
        st.write('''
                Pereira, M., Castelfranchi, Y., & Massarani, L. (2024). Científicos brasileños y divulgación científica: Una propuesta de clasificación. **Revista Iberoamericana De Ciencia, Tecnología Y Sociedad - CTS**. 
                Retrieved from https://ojs.revistacts.net/index.php/CTS/article/view/779  \n
                Pereira, M. **Ciência, sociedade, divulgação científica: a visão dos cientistas**. 2023. 167 p. Dissertação de Mestrado em Sociologia - Universidade Federal de Minas Gerais, 
                Belo Horizonte, 2023. http://hdl.handle.net/1843/55328
                ''')
    
    with col2:
        image = Image.open("img/rosetta.png")
        # image_cropped = image.crop((0, 0, 400, 400))
        st.image(image, use_container_width=True)

# Aba 2: Questionário
with tabs[1]:
    st.header("Questionário")

    st.write('''
            Os dados que apresentamos aqui são de perguntas selecionadas de cinco das sete seções do questionário original. 
             Uma cópia do questionário completo pode ser baixada abaixo:
         ''')
    
    file_path = "dados/questionario.pdf"

    with open(file_path, "rb") as f:
        pdf = f.read()
    
    st.download_button(
        label = "Baixar Questionário Completo (PDF)",
        data = pdf,
        file_name="questionario.pdf",
        mime="application/pdf"
    )

    st.write('''
             Clique nos links abaixo para acessar os resultados de cada seção:
                ''')
    
    # Links rápidos para as páginas
    st.page_link("pages/atividades.py", label="Atividades de Divulgação Científica", icon="🏋️‍♀️")
    st.page_link("pages/opinioes_ct.py", label="Opiniões sobre Ciência e Tecnologia", icon="🔬")
    st.page_link("pages/opinioes_dc.py", label="Opiniões sobre Divulgação Científica", icon="🎙️")
    st.page_link("pages/motivacoes.py", label="Motivações e Obstáculos", icon="🚧")
    st.page_link("pages/sociodemografico.py", label="Perfil Sociodemográfico", icon="🙎‍♂️")

# Aba 3: Gráfico de Mosaico
with tabs[2]:
    st.markdown('''
            ### O que é um Gráfico de Mosaico?
            Um **gráfico de mosaico** é uma ferramenta visual usada para representar a relação entre duas variáveis categóricas.
            Ela divide um retângulo em subáreas proporcionais às frequências das categorias das variáveis. Cada "bloco" do mosaico representa uma 
            combinação de categorias, e o tamanho do bloco é proporcional à frequência daquela combinação.  \n
            #### O que são Resíduos de Pearson?
            Os **resíduos de Pearson** são uma medida estatística que ajuda a entender a diferença entre os valores observados e os valores esperados
            em uma tabela de contingência (uma tabela que cruza duas ou mais variáveis categóricas). Eles são calculados da seguinte forma:
        ''')
    st.latex(r'''
            \text{Resíduo de Pearson} = \frac{(\text{Observado} - \text{Esperado})}{\sqrt{\text{Esperado}}}
             ''')
                                                                   
    st.markdown('''
            Onde:
            - **Observado**: o valor real encontrado nos dados.  \n
            - **Esperado**: o valor esperado se não houvesse associação entre as variáveis (isto é, se fossem independentes).  \n
            Os resíduos de Pearson indicam se uma combinação de categorias ocorre com mais frequência do que o esperado (resíduo positivo) ou menos
            frequência do que o esperado (resíduo negativo).  \n
            ### Gráfico de Mosaico com Resíduos de Pearson
            Quando um gráfico de mosaico é colorido com base nos resíduos de Pearson, ele destaca as combinações de categorias que ocorrem com mais
            ou menos frequência do que o esperado.  \n
            #### Como funciona?
            - **Cor Vermelha**: combinações de categorias que ocorrem com mais frequência do que o esperado. (resíduo positivo) \n
            - **Cor Azul**: combinações de categorias que ocorrem com menos frequência do que o esperado. (resíduo negativo) \n
            - **Cor Cinza**: combinações de categorias que ocorrem com a frequência esperada.  \n
            #### Exemplo:
''')
    st.image("img/exemplo_mosaico.png", width=1000)
    st.markdown('''
            Neste exemplo, o gráfico de mosaico mostra a relação entre a frequência da atividade "palestras para o público geral" e se o científica
            atua principalmente com ciência básica ou aplicada. \n
            Assim, podemos perceber, por exemplo, que os cientistas que atuam principalmente com ciência aplicada dão mais palestras do que o esperado,
            e isto pode ser percebido pelas cores vermelhas das frequências maiores e pelas cores azuis das frequências menores.
            O contrário acontece com os cientistas que atuam principalmente com ciência básica.  \n
            A barra de cores ao lado do gráfico mostra a escala de resíduos de Pearson.  Com o valor de _p_ do teste _chi-quadrado_ exibido logo abaixo\n
            Valores de _p_ menores que 0.05 indicam que a associação entre as variáveis é estatisticamente significativa.  \n
            ''')


# Aba 4: Contato
with tabs[3]:
    st.header("Contato")

    st.write(''':e-mail: [mapereira@ufmg.br](mailto:mapereira@ufmg.br)''')
    st.write('''Acesse o perfil do pesquisador no [ResearchGate](https://www.researchgate.net/profile/Marcelo-Pereira-44)''')

rodape()


