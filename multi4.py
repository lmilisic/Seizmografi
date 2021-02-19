import multiprocessing as mp
manager = None
def init_manager():
    global manager
    manager = mp.Manager()
    return manager
