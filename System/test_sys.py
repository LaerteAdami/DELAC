from aero_environment import AeroEnv
import numpy as np
import time
from gymnasium import spaces
import dolfin

import gymnasium as gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# # Parallel environments
# vec_env = make_vec_env("CartPole-v1", n_envs=1)
#
# model = PPO("MlpPolicy", vec_env, verbose=2)
# model.learn(total_timesteps=int(1e6))
# print("Done")

# obs = vec_env.reset()
# while False:
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = vec_env.step(action)
#     vec_env.render("human")

import numpy as np
x = np.array([1, 3, 4, 5, -1, -7])
# goal : range [0, 1]
x1 = (x - -1) / ( max(x) - min(x) )
print(x1)


