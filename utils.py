import os
import numpy as np


def create_history(restart_folder):
    # Create files to store history variables
    if "Drag.txt" in os.listdir(restart_folder) and "Drag_history.txt" not in os.listdir(restart_folder):
        os.rename(restart_folder + "/Drag.txt", restart_folder + "/Drag_history.txt")
        os.rename(restart_folder + "/Pressure.txt", restart_folder + "/Pressure_history.txt")
        os.rename(restart_folder + "/Time.txt", restart_folder + "/Time_history.txt")


def update_history(restart_folder):
    measures = ["Drag", "Pressure", "Time"]

    for measure in measures:
        # Reading data from new file
        with open(restart_folder + "/" + measure + ".txt") as fp:
            new_lines = fp.read()

        with open(restart_folder + "/" + measure + "_history.txt", 'r+') as fp:
            old_lines = fp.read()
            old_lines += new_lines
            fp.write(old_lines)


def get_observations(folder, n_probes, n_pressure):

    if "Pressure.txt" in os.listdir(folder):
        with open(folder + "/Pressure.txt") as fp:
            pressures = [float(line) for line in fp]
    else:
        return

    measures = int(len(pressures) / n_probes)

    id_start = 0
    if n_pressure < measures:  # Truncate pressure measurements
        id_start = abs(measures-n_pressure)

    observations = [pressures[k+id_probe*measures] for k in range(id_start, measures) for id_probe in range(n_probes)]

    return np.array(observations)


def get_cd(folder):
    with open(folder + "/Drag.txt") as f:
        drag_txt = f.readlines()

    drag = []
    for line in drag_txt:
        drag.append(float(line))

    return np.mean(drag)
