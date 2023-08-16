import gymnasium as gym
from Aero.aero_main import *
from gymnasium import spaces


class AeroEnv(gym.Env):
    metadata = {"render_modes": "human"}

    def __init__(self, generate_mesh_flag, template_mesh, T_startup, dt_control, T_max, exp_folder, restart_folder,
                 n_probes, n_pressure, train_agent, dqn_flag):
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
        self.dqn_flag = dqn_flag

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
        if self.dqn_flag:
            self.action_space = spaces.Discrete(1001, start=-500)
        else:
            self.action_space = spaces.Box(low=-1, high=1, dtype=np.float32)

        self.old_action = self.action_space.sample()  # Initialise old_action to keep track of steps without control

        # Plot variables
        if not self.train_agent:
            self.T = []  # Time list
            self.a = []  # Action list
            self.drag = []  # Drag list
            self.r = []  # Reward list

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
        if not self.train_agent:
            self.T.append(self.T_startup)
            if self.dqn_flag:
                self.a.append(self.old_action)  # Action list
            else:
                self.a.append(self.old_action[0])  # Action list
            self.drag.append(10)  # Drag list
            self.r.append(10)  # Reward list

        aero_startup(self.T_startup, self.exp_folder, self.train_agent)
        observations = self._get_obs()
        info = self._get_info()

        # create_history(self.restart_folder)

        return observations, info

    def step(self, action):
        # Compute new T control
        self.counter += 1

        T_control = self.T_startup + self.counter * self.dt_control
        if not self.train_agent:
            self.T.append(T_control)
            if self.dqn_flag:
                self.a.append(self.old_action)  # Action list
            else:
                self.a.append(self.old_action[0])  # Action list

        # Set control parameter from action
        if self.dqn_flag:
            rho_action = self._scale_action(action)
        else:
            rho_action = action[0]
        rho = 10 ** (rho_action * 1.5 + 4.5)

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
        if not self.train_agent:
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
        return {"T_startup": self.T_startup
                }

    @staticmethod
    def _scale_action(x):
        return ((x + 500) / 500) - 1
