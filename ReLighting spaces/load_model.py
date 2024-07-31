import socket
import struct
import pickle
import numpy as np
import gymnasium as gym
from gymnasium.spaces import Discrete, MultiDiscrete 
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
import os


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
        length = struct.unpack("<L", self._buffer[:4])[0] 
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

   
    # upgraded with seed parameter
    def reset(self, seed=None):
    # def reset(self):
        super().reset(seed=seed) # 
        self._conn.send_object("reset")
        info = {} # 
        msg = self._conn.receive_object()
        self.action_space = eval(msg["info"]["action_space"])
        self.observation_space = eval(msg["info"]["observation_space"])
        return msg["observation"], info
     

    def step(self, action):
        self._conn.send_object(action.tolist())
        msg = self._conn.receive_object()
        obs = msg["observation"]
        rwd = msg["reward"]
        terminated = msg["terminated"] 
        truncated = msg["truncated"] 
        info = msg["info"]
        initial_reward = msg["initial_reward"]
        return obs, rwd, terminated, truncated, info, initial_reward
        

    def close(self):
        self._conn.send_object("close")
        self._socket.close()

#Set num_cells (voxel space dimensions)
num_cells = 250
log_path = os.path.join('Training', 'Logs')
addr = ("127.0.0.1", 50710)
env = Env(addr)
env.reset()

#Load model
PPO_path = os.path.join ('Training', 'Saved Models','PPO_Model_SA_2.0')
model = PPO.load(PPO_path, env = env)


#Test model
cum_rwd = 0
cum_init_rwd = 0
obs, info = env.reset()
for i in range(100000):
    action, _states = model.predict(obs,deterministic=False)
    obs, reward, terminated, truncated, info, initial_reward = env.step(action)
    cum_rwd += reward
    cum_init_rwd += initial_reward
    print (reward)
   
    if terminated or truncated:
        print("Terminated = ", terminated, "; Truncated = ", truncated, end = "; ")
        obs, info = env.reset()
        print("Return = ", cum_rwd)
        print("Initi rew = ", cum_init_rwd )
        print("Sunhours rew = ", cum_rwd - cum_init_rwd )
        cum_rwd = 0
        break
    else:
        print("Return = ", cum_rwd)
env.close()

