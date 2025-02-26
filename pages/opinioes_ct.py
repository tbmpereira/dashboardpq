import streamlit as st
import plotly.express as px
from data_process import df, codigo_variaveis, varmap, categories
from graphs import plot_mosaic_with_residuals
from io import BytesIO
import pandas as pd
from estrutura import explicacao_mosaico

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

st.title("Opiniões sobre Ciência e Tecnologia")

tabs = st.tabs(["Visão da Ciência Brasileira", "Riscos e Benefícios da Ciência", "Temas de preocupação", "Gestão da Política de C&T"])

with tabs[0]:
    st.subheader("Se você fosse colocar a ciência brasileira num cenário mundial, você diria que ela se encontra atualmente em um nível...")

    # Gráfico de barras
    # Contar a frequência de cada valor na coluna 'octs1'
    octs1_counts = df['octs1'].value_counts().reset_index()
    octs1_counts.columns = ['Valores', 'Frequência']

    # Criar o gráfico de barras
    fig = px.bar(octs1_counts, x='Valores', y='Frequência', title='')
    fig.update_layout(xaxis_title='', yaxis_title='')
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de mosaico
    with st.container(border=True):
        st.subheader("Selecione uma variável sociodemográfica.")
        valor_selecionado = st.pills("Variável Sociodemográfica", list(codigo_variaveis.values()), default=None)
        if valor_selecionado:
            key = [key for key, value in codigo_variaveis.items() if value == valor_selecionado][0]
            ordered_categories = ["Atrasado", "Intermediário", "Avançado"]
            df.octs1 = pd.Categorical(df.octs1, categories=ordered_categories, ordered=True)
            # Gráfico de mosaico
            fig_mosaic, num_rows = plot_mosaic_with_residuals(df, 
                                                    var1="octs1", 
                                                    var2=key,
                                                    xlabel=valor_selecionado,
                                                    ylabel="Visão da Ciência Brasileira",
                                                    figsize=(12, 10))
            
            buf = BytesIO()
            fig_mosaic.savefig(buf, format="png", bbox_inches="tight", dpi=100)
            buf.seek(0)

            st.image(buf, width=1000)

            explicacao_mosaico()

with tabs[1]:
#    with col1:
    st.subheader('''Vamos agora falar sobre os riscos e os benefícios da pesquisa científica. Em sua opinião, a ciência traz para a humanidade...''')
    # Gráfico de barras
    # Contar a frequência de cada valor na coluna 'octs2'
    octs2_counts = df['octs2'].value_counts().reset_index()
    octs2_counts.columns = ['Valores', 'Frequência']

    # Criar o gráfico de barras
    fig_beneficios = px.bar(octs2_counts, x='Valores', y='Frequência', title='')
    fig_beneficios.update_layout(xaxis_title='', yaxis_title='')
    st.plotly_chart(fig_beneficios, use_container_width=True, key='beneficios')

#    with col2:
    st.subheader('''E em sua opinião, a ciência traz para a humanidade...''')
    # Gráfico de barras
    # Contar a frequência de cada valor na coluna 'octs3'
    octs3_counts = df['octs3'].value_counts().reindex(["Muitos riscos", "Alguns riscos", "Poucos riscos", "Nenhum risco"]).reset_index()
    octs3_counts.columns = ['Valores', 'Frequência']

    # Criar o gráfico de barras
    fig_maleficios = px.bar(octs3_counts, x='Valores', y='Frequência', title='')
    fig_maleficios.update_layout(xaxis_title='', yaxis_title='')
    st.plotly_chart(fig_maleficios, use_container_width=True, key='maleficios')

    # Gráfico de mosaico
    with st.container(border=True):
        st.subheader("Selecione uma variável sociodemográfica.")
        riscos_beneficios = st.pills("Riscos e Benefícios", ["Benefícios", "Riscos"], default=None, key='riscos_beneficios')
        variavel_selecionado = st.pills("Variável sociodemográfica", list(codigo_variaveis.values()), default=None, key='variavel_selecionado')
        if variavel_selecionado and riscos_beneficios:
            key = [key for key, value in codigo_variaveis.items() if value == variavel_selecionado][0]
            if riscos_beneficios == "Benefícios":
                ordered_categories = ["Muitos benefícios", "Alguns benefícios", "Poucos benefícios", "Nenhum benefício"]
                var1 = "octs2"
                df.octs2 = pd.Categorical(df.octs2, categories=ordered_categories, ordered=True)
            else:
                ordered_categories = ["Muitos riscos", "Alguns riscos", "Poucos riscos", "Nenhum risco"]
                var1 = "octs3"
                df.octs3 = pd.Categorical(df.octs3, categories=ordered_categories, ordered=True)
            
            # Gráfico de mosaico
            fig_mosaic, num_rows = plot_mosaic_with_residuals(df, 
                                                    var1=key, 
                                                    var2=var1,
                                                    xlabel=variavel_selecionado,
                                                    ylabel=riscos_beneficios,
                                                    figsize=(12, 10))
            
            buf = BytesIO()
            fig_mosaic.savefig(buf, format="png", bbox_inches="tight", dpi=100)
            buf.seek(0)

            st.image(buf, width=1000)

            explicacao_mosaico()
    
with tabs[2]:
    st.subheader("Entre os temas a seguir, que despertaram algum grau de preocupação na opinião pública, o quanto você está preocupado, como cidadão, com...")

    # Gráfico de barras
    octs6_columns = [col for col in df.columns if col.startswith('octs6')]
    octs6_counts = df[octs6_columns].apply(pd.Series.value_counts).fillna(0).reset_index()
    octs6_counts = octs6_counts.melt(id_vars='index', var_name='Variável', value_name='Frequência')
    octs6_counts.columns = ['Valores', 'Variável', 'Frequência']

    ordered_categories = ["Extremamente preocupado", "Muito preocupado", "Preocupado", "Nada preocupado", "Não sei"][::-1]
    octs6_counts['Valores'] = pd.Categorical(octs6_counts['Valores'], categories=ordered_categories, ordered=True)
    octs6_counts = octs6_counts.sort_values('Valores')

    fig = px.bar(octs6_counts, 
                 y='Valores', 
                 x='Frequência', 
                 facet_col='Variável', 
                 facet_col_wrap=2, 
                 title='',
                 height=800)
    fig.for_each_annotation(lambda a: a.update(text=f"<b>{varmap[a.text.split('=')[1]]}</b>"))  # Título em negrito

    # Remover títulos dos eixos x e y em todos os facets
    fig.update_xaxes(title_text='', showticklabels=True)  # Remove título do eixo x e mantém os rótulos
    fig.update_yaxes(title_text='', showticklabels=True)  # Remove título do eixo y e mantém os rótulos

    # Remove y ticks in the second column of facets
    for i in range(1, len(fig.data), 2):
        fig.update_yaxes(showticklabels=False, row=(i // 2) + 1, col=2)

    fig.update_layout(xaxis_title='', 
                      yaxis_title='',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de mosaico
    with st.container(border=True):
        valor_selecionado = st.pills("Variável Sociodemográfica", list(codigo_variaveis.values()), default=None, key='valor_selecionado')
        tema_selecionado = st.pills("Tema", [varmap[key] for key in varmap if key.startswith("octs6[SQ")], default=None, key='tema_selecionado')
        if valor_selecionado and tema_selecionado:
            key = [key for key, value in codigo_variaveis.items() if value == valor_selecionado][0]
            var1 = [key for key, value in varmap.items() if value == tema_selecionado][0]
            ordered_categories = ["Extremamente preocupado", "Muito preocupado", "Preocupado", "Nada preocupado", "Não sei"][::-1]
            df[var1] = pd.Categorical(df[var1], categories=ordered_categories, ordered=True)
            # Gráfico de mosaico
            fig_mosaic, num_rows = plot_mosaic_with_residuals(df, 
                                                    var1=var1, 
                                                    var2=key,
                                                    xlabel=tema_selecionado,
                                                    ylabel=valor_selecionado,
                                                    figsize=(12, 10))
            
            buf = BytesIO()
            fig_mosaic.savefig(buf, format="png", bbox_inches="tight", dpi=100)
            buf.seek(0)

            st.image(buf, width=1000)

            explicacao_mosaico()

with tabs[3]:
    st.subheader("Na sua opinião, a regulação e gestão da ciência e da tecnologia deveriam ter a participação de...")

    # Gráfico de barras
    octs4_columns = [col for col in df.columns if col.startswith('octs4')]
    octs4_counts = df[octs4_columns].apply(pd.Series.value_counts).fillna(0).reset_index()
    octs4_counts = octs4_counts.melt(id_vars='index', var_name='Variável', value_name='Frequência')
    octs4_counts.columns = ['Valores', 'Variável', 'Frequência']

    ordered_categories = ["Concordo totalmente", "Concordo em partes", "Discordo em partes", "Discordo totalmente", "Não sei"][::-1]
    octs4_counts['Valores'] = pd.Categorical(octs4_counts['Valores'], categories=ordered_categories, ordered=True)
    octs4_counts = octs4_counts.sort_values('Valores')

    fig = px.bar(octs4_counts, 
                 y='Valores', 
                 x='Frequência', 
                 facet_col='Variável', 
                 facet_col_wrap=2, 
                 title='',
                 height=750)
    fig.for_each_annotation(lambda a: a.update(text=f"<b>{varmap[a.text.split('=')[1]]}</b>"))  # Título em negrito

    # Remover títulos dos eixos x e y em todos os facets
    fig.update_xaxes(title_text='', showticklabels=True)  # Remove título do eixo x e mantém os rótulos
    fig.update_yaxes(title_text='', showticklabels=True)  # Remove título do eixo y e mantém os rótulos

    # Remove y ticks in the second column of facets
    for i in range(1, len(fig.data), 2):
        fig.update_yaxes(showticklabels=False, row=(i // 2) + 1, col=2)

    fig.update_layout(xaxis_title='', 
                      yaxis_title='',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
    #                  facet_row_spacing=0.05
    )
    st.plotly_chart(fig, use_container_width=True, key='gestao')

    # Gráfico de mosaico
    with st.container(border=True):
        valor_selecionado = st.pills("Variável Sociodemográfica", list(codigo_variaveis.values()), default=None, key='sociodemografico_selecionado')
        resposta_selecionada = st.pills("Resposta", [varmap[key] for key in varmap if key.startswith("octs4[SQ")], default=None, key='resposta_selecionada')
        if valor_selecionado and resposta_selecionada:
            key = [key for key, value in codigo_variaveis.items() if value == valor_selecionado][0]
            var1 = [key for key, value in varmap.items() if value == resposta_selecionada][0]
            ordered_categories = ["Concordo totalmente", "Concordo em partes", "Discordo em partes", "Discordo totalmente", "Não sei"]
            df[var1] = pd.Categorical(df[var1], categories=ordered_categories, ordered=True)
            # Gráfico de mosaico
            fig_mosaic, num_rows = plot_mosaic_with_residuals(df, 
                                                    var1=var1, 
                                                    var2=key,
                                                    figsize=(7, 5))
            
            buf = BytesIO()
            fig_mosaic.savefig(buf, format="png", bbox_inches="tight", dpi=100)
            buf.seek(0)

            st.image(buf, width=1000)

            explicacao_mosaico()

    st.subheader("Marque por favor sua concordância ou discordância com estas afirmações sobre ciência e tecnologia.")

    # Gráfico de barras
    octs5_columns = [col for col in df.columns if col.startswith('octs5')]
    octs5_counts = df[octs5_columns].apply(pd.Series.value_counts).fillna(0).reset_index()
    octs5_counts = octs5_counts.melt(id_vars='index', var_name='Variável', value_name='Frequência')
    octs5_counts.columns = ['Valores', 'Variável', 'Frequência']
    ordered_categories = ["Concordo totalmente", "Concordo em parte", "Discordo em parte", "Discordo totalmente", "Não sei"][::-1]
    octs5_counts['Valores'] = pd.Categorical(octs5_counts['Valores'], categories=ordered_categories, ordered=True)
    octs5_counts = octs5_counts.sort_values('Valores')

    fig = px.bar(octs5_counts, 
                 y='Valores', 
                 x='Frequência', 
                 facet_col='Variável', 
                 facet_col_wrap=2, 
                 title='',
                 height=600)
    fig.for_each_annotation(lambda a: a.update(text=f"<b>{varmap[a.text.split('=')[1]]}</b>"))  # Título em negrito

    # Remover títulos dos eixos x e y em todos os facets
    fig.update_xaxes(title_text='')  # Remove título do eixo x e rótulos
    fig.update_yaxes(title_text='')  # Remove título do eixo y e rótulos

    # # Exibir y ticks apenas na primeira coluna e x ticks apenas na quarta e quinta facetas
    # for i in range(len(fig.data)):
    #     if i % 2 == 0:  # Primeira coluna de facetas
    #         fig.update_yaxes(showticklabels=True, row=(i // 2) + 1, col=1)
    #     if i == 3 or i == 4:  # Quarta e quinta facetas
    #         fig.update_xaxes(showticklabels=True, row=(i // 2) + 1, col=(i % 2) + 1)
    #         fig.update_xaxes(showticklabels=True, row=(i // 2) + 1, col=(i % 2) + 1)

    fig.update_layout(xaxis_title='', 
                      yaxis_title='',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True, key='opinioes')

    # Gráfico de mosaico
    with st.container(border=True):
        valor_selecionado = st.pills("Variável Sociodemográfica", list(codigo_variaveis.values()), default=None, key='sociodemografico_selecionado2')
        resposta_selecionada = st.pills("Resposta", [varmap[key] for key in varmap if key.startswith("octs5[SQ")], default=None, key='resposta_selecionada2')
        if valor_selecionado and resposta_selecionada:
            key = [key for key, value in codigo_variaveis.items() if value == valor_selecionado][0]
            var1 = [key for key, value in varmap.items() if value == resposta_selecionada][0]
            ordered_categories = ["Concordo totalmente", "Concordo em parte", "Discordo em parte", "Discordo totalmente", "Não sei"][::-1]
            df[var1] = pd.Categorical(df[var1], categories=categories[var1], ordered=True)
            # Gráfico de mosaico
            fig_mosaic, num_rows = plot_mosaic_with_residuals(df, 
                                                    var1=var1, 
                                                    var2=key,
                                                    figsize=(12, 10))
            
            buf = BytesIO()
            fig_mosaic.savefig(buf, format="png", bbox_inches="tight", dpi=100)
            buf.seek(0)

            st.image(buf, width=1000)

            explicacao_mosaico()

st.markdown("---")
st.markdown("Dashboard desenvolvido por [Marcelo Pereira](https://marcelo-pereira.notion.site/)")