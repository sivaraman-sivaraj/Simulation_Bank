import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import pylab 


##################################################
##################################################
##################################################
def Point_Maker(X,Y):
    WP     = list()
    for i in range(len(X)):
        temp = [X[i],Y[i]]
        WP.append(temp)
    return WP

def Rotate(WP,theta):
    R = np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]]) 
    temp = np.array(WP).T
    WP_r   = np.matmul(R,temp)
    return WP_r.T


def Distance(A,B):
    D = np.sqrt(np.square(A[0]-B[0]) + np.square(A[1]-B[1]))
    return D

def interpretval(P1,P2,intv):
    a,b    = np.array(P1), np.array(P2)
    DV_    = b-a
    DV     = DV_/np.linalg.norm(DV_)
    l,m    = DV[0],DV[1]
    newpt  = [intv*l+P1[0],intv*m+P1[1]]
    return newpt

def Eq_Distance_maker(wp,lbp):
    WP_es = [wp[0]]
    
    current_pnt = wp[0]
    index_first = 1
    
    k           = 0
    
    Tot_dis     = 0
    for ii in range(len(wp)-1):
        temp     = Distance(wp[ii],wp[ii+1])
        Tot_dis += temp
        
    Int_Ds      = lbp
    NP          = int(Tot_dis / Int_Ds)
    
    for k in range(NP):
        New_presence   = []
        dis_sum   = 0
        pt_now    = current_pnt
        kk        = 0
        pt_target = wp[index_first]
        remainder = Int_Ds
        while len(New_presence) == 0:
            dis_temp = Distance(pt_now,pt_target)
            dis_sum  += dis_temp
            if dis_sum >= Int_Ds:
                newpt  = interpretval(pt_now,pt_target,remainder)
                New_presence.append(newpt)
            else:
                remainder -= dis_temp
                pt_now     = pt_target
                kk        += 1
                if index_first + kk > len(wp):
                    newpt  = wp[-1]
                    New_presence.append(newpt)
                else:
                    pt_target = wp[index_first+kk]
        WP_es.append(newpt)
        current_pnt   = newpt
        index_first   += kk
    return WP_es

##################################################
################## Straight Line #################
##################################################

def straight_line(inertial_frame_limit,theta):
        """
        Parameters
        ----------
        inertial_frame_limit : required way points range
        
        Returns
        -------
        wp : waypoints
        -------
        Warning:
            Heading Angle should be in a range of (-90) to (90) degree
        """
        lbp   = 1
        ### Assertion ###
        if theta > 180 :
            theta = theta - 360
        elif theta < -180:
            theta = theta + 360
        
        #################################
        #### path reward Declaration ####
        #################################
        a = (theta/180) * np.pi # radian mode
        wp = list() # path reward points
        # starting_point = [0,0] #starting point of the ship
        # prp.append(starting_point)
        
        if -45 <= theta <= 45:
            for e in range(inertial_frame_limit):
                y_t = e*(np.tan(a))
                if abs(y_t) < abs(inertial_frame_limit):
                    temp = [e,y_t]
                    wp.append(temp)
        elif -135 >= theta >= -180 or 135 <= theta <= 180:
            for e in range(inertial_frame_limit):
                y_t = -e*(np.tan(a))
                if abs(y_t) < inertial_frame_limit:
                    if e == 0:
                        temp = [e,-y_t]
                    else:
                        temp = [-e,y_t]
                    wp.append(temp)
                        
        elif 45 < theta < 135 :
            for e in range(inertial_frame_limit):
                x_t = -e/(np.tan(a))
                if abs(x_t) < inertial_frame_limit:
                    temp = [-x_t,e]
                    wp.append(temp)
        elif -45 > theta > -135 :
            for e in range(inertial_frame_limit):
                x_t = -e/(np.tan(a))
                if abs(x_t) < inertial_frame_limit:
                    temp = [x_t,-e]
                    wp.append(temp)
        
        
        ############################
        #### path reward end #######
        ############################ 
        x,y = list(),list()
        for i in range(len(wp)):
            x.append(wp[i][0])
            y.append(wp[i][1])
       
        x = x[::]
        y = y[::]
        
        ### Length of Trajectory ###
        L = np.sqrt((wp[-1][0]**2) + (wp[-1][1]**2))
        S_wp = Eq_Distance_maker(wp,lbp)
        #############################################
        WPV = list()
        for i in range(len(S_wp)):
            
            if i < int(len(S_wp)/2):
                u = 0.8
            else:
                u = 0.9
            temp = [S_wp[i][0],S_wp[i][1],u]
            WPV.append(temp)
        
        return WPV,x,y,L

##################################################
##################################################
##################################################
def polycurve(theta,n,l = 500):
    X_R      = np.random.randint(-500,1000,200)
    Y_R      = np.random.randint(-500,1000,200)
    lbp      = 3
    Model    = pylab.polyfit(X_R, Y_R, n) 
    X        = np.arange(0,l)
    estYVals = pylab.polyval(Model, X)
    Y        = estYVals-estYVals[0]
    WPs      = Point_Maker(X, Y) 
    WP       = Eq_Distance_maker(WPs,lbp)
    WP_r     = Rotate(WP,theta)
    ################################################
    L        = 0 
    for i in range(len(WP) - 2):
        temp = Distance(WP[i], WP[i+1])
        L    += temp
    ################################################
    X,Y      = list(),list()
    for i in range(len(WP_r)):
        X.append(WP_r[i][0])
        Y.append(WP_r[i][1]) 
    return WP_r,X,Y,L

##################################################
############### Closed Loop Curve ################
##################################################
def cardioid(a):
    osp = a/18
    lbp = 3
    X,Y = [],[]
    wp = []
    for i in range(0,-180,-1):
        x = 2*a*(1-np.cos(np.deg2rad(i)))*np.cos(np.deg2rad(i)) 
        y = 2*a*(1-np.cos(np.deg2rad(i)))*np.sin(np.deg2rad(i)) 
        X.append(round(x,1))
        Y.append(round(y,1))
        wp.append([round(x,1),round(y,1)])
        
    for i in range(180,0,-1):
        x = 2*a*(1-np.cos(np.deg2rad(i)))*np.cos(np.deg2rad(i)) 
        y = 2*a*(1-np.cos(np.deg2rad(i)))*np.sin(np.deg2rad(i)) 
        X.append(round(x,1))
        Y.append(round(y,1))
        wp.append([round(x,1),round(y,1)])
    ################################################
    ref_id = np.random.choice([0,1])
    if ref_id == 0:
        wp_new = wp[::-1]
        X = X[::-1]
        Y = Y[::-1]
    else:
        wp_new = wp
        
    L = 8*a # length of the cardioid formula
    S_wp = Eq_Distance_maker(wp_new,lbp)
    return S_wp,X,Y,L

def Ellipse(a,b):
    wp    = []
    X,Y   = [],[]
    L     = 0 
    lbp = 3
    def f(x,a,b):
        ia = b**2
        ib = (x**2)/(a**2)
        y2 = ia*(1-ib)
        y  = np.sqrt(y2)
        return y
    L = a
    for i in range(-L,L):
        temp = f(i,a,b)
        X.append(i+a)
        Y.append(temp)
        wp.append([i+a,temp])
    for i in range(-L,L):
        temp = f(-i,a,b)
        X.append(-i+a)
        Y.append(-temp)
        wp.append([-i+a,-temp])
    
    X.append(X[0])
    Y.append(Y[0])
    wp.append(wp[0])
    ref_id = np.random.choice([0,1])
    if ref_id == 0:
        wp_new = wp[::-1]
        X = X[::-1]
        Y = Y[::-1]
    else:
        wp_new = wp
        
    #####################
    #####################
    ec1 = 3*(a+b)
    ec2 = np.sqrt(((3*a) + b)*(a + (3*b)))
    L   = np.pi*(ec1 - ec2)
    S_wp = Eq_Distance_maker(wp,lbp)
    return S_wp,X,Y,L
##################################################
############### Sine-Cosine Curve ################
##################################################
def sine_wave():
    lbp     = 3
    WP      = []
    Fs      = 250
    f       = np.random.choice([1,2,3,4])
    sample  = 250
    X       = np.arange(sample)
    Y       = np.sin(2 * np.pi * f * X / Fs)
    Y       = np.random.choice([1,-1])*Y
    ################################################
    Y = Y*np.random.randint(20,40)
    ################################################
    for i in range(len(X)):
        temp = [X[i],Y[i]]
        WP.append(temp)
    S_wp = Eq_Distance_maker(WP,lbp)
    ################################################
    L        = 0 
    for i in range(len(WP) - 2):
        temp = Distance(WP[i], WP[i+1])
        L    += temp
    ################################################
    
    return S_wp,X,Y,L

###################################################
###################################################
def activate():
    Id  = np.random.rand()
    
    if Id < 0.0001:
        pivot = 0
        S_wp,X,Y,L = sine_wave()
    ###########################################################################
    else: #Id > 0.3 and Id <= 0.80:
        pivot = 1
        ref_head = np.random.randint(-180,180)
        S_wp,X,Y,L = straight_line(300,ref_head)
    # elif Id > 0.8 and Id <= 0.9:
    #     ref_shape = np.random.choice([1,2])
    #     if ref_shape == 1:
    #         radius            = np.random.randint(15,45)
    #         S_wp,X,Y,L     = cardioid(radius)
    #     elif ref_shape == 2:
    #         a = np.random.randint(15,45)
    #         b = np.random.randint(5,15)
    #         S_wp,X,Y,L = Ellipse(a,b)
            
    # ###########################################################################    
    # else:
    #     S_wp,X,Y,L     = polycurve(np.random.randint(-2,2),np.random.randint(0,20))
        
    ###########################################################################
    return S_wp,X,Y,L,pivot

########################################################################
########################################################################
WP,X,Y,L = straight_line(150, 45)
plt.figure(figsize=(9,6))
plt.plot(X,Y, color = "crimson")
plt.title("Random Path for Training")
plt.xlabel("Advance (m)")
plt.ylabel("Transfer (m)")
plt.axhline(y=0,color="k") 
plt.axvline(x=0,color="k") 
plt.grid()
plt.show()
print(len(WP),L)
####################
V = []
for i in range(len(WP)):
    temp = WP[i][2]
    V.append(temp)
    
plt.plot(V)
########################################################################
########################################################################















