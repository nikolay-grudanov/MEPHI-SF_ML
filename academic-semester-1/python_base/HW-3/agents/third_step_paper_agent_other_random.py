
##   6   ###############################

import random

def third_step_paper_agent_other_random(observation, configuration):
    """
    Каждый третий шаг возвращает бумагу, в остальных случаях  рандом
    """
    if observation.step % 3 == 0:
      return 1
    return random.randint(0, 2)
