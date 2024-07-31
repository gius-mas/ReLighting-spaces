import socket
import struct
import pickle
import numpy as np
#import gymnasium as gym
import gymnasium as gym
from gymnasium.spaces import Discrete, MultiDiscrete, Box, Tuple #new line added GM
#from stable_baselines3 import SAC
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
import os
# old lines commented below updated ones

class Connection:
    def __init__(self, s):
        self._socket = s
        self._buffer = bytearray()

    def receive_object(self):
        while len(self._buffer) < 4 or len(self._buffer) < struct.unpack("<L", self._buffer[:4])[0] + 4:
            new_bytes = self._socket.recv(16)
            if len(new_bytes) == 0:
                return None
            self._buffer += new_bytes
        length = struct.unpack("<L", self._buffer[:4])[0] # struct requires a buffer of 4 bytes
        header, body = self._buffer[:4], self._buffer[4:length + 4]
        obj = pickle.loads(body)
        self._buffer = self._buffer[length + 4:]
        return obj

    def send_object(self, d):
        body = pickle.dumps(d, protocol=2)
        header = struct.pack("<L", len(body))
        msg = header + body
        self._socket.send(msg)


class Env(gym.Env):
    def __init__(self, addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(addr)
        s.listen(1)
        clientsocket, address = s.accept()

        self._socket = clientsocket
        self._conn = Connection(clientsocket)

        self.action_space = None
        self.observation_space = None

    # see https://gymnasium.farama.org/content/migration-guide/
    # upgraded with seed parameter
    def reset(self, seed=None):
    # def reset(self):
        super().reset(seed=seed) # ----------------------------- new line added
        self._conn.send_object("reset")
        info = {} # ----------------------------- new line added
        msg = self._conn.receive_object()
        self.action_space = eval(msg["info"]["action_space"])
        self.observation_space = eval(msg["info"]["observation_space"])
        return msg["observation"], info
        # return msg["observation"]

    def step(self, action):
        self._conn.send_object(action.tolist())
        msg = self._conn.receive_object()
        obs = msg["observation"]
        rwd = msg["reward"]
        terminated = msg["terminated"] # ----------------------------- new line added
        truncated = msg["truncated"] # ----------------------------- new line added
        # done = msg["done"]
        info = msg["info"]
        return obs, rwd, terminated, truncated, info
        # return obs, rwd, done, info

    def close(self):
        self._conn.send_object("close")
        self._socket.close()


#crea la directory per il salvataggio del modello e il log in tensor board
log_path = os.path.join('Training', 'Logs')
addr = ("127.0.0.1", 50710)
env = Env(addr)
num_cells = 250
env.reset()

#Training

print("Training model", end = " ")
model = PPO('MlpPolicy', env, verbose=1, tensorboard_log = log_path, device = "cuda") #----new line GM
model.learn(total_timesteps=100000, log_interval=4)
print("Training done")
PPO_path = os.path.join ('Training', 'Saved Models','PPO_Model_SA_1.1_100k')
model.save(PPO_path)



#Test model
cum_rwd = 0
obs, info = env.reset()
# obs = env.reset()
for i in range(2000):
    action, _states = model.predict(obs,deterministic=False)
    obs, reward, terminated, truncated, info = env.step(action)
    # obs, reward, done, info = env.step(action)
    cum_rwd += reward
    print (reward)
    if terminated or truncated:
    # if done:
        print("Terminated = ", terminated, "; Truncated = ", truncated, end = "; ")
        obs, info = env.reset()
        # obs = env.reset()
        print("Return = ", cum_rwd)
       
        cum_rwd = 0
        break
    else:
        print("Return = ", cum_rwd)
env.close()




