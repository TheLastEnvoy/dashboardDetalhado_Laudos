import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Carregar os dados do Excel
file_path = "laudos_SO_sharepoint_11022024.xlsx"
df = pd.read_excel(file_path)

# Definir título do aplicativo
st.title("Análise de Laudos")

# Lista de todos os técnicos, tipos de laudo e assentamentos
tecnicos = ['Todos'] + list(df['Técnico'].unique())
tipos_de_laudo = ['Todos'] + list(df['Tipo de Laudo'].unique())
assentamentos = ['Todos'] + list(df['Assentamento'].unique())

# Data inicial padrão: 01/01/2022
start_date = datetime(2022, 1, 1).date()

# Data final padrão: dia atual
end_date = datetime.now().date()

# Filtrar por técnico
selected_tecnico = st.sidebar.selectbox("Selecione um técnico:", tecnicos)
if selected_tecnico != "Todos":
    filtered_df = df[df['Técnico'] == selected_tecnico]
else:
    filtered_df = df

# Filtrar por assentamento
selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos)
if selected_assentamento != "Todos":
    filtered_df = filtered_df[filtered_df['Assentamento'] == selected_assentamento]

# Filtrar por tipo de laudo
selected_tipo_laudo = st.sidebar.selectbox("Selecione um tipo de laudo:", tipos_de_laudo)
if selected_tipo_laudo != "Todos":
    filtered_df = filtered_df[filtered_df['Tipo de Laudo'] == selected_tipo_laudo]

# Filtrar por data
start_date = st.sidebar.date_input("Data inicial:", start_date)
end_date = st.sidebar.date_input("Data final:", end_date)
filtered_df['Data'] = pd.to_datetime(filtered_df['Data'], format='%d/%m/%Y').dt.date
filtered_df = filtered_df[(filtered_df['Data'] >= start_date) & (filtered_df['Data'] <= end_date)]

# Exibir tabela interativa
st.write(filtered_df)

# Exibir gráfico interativo
st.subheader("Contagem de Laudos por Tipo")
chart_data = filtered_df['Tipo de Laudo'].value_counts()
st.bar_chart(chart_data)

# Gráfico de pizza
st.subheader("Gráfico de Pizza - Distribuição dos Laudos")
pie_chart_data = filtered_df['Tipo de Laudo'].value_counts()
fig = px.pie(names=pie_chart_data.index, values=pie_chart_data.values, title='Distribuição dos Laudos')
st.plotly_chart(fig)
