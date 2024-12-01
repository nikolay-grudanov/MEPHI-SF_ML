
##   11   ##############################

import random

def anti_pattern_agent(observation, configuration):
    """
    Этот агент предполагает, что противник повторит свой последний ход, и разыгрывает встречный ход.
    """
    if observation.step > 0:
        return (observation.lastOpponentAction + 1) % 3
    else:
        return random.choice([0, 1, 2])
