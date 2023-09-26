import matplotlib.pyplot as plt
from utils import import_results

D_scale = 0.987
init = 30

exp_name_ppo_0 = "ppo_1"
lim_ppo_0 = [init, 104]
T_ppo_0, D_ppo_0, a_ppo_0, r_ppo_0 = import_results(exp_name_ppo_0, D_scale)

exp_name_ppo_1 = "ppo_4"
lim_ppo_1 = [init, 197, 389, 578, 762, 944, 1118, 1299, 1481, 1669, 1862]
T_ppo_1, D_ppo_1, a_ppo_1, r_ppo_1 = import_results(exp_name_ppo_1, D_scale)

exp_name_ppo_2 = "ppo_5"
lim_ppo_2 = [init, 203, 403]
T_ppo_2, D_ppo_2, a_ppo_2, r_ppo_2 = import_results(exp_name_ppo_2, D_scale)

exp_name_dqn_0 = "dqn_1"
lim_dqn_0 = [init, 103, 405]
T_dqn_0, D_dqn_0, a_dqn_0, r_dqn_0 = import_results(exp_name_dqn_0, D_scale)

exp_name_dqn_1 = "dqn_5"
lim_dqn_1 = [init, 208, 422, 632, 801, 839, 1049, 1260, 1467, 1671, 1873, 2069]
T_dqn_1, D_dqn_1, a_dqn_1, r_dqn_1 = import_results(exp_name_dqn_1, D_scale)

exp_name_dqn_2 = "dqn_8"
lim_dqn_2 = [init, 195, 395]
T_dqn_2, D_dqn_2, a_dqn_2, r_dqn_2 = import_results(exp_name_dqn_2, D_scale)

exp_name = [exp_name_ppo_0, exp_name_ppo_1, exp_name_ppo_2, exp_name_dqn_0, exp_name_dqn_1, exp_name_dqn_2]
D = [D_ppo_0, D_ppo_1, D_ppo_2, D_dqn_0, D_dqn_1, D_dqn_2]
lim = [lim_ppo_0, lim_ppo_1, lim_ppo_2, lim_dqn_0, lim_dqn_1, lim_dqn_2]

for kk, D_exp in enumerate(D):

    D_mean = []
    k = 0
    D_k = D_exp[lim[kk][k] + 1: lim[kk][k + 1]].mean()
    D_mean.append(D_k)
    print("Mean overall for {}: {}".format(exp_name[kk], round(sum(D_mean) / len(D_mean), 3)))


k = 0
fig, axs = plt.subplots(2, 3)
axs[0, 0].plot(T_ppo_0[lim_ppo_0[k] + 1: lim_ppo_0[k + 1]], D_ppo_0[lim_ppo_0[k] + 1: lim_ppo_0[k + 1]], label = "64")
axs[0, 0].set(ylim=[-11.5, -7.5], xticks=[])
axs[0, 0].set_ylabel("$\Delta C_D$", fontsize=15)
axs[0, 0].tick_params(axis="y", labelsize=15)
axs[0, 0].legend(loc=4, fontsize=14)

axs[0, 1].plot(T_ppo_1[lim_ppo_1[k] + 1: lim_ppo_1[k + 1]], D_ppo_1[lim_ppo_1[k] + 1: lim_ppo_1[k + 1]], label = "128")
axs[0, 1].set(yticks=[], ylim=[-11.5, -7.5], xticks=[])
axs[0, 1].legend(loc=4, fontsize=14)

axs[0, 2].plot(T_ppo_2[lim_ppo_2[k] + 1: lim_ppo_2[k + 1]], D_ppo_2[lim_ppo_2[k] + 1: lim_ppo_2[k + 1]], label = "256")
axs[0, 2].set(yticks=[], ylim=[-11.5, -7.5], xticks=[])
axs[0, 2].legend(loc=4, fontsize=14)

axs[1, 0].plot(T_dqn_0[lim_dqn_0[k] + 1: lim_dqn_0[k + 1]], D_dqn_0[lim_dqn_0[k] + 1: lim_dqn_0[k + 1]], color = "tab:red", label = "64")
axs[1, 0].set_ylabel("$\Delta C_D$", fontsize=15)
axs[1, 0].set_xlabel("T", fontsize=15)
axs[1, 0].set(ylim=[-11.5, -7.5])
axs[1, 0].tick_params(axis="both", labelsize=15)
axs[1, 0].legend(loc=4, fontsize=14)

axs[1, 1].plot(T_dqn_1[lim_dqn_1[k] + 1: lim_dqn_1[k + 1]], D_dqn_1[lim_dqn_1[k] + 1: lim_dqn_1[k + 1]], color = "tab:red", label = "128")
axs[1, 1].set(yticks=[], ylim=[-11.5, -7.5])
axs[1, 1].tick_params(axis="x", labelsize=15)
axs[1, 1].set_xlabel("T", fontsize=15)
axs[1, 1].legend(loc=4, fontsize=14)

axs[1, 2].plot(T_dqn_2[lim_dqn_2[k] + 1: lim_dqn_2[k + 1]], D_dqn_2[lim_dqn_2[k] + 1: lim_dqn_2[k + 1]], color = "tab:red", label = "256")
axs[1, 2].set(yticks=[], ylim=[-11.5, -7.5])
axs[1, 2].tick_params(axis="x", labelsize=15)
axs[1, 2].legend(loc=4, fontsize=14)
axs[1, 2].set_xlabel("T", fontsize=15)

plt.xticks(fontsize=15)
plt.tight_layout()
plt.show()
