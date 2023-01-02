#######################################################
############### Read Me First #########################
#######################################################
## There are various DRL algorithms are about to train
## 1. DDPG - Deep Deterministic Policy Gradients
## 2.
## 3. 
#######################################################
#######################################################
import os,sys,pathlib,random
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
sys.path.insert(1,os.path.join(os.getcwd(),pathlib.Path("Environment")))
import Env
import gym
import numpy as np
import torch, torch.nn as nn
from gym.envs.registration import register
import stable_baselines3
from stable_baselines3 import DDPG
from stable_baselines3.common.env_util import make_vec_env
import matplotlib.pyplot as plt
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise
##################################################
##### Registering the Environment in Gym #########
##################################################
env_dict = gym.envs.registration.registry.env_specs.copy()
for env in env_dict:
      if 'NavigationRL-v0' in env:
          del gym.envs.registration.registry.env_specs[env]

register(id ='NavigationRL-v0', entry_point='Environment.Env:load',kwargs={'W_Flag' : False})
#####################################################
######### Initialization of Networks and Params #####
#####################################################
env                     = gym.make('NavigationRL-v0')


# The noise objects for DDPG
n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

policy_kwargs = dict(activation_fn= torch.nn.Tanh,net_arch=[128,128])

model = DDPG("MlpPolicy", env,policy_kwargs = policy_kwargs, action_noise=action_noise, verbose=1)
model.learn(total_timesteps=100000, log_interval=10)
model.save("DDPG_NavigationRL_waves_1_250")

######################################################
############ Results Saving and Plotting #############
######################################################
Episode_rewards = env.Epi_rewards
np.save("DDPG_rewards_waves_1_250_tanh.npy",Episode_rewards)

plt.figure(figsize=(9,6))
running_avg = np.empty(len(Episode_rewards))
for t in range(len(Episode_rewards)):
        running_avg[t] = np.mean(Episode_rewards[max(0, t-100):(t+1)])
plt.plot(Episode_rewards,color="teal",alpha=0.2)
plt.plot(running_avg,color="teal",linewidth=2.0)
plt.ylabel("Reward Units")
plt.xlabel("No. of Episode")
plt.title("Deep Deterministic Policy Gradient (DDPG)")
plt.grid()
plt.savefig("DDPG_Rewards_waves_1_250_tanh.jpg",dpi = 420)
plt.show()
######################################################
######################################################







