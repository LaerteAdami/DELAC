from System.aero_environment import AeroEnv
from stable_baselines3 import PPO
import os
import time
from gymnasium.wrappers import TransformObservation
from stable_baselines3.common.evaluation import evaluate_policy

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# SET UP
exp_name = "TEST"
training = True
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
train_agent = False

env = AeroEnv(generate_mesh,
              template_mesh,
              T_startup,
              dt_control,
              T_max,
              exp_folder,
              restart_folder,
              n_probes,
              n_pressure,
              train_agent)

episode_steps = 2

env = TransformObservation(env, lambda x: 2 * ((x - min(x)) / (max(x) - min(x))) - 1)

start_time = time.time()
# Model definition
model = PPO("MlpPolicy", env, verbose=2, batch_size=2, n_steps=episode_steps)

if training:

    # model = PPO.load(agent_name, env, verbose=2, batch_size=2,  n_steps=episode_steps)

    model.learn(total_timesteps=2)  # int(1e2), progress_bar=True)
    model.save(agent_name)


else:
    rew, std = evaluate_policy(model, env, n_eval_episodes=2)
    print(rew, std)
    print(env.drag)
    print(env.a)

print("Total time: {}".format(time.time() - start_time))
