import matplotlib.pyplot as plt
from utils import import_results

exp_name = "dqn_3"
lim = [0, 199, 394, 595, 802, 1008]

exp_name_2 = "dqn_2"
lim_2 = [0, 194, 392, 596, 801, 1010, 1218, 1425, 1626, 1820, 2023]

exp_name_3 = "dqn_4"
lim_3 = [0, 196, 391, 590, 784, 982, 1185, 1385, 1579, 1768, 1957]

k = 4

T_1, D_1, a_1, r_1 = import_results(exp_name, 0.987)
T_2, D_2, a_2, r_2 = import_results(exp_name_2, 0.987)
T_3, D_3, a_3, r_3 = import_results(exp_name_3, 0.987)

fig, axs = plt.subplots(1)
plt.plot(T_3[lim_3[k] + 1: lim_3[k + 1]], D_3[lim_3[k] + 1: lim_3[k + 1]], label = "T2")
plt.plot(T_2[lim_2[k] + 1: lim_2[k + 1]], D_2[lim_2[k] + 1: lim_2[k + 1]], label = "T1")
plt.ylabel(ylabel='$\Delta C_D$', fontsize=15)
plt.xlabel(xlabel='T', fontsize=15)
plt.yticks([-12, -10, -8], fontsize=15)
plt.xticks(fontsize=15)
plt.legend(loc=4, fontsize=14)
plt.tight_layout()
plt.show()

D_mean = []
for k in range(len(lim) - 1):
    D_k = D_1[lim[k] + 1: lim[k + 1]].mean()
    D_mean.append(D_k)
print("Mean overall for {}: {}".format(exp_name, round(sum(D_mean) / len(D_mean), 3)))
D_mean = []
for k in range(len(lim_2) - 1):
    D_k = D_2[lim_2[k] + 1: lim_2[k + 1]].mean()
    D_mean.append(D_k)
print("Mean overall for {}: {}".format(exp_name_2, round(sum(D_mean) / len(D_mean), 3)))
D_mean = []
for k in range(len(lim_3) - 1):
    D_k = D_3[lim_3[k] + 1: lim_3[k + 1]].mean()
    D_mean.append(D_k)
print("Mean overall for {}: {}".format(exp_name_3, round(sum(D_mean) / len(D_mean), 3)))