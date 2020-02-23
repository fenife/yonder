#!/usr/bin/env python3

import logging
from .log import create_logger

create_logger(__name__)

# logging.getLogger(__name__).addHandler(logging.NullHandler())
# _logger = logging.getLogger(__name__)
# _logger.addHandler(logging.StreamHandler())
# _logger.setLevel(logging.DEBUG)
