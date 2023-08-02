from gymnasium.envs.registration import register

register(
id="AeroEnv-v0",
entry_point="gym_examples.envs:AeroEnv",
max_episode_steps=300
)