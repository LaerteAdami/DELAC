import os
import time
from stable_baselines3 import PPO, DQN
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import CheckpointCallback
from gymnasium.wrappers import TransformObservation
# Custom functionalities
from System.aero_environment import AeroEnv
from utils import write_result

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ['https_proxy'] = "http://hpc-proxy00.city.ac.uk:3128"

# SET UP PARAMETERS
exp_name = "dqn_fi"                                     # Name of the experiment
training = True                                         # Training flag: True - train / False - evaluate
dqn_flag = True                                         # DQN flag: True - use DQN / False - use PPO

# MAIN PARAMETERS OF THE TRAINING PROCESS
generate_mesh = False                                   # True / False to generate the mesh from skratch
template_mesh = 'Mesh/geometry_2d.template_geo'         # Template of the mesh to be generated
T_startup = 40                                          # Time to start up the system
dt_control = 0.5                                        # Time interval between two actions
T_max = 140                                             # Time to truncate an episode
n_probes = 5                                            # Number of probes to consider --> SEE LINE 134 in run_aero.py
n_pressure = 5                                          # Pressure points to consider
learning_rate = 0.001                                   # Learning rate
max_steps = 10000                                       # Maximum numbers of steps to train

# FOLDERS AND TRAINING FLAG
agent_name = "System/Agents/" + exp_name                # Folder to save the agent trained
exp_folder = "Aero/Results/" + exp_name                 # Folder to save the aerodynamic results
restart_folder = "Aero/Results/" + exp_name + "/t1"     # Folder to save the aerodynamic results
train_agent = training

# CREATION OF THE AERODYNAMIC ENVIRONMENT
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
episode_steps = 2  # Standard value

# SELECT THE TRANSFORMATION OF THE OBSERVATION
obs_trans = 1
match obs_trans:
    case 0:  # NO OBS TRANSFORMATION
        pass
    case 1:  # T1 - between [-1, +1]
        env = TransformObservation(env, lambda x: 2 * ((x - min(x)) / (max(x) - min(x))) - 1)
    case 2:  # T2 - between [0, +1]
        env = TransformObservation(env, lambda x: ((x - min(x)) / (max(x) - min(x))))

# SELECT THE NUMBER OF HIDDEN NODES
hidden_nodes = 1
match hidden_nodes:
    case 0:  # NO OBS TRANSFORMATION
        policy_kwargs = None
    case 1:  # T1 - between [-1, +1]
        policy_kwargs = dict(net_arch=[128, 128])
    case 2:  # T2 - between [0, +1]
        policy_kwargs = dict(net_arch=[256, 256])
    case _:
        policy_kwargs = None

# START TIME
start_time = time.time()

if training:  # START TRAINING PROCEDURE

    # Save a checkpoint every 1000 steps
    checkpoint_callback = CheckpointCallback(
        save_freq=1000,
        save_path="System/Agents/",
        name_prefix=exp_name,
        save_replay_buffer=True,
        save_vecnormalize=True,
    )
    # Model definition
    if dqn_flag:  # Train DQN model
        model = DQN("MlpPolicy", env,
                    verbose=2,
                    batch_size=2,
                    tensorboard_log="./log_tensorboard/{}/".format(exp_name),
                    policy_kwargs=policy_kwargs,
                    learning_rate=learning_rate)
        model_name = "DQN"
    else:  # Train PPO model
        model = PPO("MlpPolicy", env,
                    verbose=2,
                    batch_size=2,
                    n_steps=episode_steps,
                    tensorboard_log="./log_tensorboard/{}/".format(exp_name),
                    policy_kwargs=policy_kwargs,
                    learning_rate=learning_rate)
        model_name = "PPO"

    print("+++ Training model {}: {} +++".format(model_name, exp_name))
    print(model.policy)
    model.learn(total_timesteps=int(max_steps), callback=checkpoint_callback)
    model.save(agent_name)

else:  # START EVALUATION PROCEDURE
    # Model definition
    if dqn_flag:
        model = DQN.load(agent_name, env, verbose=2, batch_size=2, n_steps=episode_steps)
        model_name = "DQN"
    else:
        model = PPO.load(agent_name, env, verbose=2, batch_size=2, n_steps=episode_steps)
        model_name = "PPO"

    print("+++ Evaluating model {}: {} +++".format(model_name, exp_name))
    print(model.policy)
    # Evaluate the policy
    rew, std = evaluate_policy(model, env, n_eval_episodes=10)

    # Save the results in csv files
    T = env.T
    D = env.drag
    a = env.a
    r = env.r
    write_result("System/Results/" + exp_name + "_T.csv", T)
    write_result("System/Results/" + exp_name + "_D.csv", D)
    write_result("System/Results/" + exp_name + "_a.csv", a)
    write_result("System/Results/" + exp_name + "_r.csv", r)

print("Total time: {}".format(time.time() - start_time))
