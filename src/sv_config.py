#!/usr/bin/env python3

import logging

SV_CONFIG = {
        'native_width' : 32,
        'log_level' : logging.DEBUG,
}

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"

logging.basicConfig(level=SV_CONFIG['log_level'], format=FORMAT)
