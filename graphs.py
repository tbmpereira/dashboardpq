import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.mosaicplot import mosaic
from scipy.stats import chi2_contingency
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pickle
from data_process import varmap

def plot_mosaic_with_residuals(df, var1, var2, figsize=(14, 12), title=None, xlabel=None, ylabel=None):
    """
    Plota um gráfico de mosaico com resíduos de Pearson coloridos (apenas se p < 0,05) e exibe o valor de p e a estatística de qui-quadrado.

    Parâmetros:
    -----------
    df : pd.DataFrame
        DataFrame contendo os dados.
    var1 : str
        Nome da primeira variável categórica (eixo x).
    var2 : str
        Nome da segunda variável categórica (eixo y).
    figsize : tuple, opcional
        Tamanho da figura (largura, altura). Padrão é (14, 10).
    title : str, opcional
        Título do gráfico. Se None, não adiciona título.
    xlabel : str, opcional
        Título do eixo x. Se None, não adiciona título.
    ylabel : str, opcional
        Título do eixo y. Se None, não adiciona título.

    Retorna:
    --------
    fig : matplotlib.figure.Figure
        Figura do gráfico de mosaico.
    num_rows : int
        Número de linhas do DataFrame usadas para calcular o mosaico.
    """
    # Carregar o mapeamento de categorias
    with open("categories.pkl", "rb") as f:
        categories = pickle.load(f)

    categories['CE14'] = ["Até 5 anos", "6 a 10 anos", "11 a 20 anos", "21 a 35 anos", "Acima de 35 anos"]
    
    # Verifica se as variáveis existem no DataFrame
    if var1 not in df.columns or var2 not in df.columns:
        raise ValueError(f"As variáveis {var1} ou {var2} não existem no DataFrame.")

    # Remove linhas com valores ausentes em var1 ou var2
    df_clean = df.dropna(subset=[var1, var2])

    # Verifica se há dados suficientes após a remoção de valores ausentes
    if df_clean.empty:
        raise ValueError("Não há dados suficientes após a remoção de valores ausentes.")

    # Reordenar var1 e var2 de acordo com as categorias definidas
    if var1 in categories:
        df_clean[var1] = pd.Categorical(df_clean.loc[:, var1], categories=categories[var1], ordered=True)
    if var2 in categories:
        df_clean[var2] = pd.Categorical(df_clean.loc[:, var2], categories=categories[var2], ordered=True)

    # Criar tabela de contingência
    contingency_table = pd.crosstab(df_clean[var1], df_clean[var2])

    # Verifica se a tabela de contingência está vazia
    if contingency_table.size == 0:
        raise ValueError("A tabela de contingência está vazia. Verifique os dados e as variáveis selecionadas.")

    # Verifica se há dados suficientes para o teste qui-quadrado
    if contingency_table.sum().sum() < 2:
        raise ValueError("Não há dados suficientes para realizar o teste qui-quadrado.")

    # Calcular o teste de qui-quadrado e obter os resíduos de Pearson
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    residuals = (contingency_table - expected) / np.sqrt(expected)

    # Número de linhas usadas para calcular o mosaico
    num_rows = contingency_table.sum().sum()

    def residual_color(key):
        if p < 0.05:  # Apenas aplica cores se houver significância estatística
            try:
                # Agora os índices do residuals são MultiIndex (var1, var2)
                value = residuals.loc[key]  
                color = plt.cm.coolwarm(value)
            except KeyError:
                color = 'lightgray'  # Cor padrão se a chave não for encontrada
        else:
            color = 'lightgray'  # Cor padrão se p > 0.05
        
        return {'color': color}

    # Criar uma nova figura com tamanho personalizado
    fig, ax = plt.subplots(figsize=figsize)


    # Criar o gráfico de mosaico
    mosaic(contingency_table.stack(),
           properties=residual_color, 
           ax=ax, 
           gap=0.02, 
           labelizer=lambda k: '')

    # Adicionar a legenda para as cores dos resíduos de Pearson (apenas se p < 0.05)
    if p < 0.05:
        sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=residuals.min().min(), vmax=residuals.max().max()))
        sm.set_array([])
        
        # Criar eixos insetos para a barra de cores
        axins = inset_axes(
                ax,
                width="2.5%",          # Largura da barra de cores (2.5% do espaço do gráfico)
                height="100%",
                loc='lower left',    # Ponto de ancoragem inicial
                bbox_to_anchor=(1.05, 0.0, 1, 1),  # Posição relativa ao gráfico principal (direita)
                bbox_transform=ax.transAxes,       # Sistema de coordenadas do Axes principal
                borderpad=0          # Espaçamento da borda
        )

        # Adicionar a barra de cores nos eixos insetos
        cbar = fig.colorbar(sm, cax=axins, orientation='vertical')
        cbar.set_label('Residual de Pearson')

        # Adicionar o valor de p abaixo da barra de cores
        ax.text(1.1, -0.1, f'p = {p:.4f}', transform=ax.transAxes, fontsize=12, verticalalignment='top')

    # Ajustar os rótulos do eixo x
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=70)

    # Adicionar títulos aos eixos x e y
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=14, labelpad=20)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=14)

    # Adicionar título ao gráfico, se fornecido
    if title:
        ax.set_title(title, fontsize=16)

    # Ajustar o layout para evitar sobreposição
    plt.tight_layout()

    return fig, num_rows
