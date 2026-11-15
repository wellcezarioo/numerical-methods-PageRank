"""
Problema real: PageRank — como o Google ordena páginas da web.

Modelo do "navegador aleatório":
  - Com probabilidade α (fator de amortecimento, tipicamente 0.85) ele clica
    em um link qualquer da página atual.
  - Com probabilidade 1-α ele "se teletransporta" para uma página aleatória.
  - Páginas sem links de saída (dangling) mandam o navegador para qualquer página.

A importância de cada página é a fração de tempo que o navegador passa nela
no longo prazo, ou seja, o vetor estacionário π que satisfaz

        G π = π,     com  G = α S + (1-α)/n · 1 1ᵀ

π é o AUTOVETOR DOMINANTE de G (autovalor λ1 = 1) -> Método das Potências!
Além disso, |λ2| <= α, então o erro cai como α^k (convergência garantida e
previsível, independente do tamanho da web).

Execute:  python pagerank.py
"""

import time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import LinearOperator
import matplotlib.pyplot as plt
from metodo_potencias import metodo_potencias


def matriz_google_densa(links, n, alpha=0.85):
    """Monta G explicitamente (só para redes pequenas, didático)."""
    S = np.zeros((n, n))
    for origem, destinos in links.items():
        for d in destinos:
            S[d, origem] = 1.0 / len(destinos)     # coluna = página de origem
    for j in range(n):
        if S[:, j].sum() == 0:                      # página sem links de saída
            S[:, j] = 1.0 / n
    return alpha * S + (1 - alpha) / n * np.ones((n, n))


def operador_google_esparso(H, alpha=0.85):
    """
    Operador G sem formar a matriz densa (essencial para a web real, n ~ bilhões).

    H: matriz esparsa n x n com H[i, j] = 1/grau_saida(j) se j -> i.
    G x = α H x + [α (soma de x nas páginas dangling) + (1-α) Σx] / n · 1
    Custo por iteração: O(número de links), não O(n²).
    """
    n = H.shape[0]
    dangling = np.asarray(H.sum(axis=0)).ravel() == 0

    def matvec(x):
        x = np.ravel(x)
        return alpha * (H @ x) + (alpha * x[dangling].sum() + (1 - alpha) * x.sum()) / n

    return LinearOperator((n, n), matvec=matvec, dtype=float)


def pagerank(G, tol=1e-10, max_iter=1000, verbose=False):
    """Aplica o Método das Potências e normaliza π para somar 1 (probabilidades)."""
    lam, x, hist = metodo_potencias(G, tol=tol, max_iter=max_iter, verbose=verbose)
    pi = np.abs(x) / np.abs(x).sum()
    return pi, lam, hist


def matriz_H(origem, destino, n):
    """
    Matriz de transição esparsa a partir da lista de links origem -> destino.
    H[i, j] = 1/grau_saida(j) se a página j aponta para i (colunas de páginas
    dangling ficam zeradas; o operador de Google cuida delas).
    """
    A = sp.csr_matrix((np.ones(len(origem)), (origem, destino)), shape=(n, n))
    A.data[:] = 1.0                                   # remove links duplicados
    grau = np.asarray(A.sum(axis=1)).ravel()
    inv = np.divide(1.0, grau, out=np.zeros(n), where=grau > 0)
    return (sp.diags(inv) @ A).T.tocsr()


URL_STANFORD = "https://snap.stanford.edu/data/web-Stanford.txt.gz"


def carregar_web_stanford(caminho="dados/web-Stanford.txt.gz"):
    """
    Grafo REAL da web da Universidade de Stanford (2002), do repositório SNAP:
    281.903 páginas e 2.312.497 hiperlinks.  Baixa o arquivo (~9 MB) se necessário.
    """
    import os
    import urllib.request
    import pandas as pd

    if not os.path.exists(caminho):
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        print(f"Baixando {URL_STANFORD} ...")
        urllib.request.urlretrieve(URL_STANFORD, caminho)

    df = pd.read_csv(caminho, sep="\t", comment="#", header=None, names=["de", "para"])
    ids, inversa = np.unique(np.concatenate([df["de"].values, df["para"].values]),
                             return_inverse=True)
    m = len(df)
    return inversa[:m], inversa[m:], ids               # origem, destino, id original


# ============================================================================
# PARTE 1 — Mini-web com 6 páginas (dá para conferir à mão)
# ============================================================================
if __name__ == "__main__":
    print("=" * 64)
    print("PARTE 1 — Mini-web de 6 páginas")
    print("=" * 64)
    nomes = ["Home", "Notícias", "Esportes", "Blog", "Contato", "Arquivo"]
    links = {               # página -> páginas para as quais ela aponta
        0: [1, 2, 3],
        1: [0, 2],
        2: [0],
        3: [0, 1, 4],
        4: [],              # sem links de saída (dangling)
        5: [3],             # ninguém aponta para "Arquivo"
    }
    n = len(nomes)
    G = matriz_google_densa(links, n, alpha=0.85)

    print("Matriz de Google G (colunas somam 1):")
    print(np.round(G, 3))

    pi, lam, hist = pagerank(G, tol=1e-12, verbose=True)

    # referência: autovetor de numpy
    w, V = np.linalg.eig(G)
    k = np.argmax(np.abs(w))
    pi_ref = np.abs(V[:, k].real) / np.abs(V[:, k].real).sum()

    print(f"\nAutovalor dominante encontrado: λ1 = {lam:.12f}  (esperado: 1)")
    print(f"|λ2| = {np.sort(np.abs(w))[-2]:.4f}  <=  α = 0.85")
    print("\nRanking (Método das Potências vs numpy.linalg.eig):")
    for pos, i in enumerate(np.argsort(-pi), start=1):
        print(f"  {pos}º  {nomes[i]:<9}  π = {pi[i]:.6f}   (numpy: {pi_ref[i]:.6f})")
    print(f"Diferença máxima: {np.max(np.abs(pi - pi_ref)):.2e}")

    # gráfico de barras do ranking
    ordem = np.argsort(-pi)
    plt.figure(figsize=(7, 4))
    plt.bar([nomes[i] for i in ordem], pi[ordem], color="#3a6ea5")
    plt.ylabel("PageRank π")
    plt.title("PageRank da mini-web (α = 0.85)")
    plt.tight_layout()
    plt.savefig("pagerank_miniweb.png", dpi=150)

    # ========================================================================
    # PARTE 2 — Por que não usar simplesmente numpy.linalg.eig?
    # ========================================================================
    print("\n" + "=" * 64)
    print("PARTE 2 — Custo: Método das Potências x numpy.linalg.eig (denso)")
    print("=" * 64)
    print(f"{'n':>6} | {'Potências (s)':>13} | {'numpy.eig (s)':>13} | {'dif. máx em π':>13}")
    print("-" * 56)
    rng = np.random.default_rng(1)
    for N in [250, 500, 1000, 2000]:
        m = 8 * N                                       # ~8 links por página
        H = matriz_H(rng.integers(0, N, m), rng.integers(0, N, m), N)

        t0 = time.perf_counter()
        pi, _, _ = pagerank(operador_google_esparso(H, 0.85), tol=1e-12)
        t_pot = time.perf_counter() - t0

        dang = np.asarray(H.sum(axis=0)).ravel() == 0
        Gd = 0.85 * H.toarray()
        Gd[:, dang] = 0.85 / N
        Gd += 0.15 / N
        t0 = time.perf_counter()
        w, V = np.linalg.eig(Gd)                        # O(n³) tempo, O(n²) memória
        t_eig = time.perf_counter() - t0
        v = np.abs(V[:, np.argmax(np.abs(w))].real)
        print(f"{N:>6} | {t_pot:>13.4f} | {t_eig:>13.4f} | {np.max(np.abs(pi - v / v.sum())):>13.1e}")
    print("Para a web real (n ~ 10^10) a matriz densa nem caberia na memória.")

    # ========================================================================
    # PARTE 3 — PROBLEMA REAL: a web de Stanford (281 mil páginas)
    # ========================================================================
    print("\n" + "=" * 64)
    print("PARTE 3 — PageRank da web real de Stanford (SNAP, 2002)")
    print("=" * 64)
    origem, destino, ids = carregar_web_stanford()
    N = len(ids)
    H = matriz_H(origem, destino, N)
    n_dang = int((np.asarray(H.sum(axis=0)).ravel() == 0).sum())
    print(f"Páginas: {N:,}   Links: {H.nnz:,}   Páginas sem links de saída: {n_dang:,}")
    print(f"Matriz densa ocuparia {N * N * 8 / 1e9:,.0f} GB; a esparsa ocupa "
          f"{(H.data.nbytes + H.indices.nbytes + H.indptr.nbytes) / 1e6:.0f} MB.")

    t0 = time.perf_counter()
    pi, lam, hist = pagerank(operador_google_esparso(H, 0.85), tol=1e-10)
    t_pot = time.perf_counter() - t0
    print(f"\nMétodo das Potências: {len(hist['erro'])} iterações em {t_pot:.2f} s,  λ1 = {lam:.10f}")

    # referência independente: ARPACK (Arnoldi) do SciPy
    from scipy.sparse.linalg import eigs
    t0 = time.perf_counter()
    _, V = eigs(operador_google_esparso(H, 0.85), k=1, which="LM", tol=1e-12)
    t_ref = time.perf_counter() - t0
    v = np.abs(V[:, 0].real)
    v /= v.sum()
    print(f"Referência (scipy eigs/ARPACK): {t_ref:.2f} s,  dif. máx em π = {np.max(np.abs(pi - v)):.1e}")

    print("\nTop 10 páginas (id no dataset SNAP):")
    for pos, i in enumerate(np.argsort(-pi)[:10], start=1):
        print(f"  {pos:>2}º  página {ids[i]:>7}   π = {pi[i]:.6f}   links recebidos: {H.indptr[i+1] - H.indptr[i]}")
    grau_entrada = np.diff(H.indptr)                    # nº de links recebidos
    top10 = np.argsort(-pi)[:10]
    i = top10[np.argmin(grau_entrada[top10])]
    pos_pr = int(np.where(np.argsort(-pi) == i)[0][0]) + 1
    pos_grau = int(np.where(np.argsort(-grau_entrada, kind="stable") == i)[0][0]) + 1
    print(f"-> A página {ids[i]} é a {pos_pr}ª no PageRank, mas só a {pos_grau}ª em número de")
    print("   links recebidos: importa QUEM aponta para você, não só quantos.\n")

    # ------------------------------------------------------------------------
    # Convergência x α na web real: erro cai como α^k
    # ------------------------------------------------------------------------
    print("\nConvergência x fator de amortecimento α:")
    plt.figure(figsize=(7.5, 4.5))
    cores = ["#2a9d8f", "#3a6ea5", "#e76f51", "#8d5a97"]
    for alpha, cor in zip([0.5, 0.85, 0.95, 0.99], cores):
        _, _, h = pagerank(operador_google_esparso(H, alpha), tol=1e-10, max_iter=3000)
        k = np.arange(1, len(h["erro_x"]) + 1)
        plt.semilogy(k, h["erro_x"], color=cor, label=f"α = {alpha}  ({len(k)} it.)")
        plt.semilogy(k, h["erro_x"][0] * alpha ** (k - 1), "--", color=cor, lw=0.8)
        print(f"  α = {alpha:<5} -> {len(k):>5} iterações")
    plt.xlabel("iteração k")
    plt.ylabel("||x_k − x_{k−1}||∞")
    plt.title("Web de Stanford: erro do Método das Potências (tracejado: α^k)")
    plt.xlim(0, 600)
    plt.ylim(1e-11, 10)
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("pagerank_convergencia_alpha.png", dpi=150)

    print("\nGráficos salvos: pagerank_miniweb.png, pagerank_convergencia_alpha.png")
