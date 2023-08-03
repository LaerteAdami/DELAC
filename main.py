from System.aero_environment import AeroEnv
from stable_baselines3 import PPO
import os
import time
from gymnasium.wrappers import TimeLimit
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Parameters
generate_mesh = False
template_mesh = 'Mesh/geometry_2d.template_geo'
T_startup = 1
dt_control = 0.5
T_max = 11
exp_folder = "Aero/Results/test_env_new"
restart_folder = "Aero/Results/test_env_new/t1"
n_probes = 2
n_pressure = 1
train_agent = True

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

env = TimeLimit(env, max_episode_steps=10)

start_time = time.time()
# Model definition
model = PPO("MlpPolicy", env, verbose=2)
model.learn(total_timesteps=1000, progress_bar=True)
model.save("test")
#

print("Total time: {}".format(time.time() - start_time))
# vec_env = model.get_env()
# obs = env.reset()

# check_env(env)
