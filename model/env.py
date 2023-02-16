import parameters 
import income as i_a
import consume_house as c_h
import life_data  as l_d
import utility as u
import torch
import torch.nn as nn



class lifecycle_cn(object):

    def __init__(self,q0,sex,h_price,h_now,o_now,d_now = 0, a_I = [0,0,0],a_L= [0,0,0]):
        super(self).__init__()
        self.q0 = q0
        self.male_inc,self.female_inc = l_d.get_data()
        self.inc_ls = i_a.get_inc_list(self.male_inc,self.female_inc,sex,q0)
        
        self.pension_base = i_a.get_total_labor_q_R(sum(self.inc_ls))
        self.age = parameters.T_0

        # 各种类型资产的利率
        self.v_pre = parameters.v_0
        self.r_ls = parameters.r_ls0
        # 各种账户的资产
        self.a_I_ls = a_I
        self.a_L_ls = a_L


        # 住房相关
        self.d_now = d_now
        self.o_pre = o_now
        self.h_pre = h_now
        self.h_price = h_price
        


    #   获取收入
    #       获取房屋拥有数量
    #       获取贷款数量
    #       约束公式如何表达
    #       资产的增值
    
    def work_step(self,d_next, o_now, h_now, s_I_ls,s_L_ls):
        '''
        s_I_ls   
        s_L_ls 
        '''
        self.age = self.age + 1          

        self.inc = self.inc_ls[self.age - parameters.T_0]  
        self.h_price = c_h.get_the_house_price(self.h_price)

        if self.o_pre == 0 and o_now == 0:
            B_h = c_h.renter_to_renter_budget_constraint(self.h_price,h_now)
        elif self.o_pre == 0 and o_now == 1:
            B_h = c_h.renter_to_owner_budget_constraint(self.h_price,h_now,d_next) 
        elif self.o_pre == 1 and o_now == 1:
            B_h = c_h.owner_to_owner_budget_constraint(self.h_price,h_now,self.h_pre,self.d_now,d_next,self.inc)
        else: B_h = c_h.renter_to_renter_budget_constraint(self.h_price,h_now)
        self.a_I_ls = i_a.get_assert_Illiquid_ls(self.age,self.r_ls,self.a_I_ls,s_I_ls)
        self.a_L_ls = i_a.get_assert_Liquid_ls(self.age,self.r_ls,self.a_L_ls,s_L_ls)        
        B_a = i_a.get_assert_budget_constraint(s_I_ls,s_L_ls,self.a_L_ls,self.r_ls,self.inc,self.age)
        c_now = c_h.get_consume(self.inc,B_a,B_h)

        return u.get_utility_consume(c_now,h_now)
    

    def retire_step(self,age,d_next, o_now,h_now, a_L_ls,a_I_ls, c_now):
        self.age = self.age + 1
        self.inc = i_a.get_pension()
        return u.get_utility_consume(c_now,h_now)


    def reset(q0):
        pass
        

