
##   10   ##############################

import random

def paper_random_five_agent(observation, configuration):
    """
    Каждый пятый шаг возвращает рандомное значение, в остальных случаях бумагу
    """
    if observation.step % 5 == 0:
        return random.choice([0, 1, 2])
    else:
        return 1
