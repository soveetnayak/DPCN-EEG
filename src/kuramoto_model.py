# -*- coding: utf-8 -*-
"""code1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SsID52nkQNgtnK6tcFN9YZ2_m8vlcQHg
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tqdm import tqdm
from scipy.integrate import odeint

class Kuramoto:
    def __init__(self, coupling, dt, T, n_nodes):
        self.dt = dt
        self.T = T
        self.coupling = coupling
        self.n_nodes = n_nodes
        self.natfreqs = np.random.normal(size=self.n_nodes)

    def derivative(self, angles_vec, t, adj_mat, k):
        angles_i, angles_j = np.meshgrid(angles_vec, angles_vec)
        interactions = adj_mat * np.sin(angles_j - angles_i)  # Aij * sin(j-i)
        dxdt = self.natfreqs + k * interactions.sum(axis=0)  # sum over incoming interactions
        return dxdt

    def integrate(self, angles_vec, adj_mat):
        n_interactions = (adj_mat != 0).sum(axis=0)  # number of incoming interactions
        k = self.coupling / n_interactions  # normalize coupling by number of interactions
        t = np.linspace(0, self.T, int(self.T/self.dt))
        timeseries = odeint(self.derivative, angles_vec, t, args=(adj_mat, k))
        return timeseries.T

    def run(self, adj_mat=None, angles_vec=None):
        angles_vec = 2 * np.pi * np.random.random(size=self.n_nodes)
        return self.integrate(angles_vec, adj_mat)

    @staticmethod
    def phase_coherence(angles_vec):
        suma = sum([(np.e ** (1j * i)) for i in angles_vec])
        return abs(suma / len(angles_vec))

df = pd.read_csv("../data/111g0L_filtered_fragment_0_binary.csv", header=None)
A = df.values
print(A)
adjMatrix = np.array(A)
n = len(adjMatrix)

# model = Kuramoto(coupling=3, dt=0.01, T=1000, n_nodes=n)
# x = model.run(adjMatrix)
# print(x.shape)

# Run model with different coupling (K) parameters
coupling_vals = np.linspace(0, 3, 500)
runs = []
for coupling in tqdm(coupling_vals):
    model = Kuramoto(coupling=coupling, dt=0.01, T=1000, n_nodes=n)
    model.natfreqs = np.random.normal(1, 0.4, size=n)  # reset natural frequencies
    act_mat = model.run(adjMatrix)
    runs.append(act_mat)

runs_array = np.array(runs)

''' 
plt.figure()
for i, coupling in tqdm(enumerate(coupling_vals)):
    r_values = [model.phase_coherence(vec) for vec in runs_array[i, :, -80000:].T]
    r_mean = np.mean(r_values)
    r_std = np.std(r_values)
    plt.errorbar(coupling, r_mean, yerr=r_std, fmt='o', c='yellow', alpha=0.7)
    plt.scatter(coupling, r_mean, c='red', s=20, alpha=0.7)

# Predicted Kc – analytical result (from paper)
Kc = np.sqrt(8 / np.pi) * np.std(model.natfreqs) # analytical result (from paper)
plt.vlines(Kc, 0, 1, linestyles='--', color='orange', label='analytical prediction')

plt.legend()
plt.grid(linestyle='--', alpha=0.8)
plt.ylabel('Order Parameter (R)')
plt.xlabel('Coupling (K)')
sns.despine()
# plt.show()
# plt.savefig('../figures/11g0L_0_R_vs_K.png')
'''

mean_phase_coherences = []
std_phase_coherences = []
for i, coupling in tqdm(enumerate(coupling_vals)):
    # mean over 80k steps
    r_mean = np.mean([model.phase_coherence(vec) for vec in runs_array[i, :, -80000:].T])
    mean_phase_coherences.append(r_mean)
    r_std = np.std([model.phase_coherence(vec) for vec in runs_array[i, :, -80000:].T])
    std_phase_coherences.append(r_std)

# Plot mean phase coherence curve
plt.figure()
Kc = np.sqrt(8 / np.pi) * np.std(model.natfreqs) # analytical result (from paper)
plt.vlines(Kc, 0, 1, linestyles='--', color='orange', label='analytical prediction')
plt.plot(coupling_vals, mean_phase_coherences, color='blue', label='Mean Phase Coherence')
plt.xlabel('Coupling (K)')
plt.ylabel('Mean Phase Coherence')
plt.title('Mean Phase Coherence vs Coupling Strength')
plt.legend()
plt.grid(True)
plt.show()
# plt.savefig('../figures/11g0L_0_Mean_Phase_Coherence_vs_K.png')

'''
# Plot the line for mean phase coherence with standard deviation as shaded region
plt.figure()
plt.plot(coupling_vals, mean_phase_coherences, color='blue', label='Mean Phase Coherence')
plt.fill_between(coupling_vals, np.array(mean_phase_coherences) - np.array(std_phase_coherences),
                    np.array(mean_phase_coherences) + np.array(std_phase_coherences), color='blue', alpha=0.3)
plt.xlabel('Coupling (K)')
plt.ylabel('Mean Phase Coherence')
plt.title('Mean Phase Coherence vs Coupling Strength')
plt.legend()
plt.grid(True)
plt.show() 
# plt.savefig('../figures/11g0L_0_Mean_Phase_Coherence_with_std_vs_K.png')
'''