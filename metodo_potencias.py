"""
Método das Potências (e variações) para cálculo de autovalores/autovetores.

Funções:
    metodo_potencias          -> autovalor dominante (maior |λ|) e autovetor
    metodo_potencias_inversa  -> autovalor de menor |λ| ou o mais próximo de um deslocamento σ

Ideia central:
    Se A tem autovalores |λ1| > |λ2| >= ... >= |λn| e x0 tem componente na direção de v1,
        A^k x0 = c1 λ1^k [ v1 + Σ (ci/c1)(λi/λ1)^k vi ]
    Como |λi/λ1| < 1, os termos extras somem e A^k x0 aponta para v1.
    A velocidade de convergência é governada pela razão |λ2/λ1|.
"""

import numpy as np


def metodo_potencias(A, x0=None, tol=1e-10, max_iter=1000, norma="inf", verbose=False):
    """
    Calcula o autovalor dominante λ1 de A e o autovetor associado.

    Parâmetros
    ----------
    A        : matriz (n x n) — numpy array ou matriz esparsa do SciPy
               (basta que suporte o produto A @ x).
    x0       : vetor inicial (padrão: vetor de uns).
    tol      : tolerância. Para quando AMBOS são menores que tol:
                 |λ_k - λ_{k-1}| / |λ_k|   e   ||x_k - x_{k-1}||_inf
               (usar só a variação de λ pode parar cedo demais, se duas
               estimativas consecutivas coincidirem por acaso).
    max_iter : número máximo de iterações.
    norma    : "inf" (normaliza pela maior componente, versão clássica dos livros)
               ou "2" (normaliza pela norma euclidiana, λ via quociente de Rayleigh).
    verbose  : imprime a tabela de iterações.

    Retorna
    -------
    lam      : estimativa do autovalor dominante.
    x        : autovetor normalizado.
    historico: dict com listas por iteração (útil para gráficos):
               'lambda', 'erro_lambda', 'erro_x' e 'erro' (= max dos dois).
    """
    n = A.shape[0]
    x = np.ones(n) if x0 is None else np.asarray(x0, dtype=float).copy()

    # normalização inicial
    if norma == "inf":
        x = x / x[np.argmax(np.abs(x))]
    else:
        x = x / np.linalg.norm(x)

    lam_ant = 0.0
    historico = {"lambda": [], "erro_lambda": [], "erro_x": [], "erro": []}

    if verbose:
        print(f"{'k':>4} | {'λ_k':>18} | {'erro':>14}")
        print("-" * 44)

    for k in range(1, max_iter + 1):
        y = A @ x  # único custo relevante: um produto matriz-vetor

        if norma == "inf":
            # λ_k = componente de maior módulo de y (com sinal)
            idx = np.argmax(np.abs(y))
            lam = y[idx]
            x_novo = y / lam
        else:
            # quociente de Rayleigh: λ ≈ xᵀAx / xᵀx  (x já tem norma 1)
            lam = x @ y
            # o sinal de λ evita que x troque de sinal a cada iteração quando λ < 0
            x_novo = np.sign(lam) * y / np.linalg.norm(y)

        erro_lam = abs(lam - lam_ant) / abs(lam) if lam != 0 else np.inf
        erro_x = np.max(np.abs(x_novo - x))
        erro = max(erro_lam, erro_x)
        x = x_novo

        historico["lambda"].append(lam)
        historico["erro_lambda"].append(erro_lam)
        historico["erro_x"].append(erro_x)
        historico["erro"].append(erro)

        if verbose:
            print(f"{k:>4} | {lam:>18.12f} | {erro:>14.3e}")

        if erro < tol:
            break
        lam_ant = lam
    else:
        print(f"Aviso: não convergiu em {max_iter} iterações (erro = {erro:.2e}).")

    return lam, x, historico


def metodo_potencias_inversa(A, sigma=0.0, x0=None, tol=1e-10, max_iter=1000, verbose=False):
    """
    Método das Potências Inverso com deslocamento σ.

    Aplica o método das potências em (A - σI)^(-1), cujos autovalores são 1/(λi - σ).
    O dominante corresponde ao λi MAIS PRÓXIMO de σ. Com σ = 0 obtém-se o
    autovalor de menor módulo.

    Em vez de inverter a matriz, fatoramos (A - σI) = LU uma única vez e,
    a cada iteração, resolvemos um sistema linear (custo O(n²)).
    """
    from scipy.linalg import lu_factor, lu_solve

    A = np.asarray(A, dtype=float)
    n = A.shape[0]
    lu_piv = lu_factor(A - sigma * np.eye(n))

    x = np.ones(n) if x0 is None else np.asarray(x0, dtype=float).copy()
    x = x / x[np.argmax(np.abs(x))]
    mu_ant = 0.0
    historico = {"lambda": [], "erro": []}

    for k in range(1, max_iter + 1):
        y = lu_solve(lu_piv, x)          # y = (A - σI)^(-1) x
        idx = np.argmax(np.abs(y))
        mu = y[idx]                      # μ ≈ 1/(λ - σ)
        x_novo = y / mu

        lam = sigma + 1.0 / mu
        erro = max(abs(mu - mu_ant) / abs(mu), np.max(np.abs(x_novo - x)))
        x = x_novo
        historico["lambda"].append(lam)
        historico["erro"].append(erro)

        if verbose:
            print(f"{k:>4} | λ ≈ {lam:>18.12f} | erro = {erro:.3e}")
        if erro < tol:
            break
        mu_ant = mu
    else:
        print(f"Aviso: não convergiu em {max_iter} iterações (erro = {erro:.2e}).")

    return lam, x, historico
