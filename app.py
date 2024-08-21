import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from aux_fun import cria_matriz_leslie, projeta_populacao

st.set_page_config(layout="wide")

# Grupos etários
grupos_etarios = ['Recém nascidos', 'Juvenis', 'Adultos jovens', 'Adultos velhos']

# Configuração do título do aplicativo
st.title("Modelo Estruturado por Idade para Crescimento Populacional")

with st.sidebar:
    # Configuração dos sliders na barra lateral para ajustar os parâmetros da matriz Leslie
    st.header("Parâmetros do Modelo")

    b3 = st.slider(f"Taxa de natalidade de {grupos_etarios[2]} (b3)", min_value=0.0, max_value=5.0, value=1.2, step=0.01)
    b4 = st.slider(f"Taxa de natalidade de {grupos_etarios[3]} (b4)", min_value=0.0, max_value=5.0, value=1.5, step=0.01)
    s1 = st.slider(f"Taxa de sobrevivência de {grupos_etarios[0]} (s1)", min_value=0.0, max_value=1.0, value=0.6, step=0.01)
    s2 = st.slider(f"Taxa de sobrevivência de {grupos_etarios[1]} (s2)", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
    s3 = st.slider(f"Taxa de sobrevivência de {grupos_etarios[2]} (s3)", min_value=0.0, max_value=1.0, value=0.8, step=0.01)

    # Configuração do slider para definir o número de períodos de projeção
    t = st.slider("Número de períodos de projeção (t)", min_value=1, max_value=100, value=100)


    # Configuração dos sliders para definir os estados iniciais da população
    st.header("Estados Iniciais da População")

    v0_1 = st.slider(f"Estado inicial de {grupos_etarios[0]}", min_value=0, max_value=500, value=100)
    v0_2 = st.slider(f"Estado inicial de {grupos_etarios[1]}", min_value=0, max_value=500, value=80)
    v0_3 = st.slider(f"Estado inicial de {grupos_etarios[2]}", min_value=0, max_value=500, value=30)
    v0_4 = st.slider(f"Estado inicial de {grupos_etarios[3]}", min_value=0, max_value=500, value=10)

# Criar o vetor de população inicial e a matriz Leslie
v0 = np.array([v0_1, v0_2, v0_3, v0_4])
L = cria_matriz_leslie(b3, b4, s1, s2, s3)
L_df = pd.DataFrame(L)
L_df['Grupos Etários'] = grupos_etarios
L_df.set_index('Grupos Etários', inplace=True)
L_df.columns = grupos_etarios

# Calcular o autovalor dominante (taxa de crescimento populacional) e o autovetor correspondente
eigenvalues, eigenvectors = np.linalg.eig(L)
dominant_eigenvalue = np.max(np.real(eigenvalues))

col01, col02 = st.columns([0.35, 0.65])

# Projeção da população ao longo do tempo
populacao = projeta_populacao(L, v0, t)
populacao = np.array(populacao)  # Convertendo para array para facilitar o plot
populacao_df = pd.DataFrame(populacao.T)
N = populacao_df.sum()
populacao_df.loc['Total'] = N
populacao_df['Grupos Etários'] = grupos_etarios + ['Total']
populacao_df.set_index('Grupos Etários', inplace=True)

with col01:
    # Exibir a matriz de Leslie
    st.subheader("Matriz de Leslie")
    st.write(L_df)    

with col02:
    # Exibir a matriz de Leslie
    st.subheader("Estado no tempo t")
    st.write(populacao_df)

# Exibir a taxa de crescimento populacional
if dominant_eigenvalue > 1:
    st.success(f'População cresce a uma taxa de {dominant_eigenvalue:.4f} ao ano.', icon="📈")
elif dominant_eigenvalue < 1:
    st.warning(f'População DECRESCE a uma taxa de {dominant_eigenvalue:.4f} ao ano', icon="📉")
else:
    st.info(f'População estável. Taxa de crescimento: {dominant_eigenvalue:.4f} ao ano', icon="ℹ️")
    
# Criação das colunas para os gráficos
col1, col2 = st.columns(2)

# Gráfico de Linha do Crescimento Populacional
with col1:
    st.subheader("Crescimento Populacional por Grupo Etário")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=list(range(t+1)), y=populacao[:, 0], mode='lines', name=grupos_etarios[0]))
    fig_line.add_trace(go.Scatter(x=list(range(t+1)), y=populacao[:, 1], mode='lines', name=grupos_etarios[1]))
    fig_line.add_trace(go.Scatter(x=list(range(t+1)), y=populacao[:, 2], mode='lines', name=grupos_etarios[2]))
    fig_line.add_trace(go.Scatter(x=list(range(t+1)), y=populacao[:, 3], mode='lines', name=grupos_etarios[3]))
    fig_line.update_layout(xaxis_title="Tempo", yaxis_title="População")
    st.plotly_chart(fig_line)

# Gráfico de Pirâmide Etária (percentual)
with col2:
    st.subheader("Pirâmide Etária")
    percentual_final = populacao[-1] / np.sum(populacao[-1]) * 100
    fig_pyramid = go.Figure(go.Bar(
        y=grupos_etarios,
        x=percentual_final,
        orientation='h'
    ))
    fig_pyramid.update_layout(xaxis_title="Percentual da População (%)")
    st.plotly_chart(fig_pyramid)
