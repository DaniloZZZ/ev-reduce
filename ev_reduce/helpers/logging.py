
import logging
from loguru import logger
FORMAT = '[%(asctime)-5s]%(thread)s %(levelname)s::%(funcName)-8s > %(message)s'

import sys
logger.remove()
logger.add(sys.stdout, format="<d>[{time:HH:mm:ss,SS}]</> \
<e>{thread.name}</>:<lvl>{level}</lvl>\t|\
{function}> {message}"
          )
log = logger
