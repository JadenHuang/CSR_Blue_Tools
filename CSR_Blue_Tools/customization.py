# -*- coding: utf-8 -*-
from six import with_metaclass
from collections import Counter
from .helpers import AppError, Singleton
from global_settings import g
from CSRAPI import CSRSPIDevice 
import time


class CustomizationError(AppError):
    pass


class Customization(with_metaclass(Singleton, object)):

    def __init__(self):
        self.g = g()
        self.csrlib = CSRSPIDevice()

        # End __init__
        # -------------------------------------------------------------------------

    def init_csr_module(self):
        print ("init_csr_module")


    def ReadSpiPort(self,portnumber):
        print ("read spi port:")
        self.csrLib = CSRSPIDevice()
        self.csrLib.openTestEngineSpi(portnumber)
        self.csrLib.dutport = self.csrLib.spiHandle
        return self.csrLib.dutport

    def writeSerial(self,nap, uap, lap,portnumber):
        
        self.init_csr_module()
        self.csrLib = CSRSPIDevice()
        print ("Opening SPI port for DUT")
        if(self.csrLib.openTestEngineSpi(portnumber)):
            self.csrLib.dutport = self.csrLib.spiHandle

            number_ID =nap+uap+lap
            self.g.serial=number_ID.upper()

            print("input number:{}".format(self.g.serial))

            print "Writing CSR BDADDR... "
            nap = int(self.g.serial[0:4], 16)
            uap = int(self.g.serial[4:6], 16)
            lap = int(self.g.serial[6:12], 16)
            print nap, uap, lap
            self.csrlib.psWriteBdAddr(self.csrLib.dutport, lap, uap, nap)

            #Verification if the input address is correct
            lap, uap, nap = self.csrlib.psReadBdAddr(self.csrLib.dutport)
            if str(uap) =='-1' :
                uap = 0xff
            readBackAddr = ("{:04X}{:02X}{:06X}".format(nap, uap, lap ))
            print ("Read back address : {}".format(readBackAddr ))

            self.csrLib.closeTestEngine(self.csrLib.dutport)
            self.csrLib.dutport = 0
            self.csrlib.spiHandle = 0

            if (readBackAddr == self.g.serial):
                print ("Verification OK")
                # msg = "DUT BDADDR : {}".format(self.g.serial)
                # self.logger.info(msg)
                self.IncrementSerial()
                return True

            else:
                print "Verification Fail"
                #raise CustomizationError("address verification fail")
                # msg = u'(0x21006) Write address error BT-ADDR:[' + self.g.serial + ']'
                # self.logger.info(msg)
                return False

        else:
            self.csrLib.closeTestEngine(self.csrLib.dutport)
            self.csrLib.dutport = 0
            self.csrlib.spiHandle = 0

            print ("Closing SPI port for DUT")    
            return False

            

    def IncrementSerial(self):     
        self.g.serial = "{:012x}".format(int(self.g.serial, 16) + 1)


    def ReadSerial(self,portnumber):

        print("into readserial")
        self.init_csr_module()
        self.csrLib = CSRSPIDevice()
        print ("Opening SPI port for DUT")
        if(self.csrLib.openTestEngineSpi(portnumber)):
            self.csrLib.dutport = self.csrLib.spiHandle

            #Verification if the input address is correct
            lap, uap, nap = self.csrlib.psReadBdAddr(self.csrLib.dutport)
            if str(uap) =='-1' :
                 uap = 0xff
            readBackAddr = ("{:04X}{:02X}{:06X}".format(nap, uap, lap ))
            print ("Read back address : {}".format(readBackAddr ))
           
            self.csrLib.closeTestEngine(self.csrLib.dutport)

            print ("Closing SPI port for DUT")    
            self.csrLib.spiHandle = 0
            

            msg = "DUT BDADDR : {}".format(self.g.serial)
            return (lap,uap,nap)
        else:
            return (0,0,0)