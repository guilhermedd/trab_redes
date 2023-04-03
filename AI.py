# Implement Q-Learn
import random

class QLearn:
     def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
          self.q = {}
          self.alpha = alpha  # learning rate
          self.gamma = gamma  # discount factor
          self.epsilon = epsilon  # exploration vs exploitation
          self.actions = ['FIGHT',
                         'RUN', 
                         'YES',
                         'NO'
                         ]

     def get_q_value(self, state, action):
          return self.q.get((state, action), 0.0)

     def learn(self, state, action, reward, next_state):
          old_value = self.q.get((state, action), None)
          if old_value is None:
               self.q[(state, action)] = reward
          else:
               next_max = max([self.get_q_value(next_state, a) for a in self.actions])
               new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
               self.q[(state, action)] = new_value

     def choose_action(self, state, event, num):
          if event == 'MONSTER_ATTACK':
               return random.randint(0, int(num))
          available_actions = ['FIGHT', 'RUN'] if event == 'BOSS_EVENT' else ['YES', 'NO']
          if random.random() < self.epsilon:
               action = random.choice(available_actions)
          else:
               q_values = [self.get_q_value(state, a) for a in available_actions]
               max_q = max(q_values)
               if q_values.count(max_q) > 1:
                    best_options = [i for i in range(len(available_actions)) if q_values[i] == max_q]
                    action_index = random.choice(best_options)
               else:
                    action_index = q_values.index(max_q)
               action = available_actions[action_index]
          return action


