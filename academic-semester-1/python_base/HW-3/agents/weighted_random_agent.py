
##   5   ###############################

import random

def weighted_random_agent(observation, configuration):
    """ 
    Возвращает камень с вероятностью 20%, бумагу с вероятностью 50%, ножницы с вероятностью 30%
    """
    return random.choices([0, 1, 2], weights=[0.2, 0.5, 0.3])[0]
