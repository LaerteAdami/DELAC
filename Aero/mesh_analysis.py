import matplotlib.pyplot as plt

lim = 500
exp_name = ["aero_delta1_Re100_T100_results",
            "aero_delta1_Re120_T100_results",
            "aero_delta1_Re150_T100_results"]
labels = ["Re 100", "Re 120", "Re 150"]

plot_flag = True

if plot_flag:
    f, axs = plt.subplots()

for id_name, name in enumerate(exp_name):

    path = "Results/" + name + "/1/"

    with open(path+"/Drag.txt") as f:
        drag_txt = f.readlines()
    with open(path+"/Time.txt") as f:
        time_txt = f.readlines()

    drag = []
    time = []
    for line in drag_txt:
        drag.append(float(line))
    for line in time_txt:
        time.append(float(line))

    if plot_flag:

        axs.plot(time[lim:], drag[lim:], label=labels[id_name])


axs.set_ylim(0.825, 0.925)
plt.xlabel("Time [s]")
plt.ylabel("Drag")
plt.legend()
plt.show()
