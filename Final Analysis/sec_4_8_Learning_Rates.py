import matplotlib.pyplot as plt
from utils import import_results


exp_name = "dqn_9"
lim_ppo_1 = [0, 197, 388]
T_ppo_1, D_ppo_1, a_ppo_1, r_ppo_1 = import_results(exp_name, 0.987)

exp_name_ppo_2 = "dqn_10"
lim_ppo_2 = [0, 194, 381]
T_ppo_2, D_ppo_2, a_ppo_2, r_ppo_2 = import_results(exp_name_ppo_2, 0.987)

D_mean = []
for k in range(len(lim_ppo_1) - 1):
    D_k = D_ppo_1[lim_ppo_1[k] + 1: lim_ppo_1[k + 1]].mean()
    D_mean.append(D_k)
print("SMALL learning rate: {}".format(round(sum(D_mean) / len(D_mean), 3)))

D_mean = []
for k in range(len(lim_ppo_2) - 1):
    D_k = D_ppo_2[lim_ppo_2[k] + 1: lim_ppo_2[k + 1]].mean()
    D_mean.append(D_k)
print("BIG learning rate: {}".format(round(sum(D_mean) / len(D_mean), 3)))


k = 0
fig, axs = plt.subplots(2)
axs[0].plot(T_ppo_1[lim_ppo_1[k] + 1: lim_ppo_1[k + 1]], r_ppo_1[lim_ppo_1[k] + 1: lim_ppo_1[k + 1]], label="1e-5")
axs[0].plot(T_ppo_2[lim_ppo_2[k] + 1: lim_ppo_2[k + 1]], r_ppo_2[lim_ppo_2[k] + 1: lim_ppo_2[k + 1]], label="1e-3")
axs[0].legend(title="Learning rate", loc=3, ncol=3,  fontsize=15, title_fontsize=15, bbox_to_anchor=(0.5, 1))
axs[0].set_ylabel("R", fontsize=15)
axs[0].tick_params(axis='both', labelsize=15)
axs[0].set(xticks=[])

axs[1].plot(T_ppo_1[lim_ppo_1[k] + 1: lim_ppo_1[k + 1]], a_ppo_1[lim_ppo_1[k] + 1: lim_ppo_1[k + 1]])
axs[1].plot(T_ppo_2[lim_ppo_2[k] + 1: lim_ppo_2[k + 1]], a_ppo_2[lim_ppo_2[k] + 1: lim_ppo_2[k + 1]])
axs[1].set_ylabel('a', fontsize=15)
axs[1].tick_params(axis='both', labelsize=15)
plt.xlabel(xlabel='T', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.tight_layout()
plt.show()

