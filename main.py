from System.aero_environment import AeroEnv
from stable_baselines3 import PPO
import os
import time
from gymnasium.wrappers import TransformObservation
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_util import make_vec_env

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Parameters
dt_num = 0.1

generate_mesh = False
template_mesh = 'Mesh/geometry_2d.template_geo'
T_startup = 40
dt_control = 1
T_max = 340
exp_folder = "Aero/Results/test_train"
restart_folder = "Aero/Results/test_train/t1"
n_probes = 15
n_pressure = 7
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

episode_steps = 2

#  env = TimeLimit(env, max_episode_steps=episode_steps)
env = TransformObservation(env, lambda x: 2*((x - min(x)) / (max(x) - min(x))) - 1)
#  obs, info = env.reset()
#  vprint(obs)

start_time = time.time()
# Model definition
model = PPO("MlpPolicy", env, verbose=2, batch_size=2,  n_steps=episode_steps)
model.learn(total_timesteps=int(1e2), progress_bar=True)
model.save("test")
print("Total time: {}".format(time.time() - start_time))


#model.load("test_train")

# vec_env = model.get_env()
# obs = vec_env.reset()
# for i in range(10):
#     action, _state = model.predict(obs, deterministic=True)
#     obs, reward, done, info = vec_env.step(action)


