import matplotlib.pyplot as plt
from utils import import_results

exp_name = "dqn_2"
lim = [0, 194, 392, 596, 801, 1010, 1218, 1425, 1626, 1820, 2023]

exp_name_2 = "dqn_6"
lim_2 = [0, 203, 401, 597, 788, 978, 1172, 1370, 1571, 1780, 1992]

k = 3

T_1, D_1, a_1, r_1 = import_results(exp_name, 0.987)
T_2, D_2, a_2, r_2 = import_results(exp_name_2, 0.987)

fig, axs = plt.subplots(2)
axs[0].plot(T_1[lim[k] + 1: lim[k + 1]], D_1[lim[k] + 1: lim[k + 1]], label="1001 points")
axs[0].plot(T_2[lim_2[k] + 1: lim_2[k + 1]], D_2[lim_2[k] + 1: lim_2[k + 1]], label="501 points")
axs[0].set_ylabel("$\Delta C_D$", fontsize=15)
axs[0].tick_params(axis='both', labelsize=15)
axs[0].set(xticks=[])
axs[0].legend(title="Action space", loc=4, fontsize=15, title_fontsize=15)

axs[1].plot(T_1[lim[k] + 1: lim[k + 1]], a_1[lim[k] + 1: lim[k + 1]])
axs[1].plot(T_2[lim_2[k] + 1: lim_2[k + 1]], a_2[lim_2[k] + 1: lim_2[k + 1]])
plt.ylabel(ylabel='a', fontsize=15)
plt.xlabel(xlabel='T', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.tight_layout()
plt.show()
