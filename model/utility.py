import parameters as pm

def get_the_consumption_and_goal(c,h_now,g,g_get):
    '''
    c:      the consume this year
    h_s:    the house size this year
    g:      the money which you give the next goal this year
    g_get:  the goals account you have achieve this year
    '''
    g_u = g + pm.goal_achieve*g_get
    return (pm.alpha1*c**pm.rho + pm.alpha2*h_now**pm.rho + pm.alpha3*g_u**pm.rho)**(1.0/pm.rho)

def get_utility(c,h_now,g,g_get,W_now,year):
    '''
    c:      the consume this year
    h_s:    the house size this year
    g:      the money which you give the next goal this year
    g_get:  the goals account you have achieve this year
    w_now:  the agent's wealth
    '''
    u_out = get_the_consumption_and_goal(c,h_now,g,g_get)
    return u_out**(1 - pm.gamma1) / (1 - pm.gamma1) + pm.philist[year]*pm.kappa* W_now**(1 - pm.gamma2) / (1 - pm.gamma2)

