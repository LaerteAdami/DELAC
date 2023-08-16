from System.aero_environment import AeroEnv
from stable_baselines3 import PPO, DQN
import os
import time
from gymnasium.wrappers import TransformObservation
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import CheckpointCallback
import matplotlib.pyplot as plt
from utils import write_result

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ['https_proxy'] = "http://hpc-proxy00.city.ac.uk:3128"

# SET UP
exp_name = "train_1"
training = False
dqn_flag = False
agent_name = "System/Agents/" + exp_name

# Parameters
generate_mesh = False
template_mesh = 'Mesh/geometry_2d.template_geo'
T_startup = 1  # 40
dt_control = 1
T_max = 2  # 240  # 340
exp_folder = "Aero/Results/" + exp_name
restart_folder = "Aero/Results/" + exp_name + "/t1"
n_probes = 15
n_pressure = 7
train_agent = training

env = AeroEnv(generate_mesh,
              template_mesh,
              T_startup,
              dt_control,
              T_max,
              exp_folder,
              restart_folder,
              n_probes,
              n_pressure,
              train_agent,
              dqn_flag)

episode_steps = 2

env = TransformObservation(env, lambda x: 2 * ((x - min(x)) / (max(x) - min(x))) - 1)

start_time = time.time()

if training:

    # Save a checkpoint every 1000 steps
    checkpoint_callback = CheckpointCallback(
        save_freq=1,
        save_path="System/Agents/",
        name_prefix=exp_name,
        save_replay_buffer=True,
        save_vecnormalize=True,
    )
    # Model definition
    if dqn_flag:
        model = DQN("MlpPolicy", env, verbose=2, batch_size=2)
        model_name = "DQN"
    else:
        model = PPO("MlpPolicy", env, verbose=2, batch_size=2, n_steps=episode_steps)
        model_name = "PPO"

    print("+++ Training model {}: {} +++".format(model_name, exp_name))
    model.learn(total_timesteps=2, callback=checkpoint_callback)
    model.save(agent_name)

else:
    # Model definition
    if dqn_flag:
        model = DQN.load(agent_name, env, verbose=2, batch_size=2,  n_steps=episode_steps)
        model_name = "DQN"
    else:
        model = PPO.load(agent_name, env, verbose=2, batch_size=2,  n_steps=episode_steps)
        model_name = "DQN"

    print("+++ Evaluating model {}: {} +++".format(model_name, exp_name))

    rew, std = evaluate_policy(model, env, n_eval_episodes=2)

    # Plots
    T = env.T
    D = env.drag
    a = env.a
    write_result("System/Results/"+exp_name+"_T.csv", T)
    write_result("System/Results/"+exp_name+"_D.csv", D)
    write_result("System/Results/"+exp_name+"_a.csv", a)

print("Total time: {}".format(time.time() - start_time))
