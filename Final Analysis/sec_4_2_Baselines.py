import matplotlib.pyplot as plt
from utils import import_results

# BASELINE DQN #
exp_name = "dqn_1"
lim = [0, 203, 405]
k = 0

T, D, a, r = import_results(exp_name)

# PLOT BASELINE DQN RESULTS
fig, axs = plt.subplots(3)
axs[0].plot(T[lim[k] + 1: lim[k + 1]], D[lim[k] + 1: lim[k + 1]], color="tab:red")
axs[0].set_ylabel("$C_D$", fontsize=15)
axs[0].tick_params(axis='both', labelsize=15)
axs[0].set(yticks=[0.87, 0.9])
axs[0].set(xticks=[])

axs[1].plot(T[lim[k] + 1: lim[k + 1]], r[lim[k] + 1: lim[k + 1]], color="tab:red")
axs[1].set_ylabel('R', fontsize=15)
axs[1].tick_params(axis='both', labelsize=15)
axs[1].set(xticks=[])

axs[2].plot(T[lim[k] + 1: lim[k + 1]], a[lim[k] + 1: lim[k + 1]], color="tab:red")
plt.ylabel(ylabel='a', fontsize=15)
plt.xlabel(xlabel='T', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)

plt.tight_layout()
plt.show()

D_mean = []
for k in range(len(lim) - 1):
    D_k = D[lim[k] + 1: lim[k + 1]].mean()
    D_mean.append(D_k)
print("Mean drag coefficient for DQN baseline: {}".format(round(sum(D_mean) / len(D_mean), 3)))

#################

# BASELINE PPO #
exp_name = "ppo_1"
lim = [0, 204]
k = 0

T, D, a, r = import_results(exp_name)

fig, axs = plt.subplots(3)
axs[0].plot(T[lim[k] + 1: lim[k + 1]], D[lim[k] + 1: lim[k + 1]])
axs[0].set_ylabel("$C_D$", fontsize=15)
axs[0].tick_params(axis='both', labelsize=15)
axs[0].set(yticks=[0.87, 0.9])
axs[0].set(xticks=[])

axs[1].plot(T[lim[k] + 1: lim[k + 1]], r[lim[k] + 1: lim[k + 1]])
axs[1].set_ylabel('R', fontsize=15)
axs[1].tick_params(axis='both', labelsize=15)
axs[1].set(xticks=[])

axs[2].plot(T[lim[k] + 1: lim[k + 1]], a[lim[k] + 1: lim[k + 1]])
plt.ylabel(ylabel='a', fontsize=15)
plt.xlabel(xlabel='T', fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.tight_layout()
plt.show()

D_mean = []
for k in range(len(lim) - 1):
    D_k = D[lim[k] + 1: lim[k + 1]].mean()
    D_mean.append(D_k)
print("Mean drag coefficient for DQN baseline: {}".format(round(sum(D_mean) / len(D_mean), 3)))
