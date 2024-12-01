
##   7   ###############################

def rock_paper_agent(observation, configuration):
    """
    Каждый шаг возвращает камень, но четный шаг возвращает бумагу
    """
    if observation.step % 2 == 0:
      return 1
    return 0
