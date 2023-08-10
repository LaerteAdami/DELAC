import gymnasium as gym
from Aero.aero_main import *
from gymnasium import spaces


class AeroEnv(gym.Env):
    metadata = {"render_modes": "human"}

    def __init__(self, generate_mesh_flag, template_mesh, T_startup, dt_control, T_max, exp_folder, restart_folder,
                 n_probes, n_pressure, train_agent):
        self.generate_mesh_flag = generate_mesh_flag
        self.template_mesh = template_mesh
        self.T_startup = T_startup
        self.dt_control = dt_control
        self.T_max = T_max
        self.exp_folder = exp_folder
        self.restart_folder = restart_folder
        self.n_probes = n_probes
        self.n_pressure = n_pressure
        self.train_agent = train_agent

        # Parameters for reward
        self.p1 = 0.845
        self.p2 = 10000
        self.u_max = 20
        self.u = 0

        # Parameter for step() method
        self.counter = 0
        self.truncated = False
        self.episode_number = 1

        # Observation and action spaces
        self.observation_space = spaces.Box(low=-1000, high=1000, shape=(self.n_probes * self.n_pressure,),
                                            dtype=np.float64)
        self.action_space = spaces.Box(low=-1, high=1, dtype=np.float32)

        self.old_action = self.action_space.sample()  # Initialise old_action to keep track of steps without control

        # Plot variables
        self.T = [0]  # Time list
        self.a = [self.old_action]  # Action list
        self.drag = [10]  # Drag list
        self.r = [10]  # Reward list

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.counter = 0
        self.truncated = False

        print("**************************")
        print("*** EPISODE NUMBER {}  ***".format(self.episode_number))
        print("**************************")
        self.episode_number += 1

        if self.generate_mesh_flag:
            # generate mesh
            generate_mesh(self.template_mesh)

        # Start up procedure
        # Take a random T_startup in the range [-10%, +10%] of the given T_startup
        self.T_startup = round(self.np_random.uniform(self.T_startup * 0.9, self.T_startup * 1.1, ), 1)
        self.T.append(self.T_startup)

        aero_startup(self.T_startup, self.exp_folder, self.train_agent)
        observations = self._get_obs()
        info = self._get_info()

        # create_history(self.restart_folder)

        return observations, info

    def step(self, action):
        # Compute new T control
        self.counter += 1
        self.a.append(action)
        T_control = self.T_startup + self.counter * self.dt_control

        # Set control parameter from action
        rho = 10 ** (action[0] * 1.5 + 4.5)

        # Perform aero step
        aero_step(self.restart_folder, rho, T_control, self.train_agent)
        # update_history(self.restart_folder)

        # Compute CD
        cd = get_cd(self.restart_folder)

        # Update u in case of no control step
        no_control = abs(self.old_action - action) <= 0.1
        if no_control:
            self.u += 1
        else:
            self.u = 0
        self.old_action = action  # Update old action with current action

        reward = 0.5 * cd ** 2 - self.p1 / self.p2 * (1 - self.p2 ** (self.u / self.u_max))
        self.drag.append(cd)
        self.r.append(reward)

        # returns the 5-tuple (observation, reward, terminated, truncated, info)
        if self.T_startup + (self.counter + 1) * self.dt_control >= self.T_max:
            print("##########################")
            print("####### TRUNCATED  #######")
            print("##########################")
            self.truncated = True

        # Get environment observations
        observations = self._get_obs()
        info = self._get_info()

        return observations, reward, False, self.truncated, info

    def _get_obs(self):
        """
        Private method to get observations from pressure file
        """
        return get_observations(self.restart_folder, self.n_probes, self.n_pressure)

    def _get_info(self):
        return {"T_startup": self.T_startup,
                # "T": self.T,
                # "A": self.a,
                # "CD": self.drag,
                # "R": self.r}
                # "TimeLimit.truncated": self.truncated
                }
