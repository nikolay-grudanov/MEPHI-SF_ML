
##   9   ###############################

import random
def cycle_agent_v2(observation, configuration):
    """
    Перебирает ножницы камень бумагу по порядку (2-0-1-2-0-1...)
    """
    # если это первый ход
    if observation.step > 0:
        # возвращаем рандомное значение из доступных вариантов
        return (observation.last_step + 2) % configuration.signs
    # прибавляем 2 к своему последнему ходу
    return random.choice([0, 1, 2]) 
