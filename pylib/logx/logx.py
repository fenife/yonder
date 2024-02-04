#!/usr/bin/env python3

import sys
from loguru import logger

logger.remove()             # Remove default handler (and all others)
logger.add(sys.stdout, backtrace=False, diagnose=False)


