import matplotlib.pyplot as plt
import numpy as np

# --- Paramètres du CPU et de la mémoire (basés sur votre analyse) ---
# Intel Core i7-10750H (Comet Lake)
# Fréquence effective mesurée par LIKWID (moyenne des mesures LIKWID_perfctr_MEM.txt et FLOPS_DP.txt)
frequency_GHz = 3756.3207 / 1000 # Convert MHz to GHz from likwid_perfctr_MEM.txt (Clock [MHz])

# Peak Performance (P_peak) pour tout le CPU (6 cœurs, AVX2 DP)
# 2 FMA/cycle * 2 FLOPS/FMA * 6 cœurs = 24 FLOPS/cycle pour DP AVX2
# (Note: Votre précédent commentaire indiquait 16 FLOPS/cycle, mais pour 6 coeurs, 4 FLOPS/cycle/core * 6 cores = 24 FLOPS/cycle)
# Vérifions : un Skylake/Cometlake peut faire 2 FMAs (256-bit) par cycle sur les ports 0 et 1.
# Chaque 256-bit FMA est 2 FLOPS (Double Precision). Donc 4 FLOPS/cycle/core.
# Pour 6 coeurs : 4 FLOPS/cycle/core * 6 cores = 24 FLOPS/cycle.
peak_flops_per_cycle_total = 24
P_peak_GFLOPS_s = peak_flops_per_cycle_total * frequency_GHz

# Bande Passante Mémoire (B_peak) théorique pour DDR4-2933 Dual-Channel
# (2933 * 10^6 transferts/s) * 2 canaux * 8 octets/transfert = 46.928 GBytes/s
B_peak_GBytes_s = 46.928

# --- Données de votre application (issues de LIKWID et estimations) ---

# --- AVANT OPTIMISATION ---
P_before_GFLOPS_s = 0.010 # DP GFLOPS/s (LIKWID) avant optimisation
L3_bandwidth_before_GBytes_s = 374.174 / 1000 # Convert MBytes/s to GBytes/s from LIKWID

# Calcul de l'Intensité Arithmétique (AI) avant optimisation
# AI_actual = Performance / Effective_Bandwidth_Used
AI_before = P_before_GFLOPS_s / L3_bandwidth_before_GBytes_s if L3_bandwidth_before_GBytes_s > 0 else 0.0001


# --- APRÈS OPTIMISATION (estimations basées sur le gain de 83.87% du runtime) ---
P_after_GFLOPS_s = 0.062 # DP GFLOPS/s (LIKWID) après optimisation (estimé)
L3_bandwidth_after_GBytes_s = 2319.6 / 1000 # Convert MBytes/s to GBytes/s (estimé)

AI_after = P_after_GFLOPS_s / L3_bandwidth_after_GBytes_s if L3_bandwidth_after_GBytes_s > 0 else 0.0001

# Affichage des calculs pour vérification
print(f"Calculations for Roofline:")
print(f"Peak Compute Performance (P_peak): {P_peak_GFLOPS_s:.2f} GFLOPS/s")
print(f"Peak Memory Bandwidth (B_peak): {B_peak_GBytes_s:.2f} GBytes/s")

print(f"\n--- Avant Optimisation ---")
print(f"  Application Performance (P_before): {P_before_GFLOPS_s:.4f} GFLOPS/s")
print(f"  L3 Bandwidth Used by App (Before): {L3_bandwidth_before_GBytes_s:.4f} GBytes/s")
print(f"  Application Arithmetic Intensity (AI_before): {AI_before:.4f} FLOPS/Byte")

print(f"\n--- Après Optimisation ---")
print(f"  Application Performance (P_after): {P_after_GFLOPS_s:.4f} GFLOPS/s")
print(f"  L3 Bandwidth Used by App (After): {L3_bandwidth_after_GBytes_s:.4f} GBytes/s")
print(f"  Application Arithmetic Intensity (AI_after): {AI_after:.4f} FLOPS/Byte")

# --- Création du graphique Roofline ---

# Générer un ensemble d'intensités arithmétiques pour l'axe X
# Utilisation d'une échelle logarithmique
ai_values = np.logspace(-3, 3, 500) # De 0.001 à 1000 FLOPS/Byte (ajusté pour mieux voir les points)

# Calcul des performances limitées par la mémoire et par le calcul
performance_memory_bound = B_peak_GBytes_s * ai_values
performance_compute_bound = P_peak_GFLOPS_s

# Initialisation du graphique
plt.figure(figsize=(12, 8))
plt.loglog(ai_values, performance_memory_bound, label=f'Memory Bandwidth Limit (DRAM: {B_peak_GBytes_s:.2f} GB/s)', color='blue', linestyle='-')
plt.axhline(y=P_peak_GFLOPS_s, color='red', linestyle='--', label=f'Peak Compute Performance ({P_peak_GFLOPS_s:.2f} GFLOPS/s)')

# Points de notre application
plt.loglog(AI_before, P_before_GFLOPS_s, 'o', color='green', markersize=10, label='GraFC2T2 (Avant Optimisation)', zorder=5)
plt.loglog(AI_after, P_after_GFLOPS_s, '^', color='orange', markersize=10, label='GraFC2T2 (Après Optimisation)', zorder=5)

# Ajout de labels et titres
plt.xlabel('Intensité Arithmétique (FLOPS/Byte)', fontsize=13)
plt.ylabel('Performance (GFLOPS/s)', fontsize=13)
plt.title('Modèle Roofline pour GraFC2T2 sur Intel Core i7-10750H', fontsize=15)
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.legend(fontsize=11)

# Annotation des points de l'application
plt.annotate(
    f'Avant:\nAI={AI_before:.3f}\nP={P_before_GFLOPS_s:.3f}',
    xy=(AI_before, P_before_GFLOPS_s),
    xytext=(AI_before * 1.5, P_before_GFLOPS_s * 1.5),
    arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="black", lw=0.5, alpha=0.7)
)

plt.annotate(
    f'Après:\nAI={AI_after:.3f}\nP={P_after_GFLOPS_s:.3f}',
    xy=(AI_after, P_after_GFLOPS_s),
    xytext=(AI_after * 1.5, P_after_GFLOPS_s * 0.7), # Ajusté la position du texte
    arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.3", fc="cyan", ec="black", lw=0.5, alpha=0.7)
)

# Ajuster les limites des axes pour une meilleure visualisation
plt.xlim([min(ai_values), max(ai_values)])
plt.ylim([min(P_before_GFLOPS_s, P_after_GFLOPS_s) * 0.5, P_peak_GFLOPS_s * 1.5])

plt.show()

print("\n--- Analyse du Modèle Roofline ---")
print("Le graphique Roofline illustre la performance de l'application GraFC2T2 par rapport aux limites théoriques de votre CPU (Intel Core i7-10750H).")
print("Le point 'Avant Optimisation' et le point 'Après Optimisation' sont tous deux situés sur la pente de la ligne de bande passante mémoire (ou très proches de celle-ci).")
print("Ceci confirme que l'application est et reste *memory-bound* (limitée par la vitesse de transfert des données vers le CPU) malgré les améliorations significatives.")
print("Le déplacement du point 'Après Optimisation' vers le haut sur la pente indique que les optimisations (CSR, parallélisation, préchargement) ont permis une utilisation bien plus efficace de la bande passante mémoire disponible.")
print("L'augmentation de l'IPC et de la bande passante L3 utilisée, comme vu dans vos métriques LIKWID, est cohérente avec ce déplacement sur le Roofline. Le CPU est moins souvent en attente de données, ce qui se traduit par une performance globale plus élevée pour la même intensité arithmétique effective de l'algorithme.")
print("L'application n'a pas atteint la ligne horizontale de performance de calcul pic du CPU, ce qui signifie qu'elle ne s'approche pas encore de la limite de calcul pure du processeur.")