
##   14   ##############################

import random

def random_five_agent(observation, configuration):
    """
    Каждый пятый шаг возвращает рандомное значение, в остальных случаях играет по кругу 
    """
    if observation.step % 5 == 0:
        return random.choice([0, 1, 2])
    else:
        return (observation.step % 3) 
