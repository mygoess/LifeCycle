from cmath import log,exp
from distribution import GaussionDistribution,TwoPiont
import income_assert as i_a
import parameters
import numpy as np

'''
可以调整对象
'''
'''
house相关变量说明变量的命名
p_pre：     房子之前的价格 
p_now：     房子现在的价格
h_t:        t时刻租赁的房屋数
h_t_h:      t时刻拥有的房屋数
'''

#   房价限制
#   获取当前的房屋价格
def get_the_house_price(p_pre):
    return p_pre * exp(np.random.normal(parameters.mu_v,parameters.sigma_v))
#   上时期是一个承租者  
#   承租者->承租者预算限制
def renter_to_renter_budget_constraint(p_now,h_t):
    return  - parameters.phi*p_now*h_t 
#   承租者->房屋拥有者预算限制
#   购房贷款的限制

def get_the_mortgage_constraint(p_now,h_now):
    return (1 - parameters.iota) * p_now * h_now 

def renter_to_owner_budget_constraint(p_now,h_t,d_mort):
    return  - ( p_now * h_t - d_mort + parameters.delta_lc * p_now * h_t)

#   计算上一时期有房子的情况
#   下一时期的贷款限制
def get_the_next_morthgage_constraint(p_now,h_pre_h,h_now_h,d_mort_now):
    if  h_now_h!=h_pre_h : return (1-parameters.iota)*p_now*h_now_h
    else: return max((1-parameters.iota)*p_now*h_now_h , parameters.chi*d_mort_now)

def owner_to_rennter_budget_constraint(p_now,h_pre_h ,h_now,d_mort):
    return (1 - parameters.f_h)* p_now * h_pre_h - parameters.phi * p_now * h_now  - d_mort

def owner_to_owner_budget_constraint(p_now,h_now_h,h_pre_h,d_mort_now,d_mort_next,inc,R_short_now):
    L_inc = i_a.get_the_marginal_tax_rate(inc)
    part1 = (parameters.delta_lc * p_now * h_now_h + (1 - L_inc)*(R_short_now - 1 + parameters.delta_uc_r_m) * d_mort_now)
    part2 = 0
    if h_now_h == h_pre_h and d_mort_next > d_mort_now : part2 = parameters.f_d *p_now* h_now_h
    if h_now_h != h_pre_h :   part2 = p_now * (h_now_h - (1 - parameters.f_h * h_pre_h))
    return -part1 - part2 - (d_mort_now - d_mort_next) 

'''
now we can write down a complete statement of the household's working life
'''

#   得到流动性财富 论文中变量Q_t
def get_liquid_wealth_available(a_l_ls,inc,R_ls,d_mort_now):
    tax = i_a.get_tax(inc) 
    L_inc = i_a.get_the_marginal_tax_rate(inc)
    return sum(a_l_ls) + inc - tax - L_inc * sum(1.0 - 1.0/R_ls) - (1 - L_inc) * (R_ls[1] - 1 + parameters.delta_uc_r_m) * d_mort_now

#   获取消费
def get_consume(inc,B_a,B_h):
    return inc - i_a.get_tax(inc) + B_a + B_h

 
#   状态变量: c_t , o_t , h_t, {aL},{aI},d_mort_next 
#   首先这些状态变量是一个收入，但是这个收入优势随时间变化不停输入的输入
#   这些状态变脸组成一个之前的的变量是有一定时间的关系，需要得到之前的变量才能得到之后的变量

