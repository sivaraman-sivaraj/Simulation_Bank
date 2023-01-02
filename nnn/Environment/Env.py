import numpy as np
import MMG,LOS,Reward
import random_path_generation
from   gym import Env
from gym import spaces
from gym.utils import seeding
import wp_analysis

#####################################
##### Environment Construction ######
##################################### 

class load(Env):
    def __init__(self,W_Flag):
        super(load, self).__init__()
        self.W_Flag         = W_Flag
        self.u              = 0.78
        #######################################################################
        self.delta_min  = np.array([-1.0,-1.0])
        self.delta_max  = np.array([ 1.0,1.0])
        self.action_space = spaces.Box(low=self.delta_min, high=self.delta_max, shape=(2,))
        #######################################################################
        high_arr = np.array([ 0.12,np.pi,36,0.78])
        low_arr = np.array([-0.12,-np.pi,-36,-0.78])
        self.observation_space = spaces.Box(low=low_arr, high=high_arr, shape=(4,))
        self.seed(1)
        #######################################################################
        self.current_state = np.zeros(self.observation_space.shape[0])
        self.viewer        = None
        #######################################################################
        ######################### Results Plotting ############################
        #######################################################################
        self.Epi_rewards = []
        self.step_count  = 0.0
        
        
    def reset(self):
        self.WHA             = np.deg2rad(np.random.randint(-180,180))
        self.done            = False 
        self.step_count      = 0
        ########## Random Own Ship Path Generation ##########
        self.wp,self.X,self.Y,self.L   = random_path_generation.straight_line(150, 45)
        self.wpA                       = wp_analysis.activate(self.wp)
        self.cum_reward                = 0.
        #######################################################################
        self.St_angle     = np.arctan2((self.wp[2][1]-self.wp[0][1]),(self.wp[2][0]-self.wp[0][0]))
        self.psi          = 0.0
            
        self.RusPos       = 0.
        self.PropPos      = 5.0
        self.S_wp               = self.wpA[1][1]
        self.goal               = LOS.goal_setter([0,0], self.S_wp)
        self.H                  = [0,0,self.goal]
        self.done               = False
        self.state_mmg          = [self.u,0.0,0.0,0.0,0.0,self.psi,0.0,0.0]
        self.u_d                = 0.78
        self.current_state      = [0.,-self.St_angle,0.0,0.0]
        return np.array(self.current_state)
    
    def step(self,U):
        self.step_count +=1
        self.delta_d      = U[0]*np.deg2rad(15)
        self.delta_rps    = U[1]*5
        self.op,self.RuPos_new, self.PropPos_new  = MMG.activate(self.state_mmg,self.delta_d, self.delta_rps,
                                                                 self.W_Flag,self.WHA,self.RusPos,self.PropPos)
        
        self.HE,self.CTE,self.H,self.u_d     = LOS.activate(self.op,self.wpA,self.H)
        self.reward                          = Reward.get(self.HE,self.CTE,self.op[0],self.u_d)
        self.u_error                         = self.op[0] - self.u_d
        #################################
        ###### Next State Update ########
        #################################
        self.current_state  = [self.op[2],self.HE,self.CTE,self.u_error]
        self.state_mmg      = self.op
        self.RusPos         = self.RuPos_new
        self.PropPos        = self.PropPos_new
        self.cum_reward     += self.reward
        #################################
        ### Epi Termination Creteria ####
        #################################
        if abs(self.HE) > 175:
            self.done = True
        if self.CTE > 36 :
            self.done = True
        if self.step_count > 250:
            self.done = True
        
        self.last_H =  [len(self.wpA[1][0]),len(self.wpA[1][1][-1])]
        
        if self.H[0] == self.last_H[0] and self.H[1] == self.last_H[1]:
            self.done = True
        #####################################
        
        
        if self.done == True:
            self.Epi_rewards.append(self.cum_reward)
        self.info = {}
        return np.array(self.current_state), self.reward, self.done,self.info
            
    def action_space_sample(self):
        d = np.random.choice([-1,1])*np.random.rand()*np.deg2rad(15)
        return round(d,4)
    
    def action_space(self):
        return np.arange(-1,2,1)
    
    def render(self):
        pass
    def close():
        pass
     
    
#######################################################
#######################################################
# ss = load(True)
# dd = ss.reset()
# # print(dd)
# for _ in range(10):
#     a,b,c,d = ss.step([0.0])
# print(a)
#######################################################
#######################################################

        
        
        
        
     

