import matplotlib.pyplot as plt
exp_name = "aero_delta1_Re100_T100_results"

path = "Results/"+ exp_name +"/1/"

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

f, axs = plt.subplots()
axs.plot(time,drag, label="Re 150")
axs.set_ylim(0.5,1)
plt.xlabel("Time [s]")
plt.ylabel("Drag")


exp_name = "aero_delta1_Re150_T100_results"

path = "Results/"+ exp_name +"/1/"

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

axs.plot(time,drag, label="Re 100")
plt.legend()
plt.show()