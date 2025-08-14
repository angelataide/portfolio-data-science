# dashboard_titanic.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Configuração da Página e Título ---
st.set_page_config(layout="wide")
st.title('🚢 Análise Interativa do Titanic')
st.write('Este dashboard permite explorar os dados dos passageiros do Titanic e analisar os fatores de sobrevivência.')

# --- Carregar e Limpar os Dados ---
# Usamos @st.cache_data para otimizar o carregamento dos dados
@st.cache_data
def carregar_dados():
    df = sns.load_dataset('titanic')
    
    # Tratamento de dados faltantes (mesma lógica do notebook)
    # Idade: preencher com a mediana
    mediana_idade = df['age'].median()
    df['age'].fillna(mediana_idade, inplace=True)
    
    # Embarked: preencher com a moda (local mais comum)
    moda_embarked = df['embarked'].mode()[0]
    df['embarked'].fillna(moda_embarked, inplace=True)
    
    # Deck: como há muitos dados faltantes, vamos remover a coluna
    df.drop(columns=['deck'], inplace=True)
    
    return df

df_titanic = carregar_dados()

# --- Barra Lateral com Filtros Interativos ---
st.sidebar.header('Filtros para Análise')

# Filtro de Classe (multiselect)
classes = sorted(df_titanic['pclass'].unique())
classe_selecionada = st.sidebar.multiselect('Classe do Passageiro', classes, default=classes)

# Filtro de Gênero (selectbox)
genero_selecionado = st.sidebar.selectbox('Gênero', ['Todos', 'male', 'female'])

# Filtro de Faixa de Idade (slider)
idade_min = int(df_titanic['age'].min())
idade_max = int(df_titanic['age'].max())
faixa_idade_selecionada = st.sidebar.slider(
    'Faixa de Idade',
    min_value=idade_min,
    max_value=idade_max,
    value=(idade_min, idade_max) # Tupla para definir início e fim
)

# --- Filtrar o DataFrame com base nas seleções ---
# Começamos com o dataframe completo e aplicamos os filtros um a um
df_filtrado = df_titanic[
    (df_titanic['pclass'].isin(classe_selecionada)) &
    (df_titanic['age'] >= faixa_idade_selecionada[0]) &
    (df_titanic['age'] <= faixa_idade_selecionada[1])
]

# O filtro de gênero é opcional (se não for 'Todos')
if genero_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['sex'] == genero_selecionado]

# --- Exibição dos Resultados no Dashboard ---
st.header('Análise de Sobreviventes com Filtros Aplicados')

# Métricas principais
total_passageiros = df_filtrado.shape[0]
total_sobreviventes = df_filtrado[df_filtrado['survived'] == 1].shape[0]

# Evitar divisão por zero se não houver passageiros no filtro
if total_passageiros > 0:
    taxa_sobrevivencia = (total_sobreviventes / total_passageiros) * 100
else:
    taxa_sobrevivencia = 0

# Exibir em colunas
col1, col2, col3 = st.columns(3)
col1.metric("Total de Passageiros", f"{total_passageiros}")
col2.metric("Total de Sobreviventes", f"{total_sobreviventes}")
col3.metric("Taxa de Sobrevivência", f"{taxa_sobrevivencia:.2f}%")

st.markdown("---")

st.subheader('Visualização dos Dados Filtrados')

# Gráficos em colunas
gcol1, gcol2 = st.columns(2)

with gcol1:
    st.write("#### Sobrevivência por Classe")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=df_filtrado, x='pclass', hue='survived', ax=ax1, palette='viridis')
    ax1.set_xlabel('Classe do Passageiro')
    ax1.set_ylabel('Contagem')
    st.pyplot(fig1)

with gcol2:
    st.write("#### Sobrevivência por Gênero")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=df_filtrado, x='sex', hue='survived', ax=ax2, palette='plasma')
    ax2.set_xlabel('Gênero')
    ax2.set_ylabel('Contagem')
    st.pyplot(fig2)

# Gráfico de distribuição de idade
st.write("#### Distribuição de Idade por Status de Sobrevivência")
fig3, ax3 = plt.subplots()
sns.histplot(data=df_filtrado, x='age', hue='survived', kde=True, multiple='stack', ax=ax3, palette='magma')
ax3.set_xlabel('Idade')
ax3.set_ylabel('Contagem de Passageiros')
st.pyplot(fig3)

# Exibir a tabela de dados
st.subheader('Dados Detalhados')
st.dataframe(df_filtrado)