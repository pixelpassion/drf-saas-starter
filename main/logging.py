import logging

logger = logging.getLogger('root')

FORMAT = "%(filename)s:%(lineno)s %(funcName)s() - %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT)

logger.setLevel(logging.DEBUG)
