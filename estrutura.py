import pandas as pd
import streamlit as st
import plotly.express as px
from io import BytesIO
from graphs import plot_mosaic_with_residuals
from data_process import categories

def plot_bar_chart_facets(df, varmap, prefix='odc1', ordered_categories=None, title='', height=800):
    if ordered_categories is None:
        ordered_categories = ["Concordo totalmente", "Concordo em parte", "Discordo em parte", "Discordo totalmente", "Não sei"][::-1]

    columns = [col for col in df.columns if col.startswith(prefix)]
    counts = df[columns].apply(pd.Series.value_counts).fillna(0).reset_index()
    counts = counts.melt(id_vars = "index", var_name='Pergunta', value_name='Contagem')
    counts.columns = ['Resposta', 'Pergunta', 'Contagem']
    counts = counts.sort_values('Contagem')
    counts['Resposta'] = pd.Categorical(counts['Resposta'], categories=ordered_categories, ordered=True)


    fig = px.bar(counts, 
                 x='Contagem', 
                 y='Resposta', 
                 facet_col='Pergunta', 
                 facet_col_wrap=2, 
                 title=title,
                 height=height)
    fig.for_each_annotation(lambda a: a.update(
        text=f"<b>{'<br>'.join(' '.join(varmap[a.text.split('=')[1]].split(' ')[i:i+18]) for i in range(0, len(varmap[a.text.split('=')[1]].split(' ')), 18))}</b>"
    ))

    fig.update_xaxes(title_text='')  # Remove título do eixo x e mantém os rótulos
    fig.update_yaxes(title_text='')  # Remove título do eixo y e mantém os rótulos

    fig.update_layout(xaxis_title='', 
                      yaxis_title='',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

# Example usage
# plot_bar_chart(df, varmap)

def plot_bar_chart(df, column, ordered_categories=None, title='', height=800, categorical=True, orientation='h'):
    if categorical:
        if ordered_categories is None:
            ordered_categories = ["Concordo totalmente", "Concordo em parte", "Discordo em parte", "Discordo totalmente", "Não sei"][::-1]

        counts = df[column].value_counts().reindex(ordered_categories).fillna(0).reset_index()
        counts.columns = ['Valores', 'Frequência']
        counts['Valores'] = pd.Categorical(counts['Valores'], categories=ordered_categories, ordered=True)
        counts = counts.sort_values('Valores')
    else:
        counts = df[column].value_counts().reset_index()
        counts.columns = ['Valores', 'Frequência']

    fig = px.bar(counts, 
                 x='Valores', 
                 y='Frequência', 
                 title=title,
                 height=height,
                 orientation=orientation)
    
    fig.update_xaxes(title_text='')  # Remove título do eixo x e mantém os rótulos
    fig.update_yaxes(title_text='')  # Remove título do eixo y e mantém os rótulos

    fig.update_layout(xaxis_title='', 
                      yaxis_title='',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

# Example usage
# plot_bar_chart(df, 'column_name', categorical=True)

def plot_bar_chart_simplecounts(df, prefix, varmap, title='', height=800):
    columns = [col for col in df.columns if col.startswith(prefix)]
    counts = df[columns].apply(lambda x: x == "Sim").sum().reset_index()
    counts.columns = ['Pergunta', 'Contagem']
    counts['Pergunta'] = counts['Pergunta'].map(varmap)
    counts = counts.sort_values('Contagem', ascending=True)


    # Criar o gráfico de barras horizontal
    fig = px.bar(counts, 
                x='Contagem', 
                y='Pergunta', 
                orientation='h', 
                title='')

    # Atualizar os rótulos dos eixos
    fig.update_layout(xaxis_title='Frequência', yaxis_title='Variável')
    
    fig.update_xaxes(title_text='')  # Remove título do eixo x e mantém os rótulos
    fig.update_yaxes(title_text='')  # Remove título do eixo y e mantém os rótulos

    fig.update_layout(xaxis_title='', 
                      yaxis_title='',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)
    


def render_dashboard(df, varmap, varset1, varset2, key="", pills1 = "", pills2 = "", width=1000):

    default1 = list(varset1.values())[0]

    if isinstance(varset2, dict):
        default2 = list(varset2.values())[0]
    else:
        default2 = [value for key, value in varmap.items() if key.startswith(varset2)][0]

    valor_selecionado = st.pills(pills1, list(varset1.values()), default=default1, key=f'valor_selecionado_dashboard{key}')
    
    if isinstance(varset2, dict):
        tema_selecionado = st.pills(pills2, list(varset2.values()), default=default2, key=f'tema_selecionado_dashboard{key}')
    else:
        tema_selecionado = st.pills(pills2, [varmap[key] for key in varmap if key.startswith(varset2)], default=default2, key=f'tema_selecionado_dashboard{key}')
    
    if valor_selecionado == tema_selecionado:
        st.error("Selecione valores diferentes para as variáveis.")
        return

    if not valor_selecionado and not tema_selecionado:
        st.error("Selecione um valor e um tema para visualizar o dashboard.")
    
    elif valor_selecionado and tema_selecionado:
        if isinstance(varset2, dict):
            var2 = [key for key, value in varset2.items() if value == tema_selecionado][0]
        elif isinstance(varset2, str):
            var2 = [key for key, value in varmap.items() if value == tema_selecionado][0]

        var1 = [key for key, value in varset1.items() if value == valor_selecionado][0]

    if var1.startswith("MO01") or var1.startswith("MO02"):
        ordered_categories = ["Sim", "Não"]
        df[var1] = pd.Categorical(df[var1], categories=ordered_categories, ordered=True)
    elif var2.startswith("MO01") or var2.startswith("MO02"):
        ordered_categories = ["Sim", "Não"]
        df[var2] = pd.Categorical(df[var2], categories=ordered_categories, ordered=True)
    else:
        # ordenar as categorias
        df[var1] = pd.Categorical(df[var1], categories=categories[var1], ordered=True)
        df[var2] = pd.Categorical(df[var2], categories=categories[var2], ordered=True)

    # Gráfico de mosaico
    fig_mosaic, num_rows = plot_mosaic_with_residuals(df, 
                                            var1=var1, 
                                            var2=var2,
                                            figsize=(12, 10))
    
    buf = BytesIO()
    fig_mosaic.savefig(buf, format="png", bbox_inches="tight", dpi=100)
    buf.seek(0)

    st.image(buf, width=width)

# Example usage
# ordered_categories = ["Concordo totalmente", "Concordo em parte", "Discordo em parte", "Discordo totalmente", "Não sei"][::-1]
# render_dashboard(df, varmap, codigo_variaveis, ordered_categories, prefix='odc1')

def explicacao_mosaico():
    with st.expander("O que é um gráfico de mosaico?"):
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
