
import logging
FORMAT = '[%(asctime)-5s]%(thread)s %(levelname)s::%(funcName)-8s > %(message)s'

def init():
    logging.basicConfig(
        level = logging.DEBUG,
        format = FORMAT,
        datefmt='%H:%M:%S'
    )

log = logging
