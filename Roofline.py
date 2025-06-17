import matplotlib.pyplot as plt
import numpy as np

# --- Paramètres du CPU et de la mémoire (basés sur votre analyse) ---
# Intel Core i7-10750H (Comet Lake)
# Fréquence effective mesurée par LIKWID
frequency_GHz = 3.7563207  # GHz

# Peak Performance (P_peak) pour un coeur
# 2 FMA/cycle * 2 FLOPS/FMA * 4 doubles/256-bit AVX2 = 16 FLOPS/cycle
peak_flops_per_cycle = 16
P_peak_GFLOPS_s = peak_flops_per_cycle * frequency_GHz

# Bande Passante Mémoire (B_peak) théorique pour DDR4-2933 Dual-Channel
# (2933 * 10^6 transferts/s) * 2 canaux * 8 octets/transfert = 46.928 GBytes/s
B_peak_GBytes_s = 46.928

# --- Données de votre application (issues de LIKWID) ---
# Performance mesurée (DP GFLOPS/s)
P_actual_GFLOPS_s = 0.010

# Volume de données L3 utilisé pour le calcul de l'intensité arithmétique
# Volume L3 en MBytes / Runtime en secondes -> L3 bandwidth en MBytes/s
# AI = FLOPS / Bytes = (FLOPS/s) / (Bytes/s) = Performance / Bandwidth
# Ici, nous utilisons le L3 bandwidth pour l'AI_actual car DRAM_READS/WRITES sont vides.
L3_data_volume_MBytes = 844.757
runtime_s_for_L3_data = 2256.3070
L3_bandwidth_used_GBytes_s = (L3_data_volume_MBytes / runtime_s_for_L3_data) / 1000 # Convert MBytes/s to GBytes/s

# Calcul de l'Intensité Arithmétique de l'application (AI_actual)
# AI_actual = P_actual / L3_bandwidth_used_GBytes_s
# Attention: Si L3_bandwidth_used_GBytes_s est très petit ou nul, cela peut causer des problèmes.
# Utilisons la formule P_actual / Bytes_transferred, et pour Bytes_transferred, on prend le L3_data_volume.
# FLOPS = P_actual_GFLOPS_s * runtime_s_for_L3_data
# AI_actual = (P_actual_GFLOPS_s * runtime_s_for_L3_data * 1e9) / (L3_data_volume_MBytes * 1e6)
# AI_actual = (0.010 * 2256.3070 * 1e9) / (844.757 * 1e6)
AI_actual = P_actual_GFLOPS_s / L3_bandwidth_used_GBytes_s if L3_bandwidth_used_GBytes_s > 0 else 0.0001 # Avoid division by zero, give a small value if BW is zero

print(f"Calculations for Roofline:")
print(f"Peak Performance (P_peak): {P_peak_GFLOPS_s:.2f} GFLOPS/s")
print(f"Peak Memory Bandwidth (B_peak): {B_peak_GBytes_s:.2f} GBytes/s")
print(f"Application Performance (P_actual): {P_actual_GFLOPS_s:.4f} GFLOPS/s")
print(f"L3 Bandwidth Used by App: {L3_bandwidth_used_GBytes_s:.4f} GBytes/s")
print(f"Application Arithmetic Intensity (AI_actual): {AI_actual:.4f} FLOPS/Byte")


# --- Création du graphique Roofline ---

# Générer un ensemble d'intensités arithmétiques pour l'axe X
# Utilisation d'une échelle logarithmique
ai_values = np.logspace(-5, 3, 500) # De 10^-5 à 10^3 FLOPS/Byte

# Calcul des performances limitées par la mémoire et par le calcul
performance_memory_bound = B_peak_GBytes_s * ai_values
performance_compute_bound = P_peak_GFLOPS_s

# Initialisation du graphique
plt.figure(figsize=(10, 7))
plt.loglog(ai_values, performance_memory_bound, label='Memory Bandwidth Limit (DRAM)', color='blue')
plt.axhline(y=P_peak_GFLOPS_s, color='red', linestyle='--', label='Peak Compute Performance')

# Point de notre application
plt.loglog(AI_actual, P_actual_GFLOPS_s, 'o', color='green', markersize=10, label='Notre Application (GraFC2T2)')

# Ajout de labels et titres
plt.xlabel('Intensité Arithmétique (FLOPS/Byte)', fontsize=12)
plt.ylabel('Performance (GFLOPS/s)', fontsize=12)
plt.title('Modèle Roofline pour GraFC2T2 sur Intel Core i7-10750H', fontsize=14)
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.legend(fontsize=10)

# Annotation du point de l'application
plt.annotate(
    f'AI: {AI_actual:.4f}\nP: {P_actual_GFLOPS_s:.4f}',
    xy=(AI_actual, P_actual_GFLOPS_s),
    xytext=(AI_actual * 1.5, P_actual_GFLOPS_s * 2), # Position du texte par rapport au point
    arrowprops=dict(facecolor='black', shrink=0.05),
    fontsize=9
)

# Ajuster les limites des axes pour une meilleure visualisation si nécessaire
# plt.xlim([1e-4, 1e2]) # Exemple d'ajustement de l'axe X
# plt.ylim([1e-3, 1e3]) # Exemple d'ajustement de l'axe Y

plt.show()

# Pour sauvegarder le graphique (décommenter et spécifier un nom de fichier)
# plt.savefig('roofline_GraFC2T2.png', dpi=300, bbox_inches='tight')