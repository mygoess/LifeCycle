from cmath import log,exp

from torch import normal, rand
import parameters as pm
import numpy as np
import get_data as d

'''

'''



def get_deterministic_labor_inc(year,Xn):
    the_fy = 1      
    return exp(the_fy) 


def the_probility_unemployed(year,sk_q,sk_p):
    fu = pm.beta_u0 + pm.beta_u1 * year + pm.beta_u2 * sk_q + pm.beta_u3*sk_p
    return 1.0/(1.0-1.0/exp(-fu))


def get_inc(year,Xn)->float:
    '''
        Xn： the state about the income
    '''
    d_labor_inc = get_deterministic_labor_inc(year,Xn)
    # sk :  the shock 
    sk_permanent = np.random.normal(pm.mu_eta_1,pm.sigma_eta_1)\
            if np.random.binomial(1,pm.p_eta) else\
            np.random.normal(pm.mu_eta_2,pm.sigma_eta_2)
    sk_transitory = np.random.normal(0,pm.sigma_q)

    # p: probility
    p_unemployed = the_probility_unemployed(year,sk_transitory,sk_permanent)

    return (1 - np.random.binomial(1,p_unemployed)) * d_labor_inc*exp(sk_transitory + sk_permanent)



