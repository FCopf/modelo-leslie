import numpy as np

def cria_matriz_leslie(b3, b4, s1, s2, s3):
    """
    Cria a matriz de Leslie para um modelo de 4 grupos etários.

    Parâmetros:
    b3 - Taxa de natalidade do grupo etário 3 (adultos)
    b4 - Taxa de natalidade do grupo etário 4 (idosos)
    s1 - Taxa de sobrevivência do grupo etário 1 para 2
    s2 - Taxa de sobrevivência do grupo etário 2 para 3
    s3 - Taxa de sobrevivência do grupo etário 3 para 4

    Retorna:
    Uma matriz Leslie 4x4.
    """
    L = np.array([
        [0, 0, b3, b4],
        [s1, 0, 0, 0],
        [0, s2, 0, 0],
        [0, 0, s3, 0]
    ])
    return L

def projeta_populacao(L, v0, t):
    """
    Projeta a população para uma sequência de tempo 1 a t.

    Parâmetros:
    L - Matriz de Leslie
    v0 - Vetor de população inicial (grupos etários)
    t - Número de períodos a serem projetados

    Retorna:
    Uma lista com a população projetada em cada período.
    """
    populacao = [v0]
    for _ in range(t):
        v0 = np.dot(L, v0)
        populacao.append(v0)        
    return populacao