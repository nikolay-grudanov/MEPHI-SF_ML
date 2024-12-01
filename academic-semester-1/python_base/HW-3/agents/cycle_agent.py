
##   3   ###############################

def cycle_agent(observation, configuration):
    """ 
    Перебирает камень ножницы бумагу по порядку
    """
    return observation.step % 3
