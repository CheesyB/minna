#!/usr/bin/env python
import os
import logging


class Config(object):

    """Here we get the envs"""

    def __init__(self):
        self.logger = logging.getLogger("minna.config")
        self.config = {}
        self.get_envs()

    def get_envs(self):
        self.config['LOGPATH'] = os.getenv("LOGPATH")
        self.config['LOGNAME'] = os.getenv("LOGNAME")
        self.config['TOKEN'] = os.getenv("TOKEN")
        self.config['CONNECTION'] = os.getenv("CONNECTION")
        self.logger.info(self.config)

