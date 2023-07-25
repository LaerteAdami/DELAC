import matplotlib.pyplot as plt
import scipy.signal
from scipy.fft import fft
import numpy as np

exp = 5
plot_flag = True
plot_freq = False

if exp == 1:  # Test different Reynolds number

    exp_name = ["aero_delta1_Re100_T100_results",
                "aero_delta1_Re120_T100_results",
                "aero_delta1_Re150_T100_results"]
    labels = ["Re 100", "Re 120", "Re 150"]
    lim = [int(80 / 0.1), int(80 / 0.1), int(80 / 0.1)]
    dt = [0.1, 0.1, 0.1]


elif exp == 2:  # Test different mesh dimension

    exp_name = ["aero_delta1_Re150_T100_results",
                "aero_delta2_Re150_T100_results",
                "aero_delta05_Re150_T100_results"]
    labels = ["Delta 1", "Delta 2", "Delta 0.5"]
    lim = [int(80 / 0.1), int(80 / 0.2), int(80 / 0.05)]
    dt = [0.1, 0.2, 0.05]


elif exp == 3:  # Test different domain dimension

    exp_name = ["aero_delta2_Re150_T100_results",
                "aero_delta2_len075_Re150_T100_results",
                "aero_delta2_len05_Re150_T100_results"]
    lim = [int(80 / 0.2), int(80 / 0.2), int(80 / 0.2)]

    labels = ["Len 1", "Len 0.75", "Len 0.5"]
    dt = [0.2, 0.2, 0.2]

elif exp == 4:  # Final comparison

    exp_name = ["aero_delta1_Re150_T100_results",
                "aero_delta1_len075_Re150_T100_results",
                "aero_delta05_Re150_T100_results",
                "aero_delta05_len075_Re150_T100_results"]
    lim = [int(80 / 0.1), int(80 / 0.1), int(80 / 0.05), int(80 / 0.05)]

    labels = ["Medium grid, Big Domain", "Medium grid, Medium Domain",
              "Fine grid, Big Domain", "Fine grid, Medium Domain"]
    dt = [0.1, 0.1, 0.05, 0.05]

    colors = ["royalblue", "royalblue", "coral", "coral"]
    linestyles = ["-", "--", "-", "--"]

elif exp == 5: # Different density

    exp_name = ["aero_delta1_len075_Re150_T100_results",
                "test_solid_4_disp_vel",
                "test_solid_5_disp_vel",
                "test_solid_6_disp_vel",
                "test_solid_7_disp_vel",
                "test_solid_8_disp_vel"]

    lim = [int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1)]

    labels = ["No solid",
              "Rho 2e2", "Rho 2e3", "Rho 2e4","Rho 2e5","Rho 2e6"]
    dt = [0.1, 0.1, 0.1, 0.1, 0.1,0.1, 0.1]

    colors = ["royalblue", "red", "royalblue", "green", "black"]
    linestyles = ["-", "-", "-", "-", "-", "-"]

elif exp == 6: # Different lenghts

    exp_name = ["aero_delta1_len075_Re150_T100_results",
                "test_solid_7_disp_vel",
                "test_solid_10_disp_vel",
                "test_solid_11_disp_vel"]

    lim = [int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1)]

    labels = ["No solid",
              "L 1", "L 1.2", "L 1.5","Rho 2e5","Rho 2e6"]
    dt = [0.1, 0.1, 0.1, 0.1, 0.1,0.1, 0.1]

    colors = ["royalblue", "red", "royalblue", "green", "black"]
    linestyles = ["-", "-", "-", "-", "-", "-"]

elif exp == 7: # Different widths and lengths
    exp_name = ["aero_delta1_len075_Re150_T100_results",
                "test_solid_7_disp_vel",
                "test_solid_10_disp_vel",
                "test_solid_11_disp_vel",
                "test_solid_12_disp_vel",
                "test_solid_13_disp_vel",
                "test_solid_14_disp_vel"]

    lim = [int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1)]

    labels = ["No solid",
              "W 0.1 L 1","W 0.1 L 1.2","W 0.1 L 1.5", "W 0.2 L 1","W 0.2 L 1.2","W 0.2 L 1.5"]
    dt = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    colors = ["royalblue", "tan", "gold", "skyblue", "tan", "gold", "skyblue"]
    linestyles = ["-", "-", "-", "-", "--", "--", "--", "-", "-"]

elif exp == 8: # Different widths and lengths
    exp_name = ["aero_delta1_len075_Re150_T100_results",
                "test_solid_14_disp_vel",
                "test_solid_15_disp_vel",
                "test_solid_16_disp_vel"
                ]

    lim = [int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1), int(80 / 0.1)]

    labels = ["No solid",
              "Rho 2e5","Rho 2.5e5","Rho 5e5", "W 0.2 L 1","W 0.2 L 1.2","W 0.2 L 1.5"]
    dt = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    colors = ["royalblue", "tan", "gold", "skyblue", "tan", "gold", "skyblue"]
    linestyles = ["-", "-", "-", "-", "--", "--", "--", "-", "-"]

if plot_flag:
    f, axs = plt.subplots()

for id_name, name in enumerate(exp_name):

    path = "Results/" + name + "/1/"

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

    D = drag[lim[id_name]:]
    t = time[lim[id_name]:]

    if plot_flag:
        axs.plot(t, D, label=labels[id_name], linestyle=linestyles[id_name])#, color=colors[id_name])

    dt_name = dt[id_name]
    L = np.round(D, 4)
    meanD = np.mean(D)

    D -= meanD
    # Window signal
    D *= scipy.signal.windows.hann(len(D))

    fftD = fft(D)

    freq_fftx = np.linspace(0, 1 / dt_name, len(fftD))

    if plot_freq:
        f, axs = plt.subplots()
        plt.plot(t, L)
        plt.show()
        f, axs = plt.subplots()
        plt.plot(freq_fftx, abs(fftD))
        plt.show()

    print("Case {}, Mean: {}, Freq: {}".format(name, round(meanD, 3), freq_fftx[np.argmax(abs(fftD))]))

#axs.set_ylim(0.65, 0.75)
plt.xlabel("Time [s]")
plt.ylabel("Drag")
plt.legend()
plt.savefig("mesh_analysis.png")
plt.show()
