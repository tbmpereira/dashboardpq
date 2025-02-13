import pandas as pd
import pickle
import re
from scipy.stats import chi2_contingency

# Carregar os dados
df = pd.read_csv("data_tratado.csv")

# Carregar o mapeamento de variáveis
with open("varmap.pkl", "rb") as f:
    varmap = pickle.load(f)

# Aplicar a transformação de categorias ordenadas a todas as colunas que começam com 'adc1'

ordered_categories = ['Nenhuma vez', '1 vez', '2 vezes', '3 vezes', '4 vezes', '5 vezes', 'mais de 5 vezes']

dff = df.copy()

for col in dff.columns:
    if col.startswith('adc1'):
        dff.loc[:, col] = pd.Categorical(dff.loc[:, col], categories=ordered_categories, ordered=True)

# Exemplo de agregação dos dados
dff_melted = dff.melt(value_vars=[col for col in dff.columns if col.startswith('adc1')], 
                    var_name='Atividade', value_name='Frequência')


dff_melted['Atividade'] = dff_melted['Atividade'].map(varmap)

dff_freq = dff_melted.groupby(['Atividade', 'Frequência']).size().reset_index(name='Contagem')

# Garantir que a coluna 'Frequência' seja categórica e ordenada
dff_freq['Frequência'] = pd.Categorical(
    dff_freq['Frequência'], 
    categories=ordered_categories, 
    ordered=True
)

# Ordenar o DataFrame com base nas categorias
dff_freq = dff_freq.sort_values(['Atividade', 'Frequência'])

# Calcular a soma das contagens para "Nenhuma vez" em cada atividade
order_by_nenhuma_vez = (
    dff_freq[dff_freq['Frequência'] == 'Nenhuma vez']
    .set_index('Atividade')['Contagem']
    .sort_values(ascending=False)
)

# Ordenar as atividades com base na ordem decrescente de "Nenhuma vez"
ordered_activities = order_by_nenhuma_vez.index.tolist()

atividades = [value for key, value in varmap.items() if "adc1[SQ" in key]

variaveis_demograficas =  {key:value for key, value in varmap.items() if "CE" in key}

# Converter a variável CE14 para faixas de idade

def extrair_dois_primeiros_numeros(entrada):
    """
    Extrai os dois primeiros números inteiros de uma string.
    Se houver caracteres não numéricos entre os dígitos, retorna apenas o primeiro número.
    
    Parâmetros:
    -----------
    entrada : str
        A string de entrada que pode conter números e texto.
    
    Retorna:
    --------
    int or None
        Retorna os dois primeiros números consecutivos como um inteiro, 
        ou apenas o primeiro número se houver caracteres não numéricos entre eles.
        Retorna None se não houver números.
    """
    # Encontra todos os números na string
    numeros = re.findall(r'\d+', entrada)
    
    if numeros:
        # Se houver mais de um número, verifica se estão consecutivos na string original
        if len(numeros) >= 2:
            # Encontra as posições dos dois primeiros números na string
            primeiro_num = numeros[0]
            segundo_num = numeros[1]
            
            # Verifica se os dois primeiros números estão consecutivos
            posicao_primeiro = entrada.find(primeiro_num)
            posicao_segundo = entrada.find(segundo_num)
            
            # Se houver caracteres não numéricos entre os dois números, retorna apenas o primeiro
            if posicao_segundo > posicao_primeiro + len(primeiro_num):
                return int(primeiro_num)
            else:
                # Retorna os dois primeiros números consecutivos
                return int(primeiro_num + segundo_num)
        else:
            # Retorna o primeiro número se houver apenas um
            return int(numeros[0])
    else:
        return None  # Retorna None se não houver números
    
ce14_processado = df['CE14'].apply(extrair_dois_primeiros_numeros)

def classificar_vinculo(idade):
    if idade <= 5:
        return "Ingressantes"
    elif idade <= 10:
        return "Jovens acadêmicos"
    elif idade <= 20:
        return "Meia carreira"
    elif idade <= 35:
        return "Sêniores"
    else:
        return "Veteranos"
    
ce14_faixas = ce14_processado.apply(classificar_vinculo)

df['CE14'] = ce14_faixas

def criar_tabela_valores_p(df, atividades, variaveis_sociodemograficas):
    """
    Cria uma tabela de valores de p para todas as combinações de atividades e variáveis sociodemográficas.
    
    Parâmetros:
    -----------
    df : pd.DataFrame
        DataFrame contendo os dados.
    atividades : list
        Lista das colunas que representam as atividades.
    variaveis_sociodemograficas : list
        Lista das colunas que representam as variáveis sociodemográficas.
    
    Retorna:
    --------
    pd.DataFrame
        Tabela de valores de p, com atividades nas linhas e variáveis sociodemográficas nas colunas.
    """
    # Inicializar um DataFrame vazio para armazenar os valores de p
    tabela_p = pd.DataFrame(index=atividades, columns=variaveis_sociodemograficas)
    
    # Calcular o valor de p para cada combinação de atividade e variável sociodemográfica
    for atividade in atividades:
        for variavel in variaveis_sociodemograficas:
            # Criar tabela de contingência
            tabela_contingencia = pd.crosstab(df[atividade], df[variavel])
            
            # Calcular o teste qui-quadrado
            try:
                chi2, p, dof, expected = chi2_contingency(tabela_contingencia)
            except ValueError:
                # Caso haja erro (por exemplo, tabela de contingência com zeros)
                p = None
            
            # Armazenar o valor de p na tabela
            tabela_p.loc[atividade, variavel] = p
    
    return tabela_p

def destacar_p_significativo(valor_p):
    """
    Retorna um estilo CSS para destacar valores de p significativos.
    """
    if isinstance(valor_p, float) and valor_p < 0.05:
        return 'background-color: yellow; color: black;'
    return ''

codigo_atividades = {key:value for key, value in varmap.items() if "adc1[SQ" in key}
codigo_variaveis = {
    'CE02': 'Sexo',
    'CE03': 'Escolaridade_Mae',
    'CE04': 'Cor_Raca',
    'CE05': 'Religiao',
    'CE06': 'Importancia_Religiao',
    'CE10': 'Ciencia_BasicaXAplicada',
    'CE07': 'Orientacao_Politica',
    'CE08': 'Nivel_Bolsa_CNPq',
    'CE11': 'GdeArea_CNPq',
    'CE13': 'Regiao_Geografica',
    'CE14': 'Tempo_Vinculo'
}

# Criar a tabela de valores de p
tabela_p = criar_tabela_valores_p(df, codigo_atividades, codigo_variaveis)

# Renomear index e colunas de tabela_p
# tabela_p.index = [varmap[codigo] for codigo in codigo_atividades]
# tabela_p.columns = [codigo_variaveis[codigo] for codigo in codigo_variaveis]

# Aplicar estilos condicionais
# tabela_estilizada = tabela_p.style.map(destacar_p_significativo)