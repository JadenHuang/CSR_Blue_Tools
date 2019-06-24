# -*- coding: utf-8 -*-

from six import with_metaclass
from .helpers import Singleton


class g(with_metaclass(Singleton, object)):

#class g:
    def __init__(self):
	    self.debug = 0
	    self.station = '00000'
	    self.serial = '000000000000'
	    self.module = 'MAIN'
	    self.CONFIG_FILE = "config/config.xml"

