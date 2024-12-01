
##   13   ##############################

import random

def lose_pattern_agent(observation, configuration):
    """
    Этот агент выбирает проигрышную стратегию, всегда выбирая ход, который проиграет последнему ходу противника.
    """
    if observation.step > 0:
        return (observation.lastOpponentAction + 2) % 3
    else:
        return random.choice([0, 1, 2])
