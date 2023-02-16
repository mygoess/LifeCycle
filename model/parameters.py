from audioop import mul
import numpy as np

'''
the parameters of objective function
'''

alpha1 = 1.0        # the weight coeffcient of consume utility
alpha2 = 10000.0    # the weight coeffcient of house utility
alpha3 = 0.9        # the weight coeffcient of saving for goals utility
goal_achieve = 0.5  # the weight coeffcient of the extra utility for accomplishing a goal
rho = 2.0

delta = 0.96    # discounting factor of the utility 
gamma1 = 5.0      # risk aversion coeffcient of consume and goal

kappa = 0.1     # bequest motive
philist = [1,1,1,1,1,1,1,1,1,1] # the             
gamma2 = 10.0     # risk aversion coeffcient of bequest


'''
the parameters of labor income
'''
mu_eta_1 = 0.12         #  mean1 permanent shock
mu_eta_2 = -0.102       #  mean2 permanent shock
sigma_eta_1 = 0.325     #  std1 ..
sigma_eta_2 = 0.186     #  std2 ..
sigma_q =  0.186         # transitory income shock  


beta_u0 = 1     # coeffcient of the prop
beta_u1 = 1
beta_u2 = 1
beta_u3 = 1

p_eta = 0.5

'''
the parameters of the 
'''



