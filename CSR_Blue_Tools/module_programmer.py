# -*- coding: utf-8 -*-
from __future__ import print_function
from six import with_metaclass
from .config import Config
import ModuleTest_Tool.helpers as helpers
import os.path
import os
from .prog_lib import programmer
from ModuleTest_Tool.CP2110API import *
from ModuleTest_Tool.comminterface import *

class ModuleProgramError(helpers.AppError):
    pass


class ModuleProgram(with_metaclass(helpers.Singleton, object)):
    def __init__(self):

        self.config = Config()
        #self.hid_device = SLABHIDDevice()   #this object is to be associated to DUT with CP2110 hid interface. 
        self.prog = programmer.Programmer()

    # -------------------------------------------------------------------------
    # Module Programming Routine
    # -------------------------------------------------------------------------
    def Module_Flashing(self):
        name = self.config.get_module_name()
        try:
            program = getattr(self, 'program_' + name)
        except AttributeError:
            raise ModuleProgramError("Platform {} not supported yet".format(name))
        program()


    def program_QC30xFxA(self):
        mod_config = self.config.get_module_config()
        relative_dir = mod_config.find(".//program/directory").text
        abs_dir = os.path.join(os.getcwd(), relative_dir)
        method = mod_config.find("./program").attrib["type"].upper()
        action = mod_config.find("./program").attrib["action"].upper()

        firmware = os.path.join(abs_dir, mod_config.find(".//program/firmware").text)

        if not self.config.isSimpleModeEnabled():
            self.prog.init_QC30xFxA()
        self.prog.program_CSR_NVSCMD(firmware, action)

    def program_BC870FxA(self):
        mod_config = self.config.get_module_config()
        relative_dir = mod_config.find(".//program/directory").text
        abs_dir = os.path.join(os.getcwd(), relative_dir)
        method = mod_config.find("./program").attrib["type"].upper()
        action = mod_config.find("./program").attrib["action"].upper()

        firmware = os.path.join(abs_dir, mod_config.find(".//program/firmware").text)

        if not self.config.isSimpleModeEnabled():
            self.prog.init_BC870FxA()
        self.prog.program_CSR_BLUEFLASHCMD(firmware, action)