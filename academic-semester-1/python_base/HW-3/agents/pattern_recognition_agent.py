
##   12   ##############################

import random

def pattern_recognition_agent(observation, configuration):
    """
    Этот агент пытается обнаружить закономерность в движениях противника и противодействовать ей.
    """
    if observation.step > 1:
        last_two_moves = (observation.lastOpponentAction, observation.lastOpponentAction)
        if last_two_moves == (0, 0):  # Соперник дважды сыграл камень
            return 1  
        elif last_two_moves == (1, 1):  # Соперник дважды сыграл бумагу
            return 2  
        elif last_two_moves == (2, 2):  # Соперник дважды сыграл ножницы
            return 0  
    return random.choice([0, 1, 2])
