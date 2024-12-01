
##   8   ###############################

def rock_scissors_agent(observation, configuration):
    """
    Каждый шаг возвращает камень, но четный шаг возвращает ножницы
    """
    if observation.step % 2 == 0:
      return 2
    return 0
