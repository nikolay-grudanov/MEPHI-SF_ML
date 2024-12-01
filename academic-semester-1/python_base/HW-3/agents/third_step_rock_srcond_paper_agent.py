
##   15   ##############################

import random

def third_step_rock_srcond_paper_agent(observation, configuration):
    """
    Каждый третий шаг возвращает камень, каждый второй бумагу
    """
    if observation.step % 3 == 0:
      return 0
    if observation.step % 2 == 0:
        return 1
    return random.randint(0, 2)
