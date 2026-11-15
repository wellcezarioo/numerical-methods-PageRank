"""
Exemplos de validação do Método das Potências.

1. Matriz 3x3 clássica: compara com numpy.linalg.eig.
2. Efeito da razão |λ2/λ1| na velocidade de convergência (gráfico).
3. Método das Potências Inverso: menor autovalor e autovalor mais próximo de σ.

Execute:  python exemplos_validacao.py
"""

import numpy as np
import matplotlib.pyplot as plt
from metodo_potencias import metodo_potencias, metodo_potencias_inversa

np.set_printoptions(precision=6, suppress=True)

# ----------------------------------------------------------------------------
# 1) Exemplo clássico
# ----------------------------------------------------------------------------
print("=" * 60)
print("1) Matriz 3x3 — autovalor dominante")
print("=" * 60)
A = np.array([[4.0, 1.0, 1.0],
              [1.0, 3.0, 2.0],
              [1.0, 2.0, 5.0]])

lam, v, hist = metodo_potencias(A, tol=1e-12, verbose=True)

autovalores, autovetores = np.linalg.eig(A)
i = np.argmax(np.abs(autovalores))
v_ref = autovetores[:, i] / autovetores[np.argmax(np.abs(autovetores[:, i])), i]

print(f"\nMétodo das Potências : λ1 = {lam:.12f}   ({len(hist['lambda'])} iterações)")
print(f"numpy.linalg.eig     : λ1 = {autovalores[i]:.12f}")
print(f"Autovetor (potências): {v}")
print(f"Autovetor (numpy)    : {v_ref}")
print(f"Resíduo ||Av - λv||  : {np.linalg.norm(A @ v - lam * v):.2e}")
print(f"Todos os autovalores : {np.sort(autovalores)[::-1]}")
print(f"Razão |λ2/λ1|        : {np.sort(np.abs(autovalores))[-2] / abs(autovalores[i]):.4f}")

# ----------------------------------------------------------------------------
# 2) Velocidade de convergência depende de |λ2/λ1|
# ----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("2) Efeito da razão |λ2/λ1| na convergência")
print("=" * 60)
rng = np.random.default_rng(0)
Q, _ = np.linalg.qr(rng.standard_normal((5, 5)))  # base ortonormal aleatória

plt.figure(figsize=(7, 4.5))
for razao in [0.2, 0.5, 0.8, 0.95]:
    D = np.diag([10.0, 10.0 * razao, 2.0, 1.0, 0.5])
    M = Q @ D @ Q.T                                  # simétrica com autovalores conhecidos
    _, _, h = metodo_potencias(M, tol=1e-14, max_iter=2000)
    erro_real = np.abs(np.array(h["lambda"]) - 10.0) / 10.0
    plt.semilogy(range(1, len(erro_real) + 1), erro_real, label=f"|λ2/λ1| = {razao}")
    print(f"|λ2/λ1| = {razao:<5} -> {len(h['lambda']):>4} iterações")

plt.xlabel("iteração k")
plt.ylabel("erro relativo em λ1")
plt.title("Convergência do Método das Potências")
plt.xlim(0, 150)
plt.ylim(1e-15, 1)
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("convergencia_razao.png", dpi=150)
print("Gráfico salvo em convergencia_razao.png")

# ----------------------------------------------------------------------------
# 3) Potências Inverso (com e sem deslocamento)
# ----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("3) Método das Potências Inverso")
print("=" * 60)
lam_min, _, h = metodo_potencias_inversa(A, sigma=0.0)
print(f"Menor autovalor (σ=0)       : {lam_min:.12f}  ({len(h['lambda'])} iterações)")
lam_s, _, h = metodo_potencias_inversa(A, sigma=3.0)
print(f"Autovalor mais próximo de 3 : {lam_s:.12f}  ({len(h['lambda'])} iterações)")
print(f"Referência numpy            : {np.sort(autovalores)}")
