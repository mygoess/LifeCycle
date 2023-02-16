from cmath import log,exp
from distribution import GaussionDistribution,TwoPiont
import parameters
import numpy as np


def get_year(age: int) -> int:
    return age + parameters.born

#   线性插值得到分位数
def is_recession(age: int) -> bool:
    year = get_year(age)
    if year not in parameters.e_dict:
        return False
    return parameters.e_dict[year]

#   获取总分红、长期回报率、短期回报率、固定利率
def get_dividend(year,v_tpre):
    e_t = 0  if is_recession(year) else 1
    e_tpre = 0 if is_recession(year-1) else 1
    var = np.array([1,e_t - e_tpre , e_tpre - e_t , v_tpre])
    return exp(np.dot(var, parameters.theta_v) + np.random.normal(0,parameters.sigma_v_))

def get_R_long(year,v_tpre):
    e_t = 0  if is_recession(year) else 1
    e_tpre = 0 if is_recession(year-1) else 1
    var = np.array([1,e_t - e_tpre , e_tpre - e_t , v_tpre])    
    return exp(np.dot(var, parameters.theta_long_bond) + np.random.normal(0,parameters.sigma_r_long))
    
def get_R_short(year,v_tpre):
    e_t = 0  if is_recession(year) else 1
    e_tpre = 0 if is_recession(year-1) else 1
    var = np.array([1,e_t - e_tpre , e_tpre - e_t , v_tpre])    
    return exp(np.dot(var, parameters.theta_short_bond) + np.random.normal(0,parameters.sigma_r_short))

def get_R_quity(year,v_tpre):
    e_t = 0  if is_recession(year) else 1
    e_tpre = 0 if is_recession(year-1) else 1
    var = np.array([1,e_t - e_tpre , e_tpre - e_t , v_tpre])   
    return exp(np.dot(var, parameters.theta_quity) + np.random.normal(0,parameters.sigma_r_quity))

def get_R_ls(year,v_tpre):
    '''
    year: the number of the years from the T_0 to now
    '''
    r0 = get_R_long(year,v_tpre)
    r1 = get_R_short(year, v_tpre)
    r2 = get_R_quity(year,v_tpre)
    return [r0,r1,r2]
    
#   获取流动性存款和非流动性资产的加和
#   流动性账户和非流动性账户账号利率可以暂时认为是相同
#   对于非流动性账户的会在存款时有加成

def get_assert_Liquid_ls(age,R,a_Liquid,s_L):
    a_L_new = []
    for i in range(3):
        a_L_new.append(R[i]*(a_Liquid[i] + s_L[i]))
    return a_L_new

#   非流动性账户加成
def employer_401K(x,inc,age):  
    if x <= 0 or age >= parameters.T_R: return x
    elif x > 0 and x <= parameters.l * inc: return (1+parameters.k/2) * x
    else: return x + parameters.k/2 * inc
#   非流动性账户计算
#   sum(s_I) < parameters.S_I_max_t
def get_assert_Illiquid_ls(age,R,a_Illiquid,s_I):
    a_I_new = []
    for i in range(3):
        s_I[i] = employer_401K(s_I[i])
        a_I_new.append(R[i]*(a_Illiquid[i] + s_I[i]))
    return a_I_new

def get_the_marginal_tax_rate(inc):
    return 1 - parameters.lambda_*(1 - parameters.kappa)*inc**(-parameters.kappa)

def get_assert_budget_constraint(s_I,s_L,a_L,R,inc,age):
    '''
    L_inc : the marginal tax rate
    the_withdraw : the tax benefits of contributions to (sI ≥ 0) retirement accounts less the tax and possibly early-withdrawal penalty costs associated with withdrawal from (sI < 0) retirement accounts
    '''
    L_inc = get_the_marginal_tax_rate(inc)
    s_I_sum = sum(s_I)
    # 计算补偿金
    if s_I_sum >= 0: the_withdraw = s_I_sum * L_inc
    elif s_I_sum and age < 60: 
        the_withdraw = s_I_sum * (L_inc + 0.1)
    elif s_I_sum and age >= 60:
        the_withdraw = s_I_sum * L_inc
    else: the_withdraw = 0

    return - sum(s_L) - sum(s_I) - L_inc * np.dot((R - 1.0)/R,a_L) + the_withdraw