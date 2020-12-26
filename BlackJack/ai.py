import copy
import random

from game import Game, states

HIT = 0
STAND = 1
DISCOUNT = 0.95  # This is the gamma value for all value calculations
EPSILON = 0.4

class Agent:
    def __init__(self):

        # For MC values
        self.MC_values = {}  # Dictionary: Store the MC value of each state
        self.S_MC = {}      # Dictionary: Store the sum of returns in each state
        self.N_MC = {}      # Dictionary: Store the number of samples of each state
        # MC_values should be equal to S_MC divided by N_MC on each state (important for passing tests)

        # For TD values
        self.TD_values = {}  # Dictionary storing the TD value of each state
        self.N_TD = {}       # Dictionary: Store the number of samples of each state

        # For Q-learning values
        self.Q_values = {}   # Dictionary storing the Q-Learning value of each state and action
        self.N_Q = {}        # Dictionary: Store the number of samples of each state

        # Initialization of the values
        for s in states:
            self.MC_values[s] = 0
            self.S_MC[s] = 0
            self.N_MC[s] = 0
            self.TD_values[s] = 0
            self.N_TD[s] = 0
            # First element is the Q value of "Hit", second element is the Q value of "Stand"
            self.Q_values[s] = [0, 0]
            self.N_Q[s] = 0
        # NOTE: see the comment of `init_cards()` method in `game.py` for description of game state
        self.simulator = Game()

    # NOTE: do not modify
    # This is the policy for MC and TD learning.
    @staticmethod
    def default_policy(state):
        user_sum = state[0]
        user_A_active = state[1]
        actual_user_sum = user_sum + user_A_active * 10
        if actual_user_sum < 14:
            return 0
        else:
            return 1

    # NOTE: do not modify
    # This is the fixed learning rate for TD and Q learning.
    @staticmethod
    def alpha(n):
        return 10.0/(9 + n)

    def MC_run(self, num_simulation, tester=False):

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):
            # Do not modify the following three lines
            if tester:
                self.tester_print(simulation, num_simulation, "MC")
            self.simulator.reset()  # Restart the simulator

            # TODO: Remove the following dummy updates and implement MC-learning
            # Note: Do not reset the simulator again in the rest of this simulation
            # Hint: Simulate a full episode using "self.simulator.simulate_sequence(...)"
            episode = self.simulator.simulate_sequence(
                policy=self.default_policy)

            for i in range(len(episode)):

                state, _ = episode[i]
                sum_of_return = 0
                for j in range(i, len(episode)):
                    _, reward = episode[j]

                    sum_of_return += (DISCOUNT**(j-i)) * reward

                self.S_MC[state] += sum_of_return
                self.N_MC[state] += 1
                self.MC_values[state] = self.S_MC[state] / self.N_MC[state]

            # Hint: You need to compute reward-to-go for each state in the episode
            # Useful variables:
            #     - DISCOUNT
            #     - self.MC_values     (read comments in self.__init__)

    def TD_run(self, num_simulation, tester=False):
        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):
            # Do not modify the following three lines
            if tester:
                self.tester_print(simulation, num_simulation, "TD")
            self.simulator.reset()

            # TODO: Remove the following dummy updates and implement TD-learning
            # Note: Do not reset the simulator again in the rest of this simulation
            # Hint: You need a loop that takes one step simulation each time, until state is "None" which indicates termination
            s = self.simulator.state

            while s is not None:
                action = self.default_policy(s)
                reward = self.simulator.check_reward()
                next_s, _ = self.simulator.simulate_one_step(action)
                
                self.N_TD[s] += 1

                if next_s is not None:
                    self.TD_values[s] += self.alpha(self.N_TD[s]) * (reward + DISCOUNT * self.TD_values[next_s] - self.TD_values[s])
                else:
                    self.TD_values[s] += self.alpha(self.N_TD[s]) * (reward - self.TD_values[s])

                s = next_s

            # Hint: current state can be accessed by "self.simulator.state"
            # Hint: Simulate one step using "self.simulator.simulate_one_step(...)"
            # Hint: The learning rate alpha is given by "self.alpha(...)"
            # Useful variables:
            #     - DISCOUNT
            #     - self.TD_values  (read comments in self.__init__)

    def Q_run(self, num_simulation, tester=False):
        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):
            # Do not modify the following three lines
            if tester:
                self.tester_print(simulation, num_simulation, "Q")
            self.simulator.reset()

            # TODO: Remove the following dummy update and implement Q-learning
            # Note: Do not reset the simulator again in the rest of this simulation
            # Hint: You need a loop that takes one step simulation each time, until state is "None" which indicates termination

            s = self.simulator.state

            while s is not None:
                action = self.pick_action(s, EPSILON)
                reward = self.simulator.check_reward()
                next_s, _ = self.simulator.simulate_one_step(action)
                
                self.N_Q[s] += 1

                if next_s is not None:
                    self.Q_values[s][action] += self.alpha(self.N_Q[s]) * (reward + DISCOUNT * max(self.Q_values[next_s][HIT], self.Q_values[next_s][STAND]) - self.Q_values[s][action]) 
                else:
                    self.Q_values[s][action] += self.alpha(self.N_Q[s]) * (reward - self.Q_values[s][action]) 

                s = next_s

            # Hint: current state can be accessed by "self.simulator.state"
            # Hint: Simulate one step using "self.simulator.simulate_one_step(...)"
            # Hint: The learning rate alpha is given by "self.alpha(...)"
            # Hint: Implement epsilon-greedy method in "self.pick_action(...)"
            # Useful variables:
            #     - DISCOUNT
            #     - self.Q_values  (read comments in self.__init__)

    def pick_action(self, s, epsilon):
        # Replace the following random return value with the epsilon-greedy strategy
        # Hint: Generate a random number with `random.random()` and compare with epsilon
        # Hint: A random action is just `random.randint(0,1)`
        if random.random() < epsilon:
            return random.randint(0, 1)
        else:
            return HIT if self.Q_values[s][0] > self.Q_values[s][1] else STAND 

    # Note: do not modify
    def autoplay_decision(self, state):
        hitQ, standQ = self.Q_values[state][HIT], self.Q_values[state][STAND]
        if hitQ > standQ:
            return HIT
        if standQ > hitQ:
            return STAND
        return HIT  # Before Q-learning takes effect, just always HIT

    # NOTE: do not modify
    def save(self, filename):
        with open(filename, "w") as file:
            for table in [self.MC_values, self.TD_values, self.Q_values, self.S_MC, self.N_MC, self.N_TD, self.N_Q]:
                for key in table:
                    key_str = str(key).replace(" ", "")
                    entry_str = str(table[key]).replace(" ", "")
                    file.write(f"{key_str} {entry_str}\n")
                file.write("\n")

    # NOTE: do not modify
    def load(self, filename):
        with open(filename) as file:
            text = file.read()
            MC_values_text, TD_values_text, Q_values_text, S_MC_text, N_MC_text, NTD_text, NQ_text, _ = text.split(
                "\n\n")

            def extract_key(key_str):
                return tuple([int(x) for x in key_str[1:-1].split(",")])

            for table, text in zip(
                [self.MC_values, self.TD_values, self.Q_values,
                    self.S_MC, self.N_MC, self.N_TD, self.N_Q],
                [MC_values_text, TD_values_text, Q_values_text,
                    S_MC_text, N_MC_text, NTD_text, NQ_text]
            ):
                for line in text.split("\n"):
                    key_str, entry_str = line.split(" ")
                    key = extract_key(key_str)
                    table[key] = eval(entry_str)

    # NOTE: do not modify
    @staticmethod
    def tester_print(i, n, name):
        print(f"\r  {name} {i + 1}/{n}", end="")
        if i == n - 1:
            print()
