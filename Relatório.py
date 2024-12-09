import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página Streamlit
st.set_page_config(
    page_title="Dashboard Resumo e Planilha Geral",
    layout="wide",
)

# Título
st.title("Dashboard Inicial - Resumo Geral e Dados")

# Carregar Planilha
uploaded_file = st.file_uploader(
    "Carregue a planilha Excel com os dados:", type=["xlsx", "xls"]
)

if uploaded_file:
    try:
        # Lendo dados da planilha
        df = pd.read_excel(uploaded_file)

        # Validar se os dados têm as colunas esperadas
        colunas_necessarias = ["Unidade", "Cliente", "Vendedor", "Valor_Compra", "Valor_Mensal", "Valor_Plano de assinatura"]
        if not set(colunas_necessarias).issubset(df.columns):
            st.error(
                f"A planilha deve conter as seguintes colunas obrigatórias: {colunas_necessarias}"
            )
        else:
            # Resumo Geral
            total_clientes = df["Cliente"].nunique()
            soma_valor_compra = df["Valor_Compra"].sum()
            soma_valor_mensal = df["Valor_Mensal"].sum()
            soma_valor_plano = df["Valor_Plano de assinatura"].sum()

            st.header("Resumo Geral")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total de Clientes", total_clientes)
            col2.metric("Total Valor de Compra", f"R$ {soma_valor_compra:,.2f}")
            col3.metric("Total Valor Mensal", f"R$ {soma_valor_mensal:,.2f}")
            col4.metric("Total Plano de Assinatura", f"R$ {soma_valor_plano:,.2f}")

            # Layout: Planilha e Gráfico
            st.header("Planilha Geral e Gráfico")
            col1, col2 = st.columns([3, 2])

            # Exibir Planilha Geral
            with col1:
                st.subheader("Planilha Geral")
                st.dataframe(df, use_container_width=True)

            # Gráfico de Barras: Quantidade de Clientes por Unidade
            with col2:
                st.subheader("Quantidade de Clientes por Unidade")
                dados_unidade = df.groupby("Unidade")["Cliente"].nunique().reset_index()
                dados_unidade = dados_unidade.rename(columns={"Cliente": "Quantidade_Clientes"})
                fig = px.bar(
                    dados_unidade,
                    x="Unidade",
                    y="Quantidade_Clientes",
                    title="Clientes por Unidade",
                    labels={"Unidade": "Unidade", "Quantidade_Clientes": "Clientes"}
                )
                st.plotly_chart(fig, use_container_width=True)

            # Gráficos Individuais por Vendedor (Todos os Vendedores)
            st.header("Análises por Vendedor")
            vendedores = df["Vendedor"].unique()

            for vendedor in vendedores:
                st.subheader(f"Análise para o Vendedor: {vendedor}")

                # Filtrando os dados do vendedor específico
                dados_vendedor = df[df["Vendedor"] == vendedor]

                # Informações principais do vendedor
                total_clientes_vendedor = dados_vendedor["Cliente"].nunique()
                soma_valor_compra_vendedor = dados_vendedor["Valor_Compra"].sum()
                soma_valor_mensal_vendedor = dados_vendedor["Valor_Mensal"].sum()
                soma_valor_plano_vendedor = dados_vendedor["Valor_Plano de assinatura"].sum()

                # Apresentando as informações na interface
                col_vend_1, col_vend_2, col_vend_3, col_vend_4 = st.columns(4)
                col_vend_1.metric("Total de Clientes Atendidos", total_clientes_vendedor)
                col_vend_2.metric("Total Valor de Compra", f"R$ {soma_valor_compra_vendedor:,.2f}")
                col_vend_3.metric("Total Valor Mensal", f"R$ {soma_valor_mensal_vendedor:,.2f}")
                col_vend_4.metric("Total Plano de Assinatura", f"R$ {soma_valor_plano_vendedor:,.2f}")

                # Gráfico: Comparativo por temperatura e quantidade de propostas
                st.subheader("Gráfico de Análise do Vendedor")
                fig_vendedor = px.line(
                    dados_vendedor,
                    x="Mês",
                    y=["Temperatura", "Valor_Compra"],
                    title=f"Análise do Vendedor: {vendedor}",
                    labels={"Temperatura": "Temperatura", "Valor_Compra": "Valor de Compra"}
                )
                st.plotly_chart(fig_vendedor, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao processar a planilha: {e}")
else:
    st.warning("Por favor, carregue sua planilha para começar.")
