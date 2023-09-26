import matplotlib.pyplot as plt
from utils import import_results

k = 0

exp_name = "dqn_1"
lim = [0, 105]
T, D, a, r = import_results(exp_name, 0.987)


exp_name_2 = "dqn_11"
lim_2 = [0, 208, 421]
T_2, D_2, a_2, r_2 = import_results(exp_name_2, 0.987)

fig, axs = plt.subplots()
plt.plot(T[lim[k] + 1: lim[k + 1]], D[lim[k] + 1: lim[k + 1]], label="Baseline")
plt.plot(T_2[lim_2[k] + 1: lim_2[k + 1]], D_2[lim[k] + 1: lim_2[k + 1]], color="tab:red", label="Final configuration")
plt.ylabel(ylabel="$\Delta C_D$", fontsize=15)
plt.xlabel(xlabel='T', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.legend(loc=4, fontsize=15)
plt.tight_layout()
plt.show()
