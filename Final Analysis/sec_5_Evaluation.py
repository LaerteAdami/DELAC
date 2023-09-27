import matplotlib.pyplot as plt
import numpy as np

#####################################
exp_name = "rigid_flap_case"
path = "../Aero/Results/" + exp_name + "/1/"
with open(path + "/Drag.txt") as f:
    drag_txt = f.readlines()
with open(path + "/Time.txt") as f:
    time_txt = f.readlines()
drag = []
time = []
for line in drag_txt:
    drag.append(float(line))
for line in time_txt:
    time.append(float(line))
lim_time = 40
D_solid = drag[int(lim_time / 0.1):]
t_solid = time[int(lim_time / 0.1):]
D_solid = np.array(D_solid)
D_solid *= 2 /(1.225*1.225)

##################################
exp_name = "free_flexible_case"
path = "../Aero/Results/" + exp_name + "/1/"
with open(path + "/Drag.txt") as f:
    drag_txt = f.readlines()
with open(path + "/Time.txt") as f:
    time_txt = f.readlines()
drag = []
time = []
for line in drag_txt:
    drag.append(float(line))
for line in time_txt:
    time.append(float(line))
lim_time = 40
D_flex = drag[int(lim_time / 0.1):]
t_flex = time[int(lim_time / 0.1):]
D_flex = np.array(D_flex)
D_flex *= 2 /(1.225*1.225)

##################################
k = 0
exp_name = "dqn_11"
lim = [6, 128, 401, 597, 788, 978, 1172, 1370, 1571, 1780, 1992]
with open("Results/" + exp_name + "_T.csv") as fp:
    T = [float(line) for line in fp]
with open("Results/" + exp_name + "_D.csv") as fp:
    D = [float(line) for line in fp]
D = np.array(D)
D *= 2 / (1.225 * 1.225)


fig, axs = plt.subplots()
plt.plot(t_solid,D_solid, label="Rigid")
plt.plot(t_flex, D_flex, label="Free flexible")
plt.plot(T[lim[k] + 1: lim[k + 1]], D[lim[k] + 1: lim[k + 1]], label="Controlled")
plt.ylabel(ylabel="$C_D$", fontsize=15)
plt.tick_params(axis='both', labelsize=15)
plt.yticks([0.8, 0.85, 0.9, 0.95, 1])
plt.xlabel(xlabel='T', fontsize=15)
plt.legend(loc=4, fontsize=15)
plt.tight_layout()
plt.show()
