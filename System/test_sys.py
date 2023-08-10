import os
from importlib.metadata import packages_distributions
from importlib import import_module


test = packages_distributions()["stable_baselines3"]
print(test)
import_module("stable_baselines3", test[0])
import_module()
#from (stable-baselines3) import PPO
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






