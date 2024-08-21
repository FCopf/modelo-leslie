import streamlit as st
import numpy as np
import plotly.graph_objects as go
from aux_fun import cria_matriz_leslie, projeta_populacao

# Configuração do título do aplicativo
st.title("Modelo de Leslie para Projeção Populacional")

# Configuração dos sliders na barra lateral para ajustar os parâmetros da matriz Leslie
st.sidebar.header("Parâmetros do Modelo de Leslie")

b3 = st.sidebar.slider("Taxa de natalidade do grupo etário 3 (b3)", min_value=0.0, max_value=5.0, value=1.2, step=0.01)
b4 = st.sidebar.slider("Taxa de natalidade do grupo etário 4 (b4)", min_value=0.0, max_value=5.0, value=1.5, step=0.01)
s1 = st.sidebar.slider("Taxa de sobrevivência do grupo etário 1 para 2 (s1)", min_value=0.0, max_value=1.0, value=0.6, step=0.01)
s2 = st.sidebar.slider("Taxa de sobrevivência do grupo etário 2 para 3 (s2)", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
s3 = st.sidebar.slider("Taxa de sobrevivência do grupo etário 3 para 4 (s3)", min_value=0.0, max_value=1.0, value=0.8, step=0.01)

# Configuração do slider para definir o número de períodos de projeção
t = st.sidebar.slider("Número de períodos de projeção (t)", min_value=1, max_value=100, value=100)

# Configuração dos sliders para definir os estados iniciais da população
st.sidebar.header("Estados Iniciais da População")

v0_1 = st.sidebar.slider("Estado inicial do grupo etário 1", min_value=0, max_value=500, value=100)
v0_2 = st.sidebar.slider("Estado inicial do grupo etário 2", min_value=0, max_value=500, value=80)
v0_3 = st.sidebar.slider("Estado inicial do grupo etário 3", min_value=0, max_value=500, value=30)
v0_4 = st.sidebar.slider("Estado inicial do grupo etário 4", min_value=0, max_value=500, value=10)

# Criar a matriz Leslie e o vetor de população inicial
L = cria_matriz_leslie(b3, b4, s1, s2, s3)
v0 = np.array([v0_1, v0_2, v0_3, v0_4])

col01, col02, col03 = st.columns([0.2, 0.4, 0.4])

with col01:
    # Exibir a matriz de Leslie
    st.subheader("Estado inicial")
    st.write(v0)
    

with col02:
    # Exibir a matriz de Leslie
    st.subheader("Matriz de Transição")
    st.write(L)

with col03:
    # Calcular o autovalor dominante (taxa de crescimento populacional) e o autovetor correspondente
    eigenvalues, eigenvectors = np.linalg.eig(L)
    dominant_eigenvalue = np.max(np.real(eigenvalues))

    # Exibir a taxa de crescimento populacional
    if dominant_eigenvalue > 1:
        st.success(f'População cresce a uma taxa de {dominant_eigenvalue:.4f} ao ano.', icon="📈")
    elif dominant_eigenvalue < 1:
        st.warning(f'População DECRESCE a uma taxa de {dominant_eigenvalue:.4f} ao ano', icon="📉")
    else:
        st.info(f'População estável. Taxa de crescimento: {dominant_eigenvalue:.4f} ao ano', icon="ℹ️")
    

# Projeção da população ao longo do tempo
populacao = projeta_populacao(L, v0, t)
populacao = np.array(populacao)  # Convertendo para array para facilitar o plot

# Criação das colunas para os gráficos
col1, col2 = st.columns(2)

# Gráfico de Linha do Crescimento Populacional
with col1:
    st.subheader("Crescimento Populacional por Grupo Etário")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=list(range(t+1)), y=populacao[:, 0], mode='lines', name="Rescém nascidos"))
    fig_line.add_trace(go.Scatter(x=list(range(t+1)), y=populacao[:, 1], mode='lines', name="Juvenis"))
    fig_line.add_trace(go.Scatter(x=list(range(t+1)), y=populacao[:, 2], mode='lines', name="Adultos jovens"))
    fig_line.add_trace(go.Scatter(x=list(range(t+1)), y=populacao[:, 3], mode='lines', name="Adultos velhos"))
    fig_line.update_layout(xaxis_title="Tempo", yaxis_title="População")
    st.plotly_chart(fig_line)

# Gráfico de Pirâmide Etária (percentual)
with col2:
    st.subheader("Pirâmide Etária")
    percentual_final = populacao[-1] / np.sum(populacao[-1]) * 100
    fig_pyramid = go.Figure(go.Bar(
        y=["Grupo Etário 1", "Grupo Etário 2", "Grupo Etário 3", "Grupo Etário 4"],
        x=percentual_final,
        orientation='h'
    ))
    fig_pyramid.update_layout(xaxis_title="Percentual da População (%)")
    st.plotly_chart(fig_pyramid)
