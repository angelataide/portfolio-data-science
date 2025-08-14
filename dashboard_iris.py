# dashboard_iris.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Título e Descrição ---
st.set_page_config(layout="wide") # Deixa o layout da página mais largo
st.title('Dashboard Interativo do Dataset Iris 🌸')
st.write('Este dashboard permite explorar as características das diferentes espécies de flores Iris.')

# --- Carregar os Dados ---
# Usamos @st.cache_data para que os dados não sejam recarregados a cada interação
@st.cache_data
def carregar_dados():
    df = sns.load_dataset('iris')
    return df

df_iris = carregar_dados()

# --- Barra Lateral com Filtros ---
st.sidebar.header('Filtros')
# Pega a lista de espécies únicas e adiciona a opção 'Todas'
lista_especies = ['Todas'] + list(df_iris['species'].unique())

# Cria um seletor na barra lateral
especie_selecionada = st.sidebar.selectbox('Selecione a Espécie', lista_especies)

# --- Filtrar os Dados com Base na Seleção ---
if especie_selecionada == 'Todas':
    df_filtrado = df_iris
else:
    df_filtrado = df_iris[df_iris['species'] == especie_selecionada]

# --- Exibir os Dados e Gráficos ---
st.header(f'Exibindo dados para: {especie_selecionada}')

# Mostra a tabela de dados filtrada
st.dataframe(df_filtrado.head())

# Cria um gráfico de barras para comparar as médias das características
st.subheader('Comparação das Médias das Características')

# Prepara os dados para o gráfico (calcula a média e "derrete" o dataframe)
df_medias = df_filtrado.groupby('species').mean().reset_index()
df_melted = pd.melt(df_medias, id_vars='species', var_name='Característica', value_name='Média (cm)')

# Cria a figura e o eixo do gráfico
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=df_melted, x='Característica', y='Média (cm)', hue='species', ax=ax, palette='viridis')
plt.xticks(rotation=45)
plt.title('Média das Características por Espécie')

# Mostra o gráfico no Streamlit
st.pyplot(fig)

# --- Outro Gráfico: Pairplot ---
st.subheader('Visualização Cruzada das Características (Pairplot)')
fig_pairplot = sns.pairplot(df_filtrado, hue='species', palette='viridis')
st.pyplot(fig_pairplot)