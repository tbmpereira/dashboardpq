import streamlit as st
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter, default_converter
import tempfile
from PIL import Image

# Ativar o conversor padrão
with localconverter(default_converter):
    # Título do aplicativo Streamlit
    st.title("Dashboard PQ - Gráfico de Mosaico")

    # Definir o diretório de trabalho no R
    robjects.r('''
        setwd("E:/Dashboard PQ")
    ''')

    # Carregar pacotes R
    base = importr("base")
    tidyverse = importr("tidyverse")
    vcd = importr("vcd")
    jsonlite = importr("jsonlite")

    # Carregar o script R
    robjects.r('''
        source("testes_mosico.R")
    ''')

    # Função para gerar o gráfico de mosaico
    def gerar_mosaico(var1, var2):
        # Executar a função R para gerar o gráfico
        robjects.r(f'''
            png(tempfile(), width = 800, height = 600)
            grafico_mosaico(data, "{var1}", "{var2}")
            dev.off()
        ''')

        # Capturar o gráfico salvo em um arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        temp_file.close()
        robjects.r(f'''
            png("{temp_file.name}", width = 800, height = 600)
            grafico_mosaico(data, "{var1}", "{var2}")
            dev.off()
        ''')

        # Exibir o gráfico no Streamlit
        image = Image.open(temp_file.name)
        st.image(image, caption=f"Gráfico de Mosaico: {var1} vs {var2}")

    # Carregar as variáveis disponíveis
    variaveis = robjects.r('''
        names(data)
    ''')

    # Widgets para selecionar var1 e var2
    var1 = st.selectbox("Selecione a primeira variável (var1):", variaveis)
    var2 = st.selectbox("Selecione a segunda variável (var2):", variaveis)

    # Botão para gerar o gráfico
    if st.button("Gerar Gráfico"):
        st.write(f"Gerando gráfico de mosaico para {var1} vs {var2}...")
        gerar_mosaico(var1, var2)