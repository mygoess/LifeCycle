import random
import numpy as np
import matplotlib.pyplot as plt

class GaussionDistribution(object):
    def __init__(self,mean,std):
        self.mean = mean
        self.std = std
    def get_samples(self,sample_nums):
        if sample_nums == 1:
            return np.random.normal(self.mean,self.std,sample_nums)[0]
        else: return np.random.normal(self.mean,self.std,sample_nums)

class TwoPiont(object):
    def __init__(self,p):
        self.p = p
    def get_TP(self):
        return np.random.binomial(1,self.p)

