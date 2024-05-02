%%writefile app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações iniciais de página
st.set_page_config(page_title='Dashboard de Vendas', layout='wide', page_icon='📊')

# Opção para escolher o tema
theme_choice = st.sidebar.radio('Escolha o tema da página:', ('Claro', 'Escuro'))

if theme_choice == 'Escuro':
    st.write('<style>body { background-color: #262730; color: white; }</style>', unsafe_allow_html=True)
else:
    st.write('<style>body { background-color: #FFFFFF; color: black; }</style>', unsafe_allow_html=True)

# Lendo e preparando os dados
df = pd.read_csv("C:/Users/calaz/OneDrive/Documentos/GitHub/Dashboards-Project/Supermarket Dashboard code/supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
df["Day"] = df["Date"].dt.day

# Sidebar - Filtros
month = st.sidebar.selectbox("Mês", df["Month"].unique())
city = st.sidebar.selectbox("Cidade", df["City"].unique(), index=0)

# Filtragem dos dados
df_filtered = df[(df["Month"] == month) & (df["City"] == city)]

# Colunas para os gráficos
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Gráficos
# Faturamento por dia
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

# Faturamento por tipo de produto
fig_prod = px.bar(df_filtered, x="Product line", y="Total", color="City", title="Faturamento por tipo de produto", orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

# Faturamento por filial
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total", title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

# Faturamento por tipo de pagamento
fig_kind = px.pie(df_filtered, values="Total", names="Payment", title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

# Avaliação média por filial
fig_rating = px.bar(df_filtered, y="Rating", x="City", title="Avaliação média por filial")
col5.plotly_chart(fig_rating, use_container_width=True)