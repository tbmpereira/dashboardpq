import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.mosaicplot import mosaic
from scipy.stats import chi2_contingency
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def plot_mosaic_with_residuals(df, var1, var2, ordered_categories=None, figsize=(14, 10), title=None):
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
    ordered_categories : list, opcional
        Lista de categorias ordenadas para a variável `var1`. Se None, usa a ordem original.
    figsize : tuple, opcional
        Tamanho da figura (largura, altura). Padrão é (14, 10).
    title : str, opcional
        Título do gráfico. Se None, não adiciona título.

    Retorna:
    --------
    p : float
        Valor de p do teste de qui-quadrado.
    fig : matplotlib.figure.Figure
        Figura do gráfico de mosaico.
    num_rows : int
        Número de linhas do DataFrame usadas para calcular o mosaico.
    """
    # Verifica se as variáveis existem no DataFrame
    if var1 not in df.columns or var2 not in df.columns:
        raise ValueError(f"As variáveis {var1} ou {var2} não existem no DataFrame.")

    # Remove linhas com valores ausentes em var1 ou var2
    df_clean = df.dropna(subset=[var1, var2])

    # Verifica se há dados suficientes após a remoção de valores ausentes
    if df_clean.empty:
        raise ValueError("Não há dados suficientes após a remoção de valores ausentes.")

    # Reordenar a coluna var1, se necessário
    if ordered_categories is not None:
        df_clean.loc[:, var1] = pd.Categorical(df_clean[var1], categories=ordered_categories, ordered=True)
        df_clean = df_clean.sort_values(by=var1)  # Ordenar o DataFrame pela coluna var1

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
                # Tenta acessar o valor no DataFrame de resíduos
                value = residuals.loc[key[1], key[0]]
                # Mapeia o valor do residual para a cor (escala vermelho-azul)
                color = plt.cm.coolwarm(value)
            except KeyError:
                # Se a chave não existir, usa uma cor padrão (cinza)
                color = 'lightgray'
        else:
            # Cor padrão (cinza) quando não há significância
            color = 'lightgray'
        
        return {'color': color}

    # Criar uma nova figura com tamanho personalizado
    fig, ax = plt.subplots(figsize=figsize)

    # Criar o gráfico de mosaico
    mosaic(df_clean, [var2, var1], properties=residual_color, ax=ax, gap=0.02, labelizer=lambda k: '')

    # Adicionar a legenda para as cores dos resíduos de Pearson (apenas se p < 0,05)
    if p < 0.05:
        sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=residuals.min().min(), vmax=residuals.max().max()))
        sm.set_array([])
        
        # Criar eixos insetos para a barra de cores
        axins = inset_axes(
                ax,
                width="2.5%",          # Largura da barra de cores (5% do espaço do gráfico)
                height="100%",
                loc='lower left',    # Ponto de ancoragem inicial
                bbox_to_anchor=(1.05, 0.0, 1, 1),  # Posição relativa ao gráfico principal (direita)
                bbox_transform=ax.transAxes,       # Sistema de coordenadas do Axes principal
                borderpad=0          # Espaçamento da borda
        )

        # Adicionar a barra de cores nos eixos insetos
        cbar = fig.colorbar(sm, cax=axins, orientation='vertical')
        cbar.set_label('Residual de Pearson')

    # Ajustar os rótulos do eixo x
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    # Adicionar título ao gráfico, se fornecido
    if title:
        ax.set_title(title, fontsize=16)

    return p, fig, num_rows