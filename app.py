import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard de Fraudes", layout="wide")

st.title("🏦 Dashboard Executivo: Análise de Fraudes Bancárias")
st.markdown("Este dashboard apresenta os resultados da camada **Gold** do nosso pipeline de dados.")

# Carregar os dados da camada Gold
try:
    df_gold = pd.read_parquet('data_gold/relatorio_pico_fraudes.parquet')
    
    # Sidebar para filtros
    st.sidebar.header("Filtros")
    hora_selecionada = st.sidebar.multiselect(
        "Selecione as Horas:",
        options=df_gold["hora_do_dia"].unique(),
        default=df_gold["hora_do_dia"].unique()
    )
    
    df_filtrado = df_gold[df_gold["hora_do_dia"].isin(hora_selecionada)]

    # Métricas Principais
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Fraudes", f"{df_filtrado['total_transacoes_fraudulentas'].sum()}")
    col2.metric("Prejuízo Total", f"R$ {df_filtrado['valor_total_perdido'].sum():,.2f}")
    col3.metric("Ticket Médio", f"R$ {df_filtrado['ticket_medio_fraude'].mean():,.2f}")

    st.divider()

    # Gráfico de Barras: Prejuízo por Hora
    st.subheader("⚠️ Impacto Financeiro por Hora do Dia")
    fig_bar = px.bar(
        df_filtrado, 
        x="hora_do_dia", 
        y="valor_total_perdido",
        labels={'hora_do_dia': 'Hora do Dia', 'valor_total_perdido': 'Valor Perdido (R$)'},
        color="valor_total_perdido",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Tabela de Dados
    st.subheader("📄 Dados Detalhados")
    st.dataframe(df_filtrado, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.info("Certifique-se de rodar o 'analysis_gold.py' primeiro para gerar os dados.")