import pandas as pd

# income表格中的单位为1000
# p5 10 25 75 80 90 95 99
'''

working life
retirement

房价
不同投资类型的年利率

药物支出的分位表


规范一下env环境
'''

def get_data():
    male_inc = pd.read_csv('/home/Cylone/lifecycle_model_US/data_US/GKSW_male.csv')
    female_inc = pd.read_csv('/home/Cylone/lifecycle_model_US/data_US/GKSW_female.csv')
    return male_inc,female_inc

