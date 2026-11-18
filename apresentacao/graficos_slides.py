"""
Gráficos usados nos slides (fonte maior, fundo claro, para projetar).

Gera em apresentacao/figuras/:
    convergencia_razao_slides.png   erro x iteração para |λ2/λ1| = 0,2 / 0,5 / 0,8 / 0,95
    pagerank_alpha_slides.png       web de Stanford: erro x iteração para α = 0,5 / 0,85 / 0,95 / 0,99
    miniweb_slides.png              diagrama de links da mini-web de 6 páginas

Execute a partir da raiz do repositório:  python apresentacao/graficos_slides.py   (~30 s)
"""
import math
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from metodo_potencias import metodo_potencias                                    # noqa: E402
from pagerank import carregar_web_stanford, matriz_H, operador_google_esparso   # noqa: E402

SAIDA = os.path.join(RAIZ, "apresentacao", "figuras")
os.makedirs(SAIDA, exist_ok=True)

FUNDO, TINTA, SUAVE = "#FBFAF6", "#16213A", "#4A5468"
CORES = ["#2A9D8F", "#2F5D8C", "#E76F51", "#8D5A97"]
plt.rcParams.update({
    "font.size": 20, "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#9AA0AA", "axes.labelcolor": TINTA, "xtick.color": SUAVE, "ytick.color": SUAVE,
    "figure.facecolor": FUNDO, "axes.facecolor": FUNDO,
})

# ----------------------------------------------------------------------------
# 1) Convergência x razão |λ2/λ1|  (mesmas matrizes de exemplos_validacao.py)
# ----------------------------------------------------------------------------
rng = np.random.default_rng(0)
Q, _ = np.linalg.qr(rng.standard_normal((5, 5)))
fig, ax = plt.subplots(figsize=(10, 6.2))
for razao, cor in zip([0.2, 0.5, 0.8, 0.95], CORES):
    M = Q @ np.diag([10.0, 10.0 * razao, 2.0, 1.0, 0.5]) @ Q.T
    _, _, h = metodo_potencias(M, tol=1e-14, max_iter=2000)
    erro = np.abs(np.array(h["lambda"]) - 10.0) / 10.0
    ax.semilogy(range(1, len(erro) + 1), erro, color=cor, lw=3.5,
                label=f"|λ₂/λ₁| = {razao}   →  {len(erro)} iterações")
ax.set_xlabel("iteração k")
ax.set_ylabel("erro relativo em λ₁")
ax.set_xlim(0, 150)
ax.set_ylim(1e-15, 1)
ax.grid(True, which="major", alpha=0.3)
ax.legend(frameon=False, fontsize=19, loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(SAIDA, "convergencia_razao_slides.png"), dpi=160)
plt.close(fig)

# ----------------------------------------------------------------------------
# 2) Web de Stanford: erro x α  (mesmo experimento de pagerank.py)
# ----------------------------------------------------------------------------
origem, destino, ids = carregar_web_stanford(os.path.join(RAIZ, "dados", "web-Stanford.txt.gz"))
H = matriz_H(origem, destino, len(ids))
fig, ax = plt.subplots(figsize=(10, 6.2))
for alpha, cor in zip([0.5, 0.85, 0.95, 0.99], CORES):
    _, _, h = metodo_potencias(operador_google_esparso(H, alpha), tol=1e-10, max_iter=3000)
    k = np.arange(1, len(h["erro_x"]) + 1)
    ax.semilogy(k, h["erro_x"], color=cor, lw=3.5, label=f"α = {alpha}   →  {len(k)} iterações")
    ax.semilogy(k, h["erro_x"][0] * alpha ** (k - 1), "--", color=cor, lw=1.6)
ax.set_xlabel("iteração k")
ax.set_ylabel("‖xₖ − xₖ₋₁‖∞")
ax.set_xlim(0, 600)
ax.set_ylim(1e-11, 10)
ax.grid(True, which="major", alpha=0.3)
ax.legend(frameon=False, fontsize=19, loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(SAIDA, "pagerank_alpha_slides.png"), dpi=160)
plt.close(fig)

# ----------------------------------------------------------------------------
# 3) Diagrama da mini-web (mesmos links de pagerank.py)
# ----------------------------------------------------------------------------
pos = {"Home": (0.5, 0.80), "Notícias": (0.12, 0.45), "Esportes": (0.12, 0.06),
       "Blog": (0.88, 0.45), "Contato": (0.88, 0.06), "Arquivo": (0.5, 0.06)}
links = [("Home", "Notícias"), ("Home", "Esportes"), ("Home", "Blog"), ("Notícias", "Home"),
         ("Notícias", "Esportes"), ("Esportes", "Home"), ("Blog", "Home"), ("Blog", "Notícias"),
         ("Blog", "Contato"), ("Arquivo", "Blog")]
fig, ax = plt.subplots(figsize=(10, 7.4))
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.06, 0.92)
ax.axis("off")
pares = set(links)
for a, b in links:
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ang = math.atan2(abs((y2 - y1) / 0.98 * 533), abs((x2 - x1) / 1.1 * 720))
    recuo = min(72 / max(math.cos(ang), 1e-6), 32 / max(math.sin(ang), 1e-6)) + 6  # para na borda da caixa
    ax.add_patch(FancyArrowPatch(pos[a], pos[b], connectionstyle=f"arc3,rad={0.18 if (b, a) in pares else 0.0}",
                                 arrowstyle="-|>,head_length=14,head_width=8", color="#2F5D8C", lw=2.6,
                                 shrinkA=recuo, shrinkB=recuo, zorder=1))
for nome, (x, y) in pos.items():
    cor = {"Contato": "#F4A261", "Arquivo": "#D9DEE6"}.get(nome, TINTA)
    ax.add_patch(FancyBboxPatch((x - 0.1, y - 0.05), 0.2, 0.1, boxstyle="round,pad=0.01,rounding_size=0.03",
                                fc=cor, ec="none", zorder=2))
    ax.text(x, y, nome, ha="center", va="center", fontsize=24, fontweight="bold", zorder=3,
            color=TINTA if nome in ("Contato", "Arquivo") else "#F6F4EE")
fig.tight_layout(pad=0.2)
fig.savefig(os.path.join(SAIDA, "miniweb_slides.png"), dpi=160)
plt.close(fig)

print(f"Figuras salvas em {SAIDA}")
