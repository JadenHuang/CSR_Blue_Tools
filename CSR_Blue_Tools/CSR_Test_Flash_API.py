# -*- coding: utf-8 -*-
from six import with_metaclass
from ctypes import *
import ctypes.wintypes
import os
import time
import re
import struct
#from ModuleTest_Tool.helpers import Singleton, AppError
from helpers import Singleton, AppError
#
# CSR error class
#
class CSRFlashAPIError(AppError):
    pass

#class SLABHIDDevice(with_metaclass(Singleton, object)):
class CSRFlashSPIDevice(with_metaclass(Singleton, object)):

    def __init__(self):
        self.csrLib = self.__getLib()

    def __getLib(self):
        if __name__ == "__main__":
             _environ = dict(os.environ)
             _DIRNAME = os.path.dirname(os.path.abspath(__file__))
             dll_path = os.path.join(_DIRNAME, "dlls", "CSR_BT")
             os.environ['PATH'] += os.pathsep + dll_path
             #print (os.environ['PATH'])
             _dll = ctypes.windll.LoadLibrary("TestFlash.dll")
             print ("load library passed")
             os.environ.clear()
             os.environ.update(_environ)        
        else :
            _environ = dict(os.environ)
            _DIRNAME = os.path.dirname(os.path.abspath(__file__))
            dll_path = os.path.join(_DIRNAME, "dlls", "CSR_BT")
            os.environ['PATH'] += os.pathsep + dll_path
            _dll = ctypes.windll.LoadLibrary("TestFlash.dll")
            print ("TestFlash.dll loaded successfully")
            os.environ.clear()
            os.environ.update(_environ)

        return _dll
#---------------------------------------------------------------------------------
    def flmGetAvailableSpiPorts(self):
        bufSize = struct.pack('<H', 500)
        portsBuf = "\0" * 500  #reserve a buffer size of 100 characters
        transBuf = "\0" * 500
        numPortFound = struct.pack('<H', 0)

        self.flmGetAvailableSpiPortsStatus = self.csrLib.flmGetAvailableSpiPorts(ctypes.c_char_p(bufSize),ctypes.c_char_p(portsBuf),ctypes.c_char_p(transBuf),ctypes.c_char_p(numPortFound))
        if self.flmGetAvailableSpiPortsStatus == 0:

            # print portsBuf
            # print transBuf
            # print struct.unpack('<H', numPortFound)[0]
            # print numPortFound[1]
            return portsBuf,transBuf,struct.unpack('<H', numPortFound)[0]
        else:
            print ("flmGetAvailableSpiPortsStatus error ")
            print self.flmGetAvailableSpiPortsStatus

            return(" "," ",0)

            
    def flmOpen(self,deviceMaskNumber):
        number = 0
        for i in range(deviceMaskNumber):
            add = 0x01 << i
            number = add + number
        deviceMask = ctypes.wintypes.DWORD(number)
        xtal = ctypes.wintypes.DWORD(26)
        transport = ctypes.wintypes.DWORD(2)

        self.flmOpenState = self.csrLib.flmOpen(deviceMask,xtal,transport)
        if self.flmOpenState == 0:
            print ("Test Flash sucessfully opened.")
            return True
        else:
            return False
            print ("Test Flash cannot be opened successfully")

    def flmReadProgramFiles(self,filename):
        fn = ctypes.c_char_p(filename)
        print fn 
        ResdFilesState = self.csrLib.flmReadProgramFiles(fn)
        if ResdFilesState == 0:
            print ("Read file sccessfully.")
            return True
        else:
            return False
            print ("Cannot read file successfully")


    def flmProgramSpawn(self,deviceMaskNumber):
        number = 0
        for i in range(deviceMaskNumber):
            add = 0x01 << i
            number = add + number
        deviceMask = ctypes.wintypes.DWORD(number)
        eraseFirst  = ctypes.wintypes.BYTE(1)
        verifyAfter = ctypes.wintypes.BYTE(1)
        restartAfter = ctypes.wintypes.BYTE(1)
        ProgramSpawnState = self.csrLib.flmProgramSpawn(deviceMask,eraseFirst,verifyAfter,restartAfter)
        if ProgramSpawnState == 0:
            print ("ProgramSpawnState sccessfully.")
            return True
        else:
            return False
            print ("ProgramSpawnState faild.")


    def flmGetDeviceProgress(self,devicenumber):
        device = ctypes.wintypes.DWORD(devicenumber)
        ProgressState = self.csrLib.flmGetDeviceProgress(device)
        return ProgressState

    def flmGetLastError(self):
        ErrorState = self.csrLib.flmGetLastError()
        return ErrorState

    def flmClose(self,deviceMaskNumber):
        number = 0
        for i in range(deviceMaskNumber):
            add = 0x01 << i
            number = add + number
        deviceMask = ctypes.wintypes.DWORD(number)
        CloseState = self.csrLib.flmClose(deviceMask)

    def flmGetBitErrorField(self):
        Error_number = self.csrLib.flmGetBitErrorField()
        return Error_number

    def flmGetDeviceError(self,devicenumber):
        device = ctypes.wintypes.DWORD(devicenumber)
        ErrorState = self.csrLib.flmGetDeviceError(device)
        return ErrorState

    def flmResetAndStart(self,deviceMaskNumber):
        number = 0
        for i in range(deviceMaskNumber):
            add = 0x01 << i
            number = add + number
        deviceMask = ctypes.wintypes.DWORD(number)
        #CloseState = self.csrLib.flmClose(deviceMask)
        deviceMask = ctypes.wintypes.DWORD(3)
        reset = self.csrLib.flmResetAndStart(deviceMask)
        if reset == 0:
            print("reset successfully")

    def flmGetVersion(self):
        versionStr = "\0"*50
        #versionStr = ctypes.c_char_p()
        self.csrLib.flmGetVersion(ctypes.c_char_p(versionStr)) 
        return versionStr
        #print versionStr


    def flmEraseSpawn(self,deviceMaskNumber):
        number = 0
        for i in range(deviceMaskNumber):
            add = 0x01 << i
            number = add + number
        deviceMask = ctypes.wintypes.DWORD(number)
        EraseState = self.csrLib.flmEraseSpawn(number)
        if EraseState == 0:
            print "Erase Spawn Successfully"
        return EraseState

    def flmEraseBlock(self,deviceMaskNumber):
        number = 0
        for i in range(deviceMaskNumber):
            add = 0x01 << i
            number = add + number
        deviceMask = ctypes.wintypes.DWORD(number)
        EraseState = self.csrLib.flmEraseBlock(number)
        if EraseState == 0:
            print "Erase Block Successfully"
        return EraseState

#-----------------------------------------------------------------
    def flInit(self):
        port  = ctypes.wintypes.DWORD(0)
        xtal = ctypes.wintypes.DWORD(26)
        delays = ctypes.wintypes.DWORD(2)
        transport = ctypes.wintypes.DWORD(2)
        flInitState = self.csrLib.flInit(port,xtal,delays,transport)
        if flInitState == 0 :
            print ("FlInit Successfully")



    def flReadProgramFiles(self,filename):
        fn = ctypes.c_char_p(filename)
        ResdFilesState = self.csrLib.flReadProgramFiles(fn)
        if ResdFilesState == 0:
            print ("Read file sccessfully.")
            return True
        else:
            self.flClose()
            print ("Cannot read file successfully")
            return False




    def flProgramSpawn(self):
        flprogramspawnState = self.csrLib.flProgramSpawn()
        if flprogramspawnState == 0:
            print("flProgramSpawn successfully")
        else:
            self.flClose()

    def flGetProgress(self):
        number = self.csrLib.flGetProgress()
        return number

    def flClose(self):
        self.csrLib.flClose()

    def flGetLastError(self):
        ErrorState = self.csrLib.flGetLastError()
        return ErrorState




#-----------------------------------------------------------------------------------



if __name__ == "__main__":
    devicenumber = 2
    csrflashlib = CSRFlashSPIDevice()

    #filename = "c:"+"\""+"Users"+"\""+"Jaden"+"\""+"Desktop"+"\""+"BAT_MOBILE_RC2"+"\""+"LR_Receiver_20170323.xpv"
    filename = r"C:\Users\Jaden\Desktop\test\TestTool\CSR_Blue_Tools\LR_Receiver_20170323.xpv"

    # csrflashlib.flInit()
    # csrflashlib.flReadProgramFiles(filename)
    # csrflashlib.flProgramSpawn()
    # Progress = csrflashlib.flGetProgress()
    # print Progress
    # while Progress < 100:
    #     Progress = csrflashlib.flGetProgress()
    #     print Progress
    #     time.sleep(1)
    # error = csrflashlib.flGetLastError()
    # if error ==0:
    #     print("program successfully")
    # else:
    #     print error




    if(csrflashlib.flmOpen(devicenumber) == True):
        print("flmOpem successfully")
    else:
        print("flmOpem fail")
    if(csrflashlib.flmReadProgramFiles(filename) == True):
        print("flmReadProgramFiles successfully")
    else:
        csrflashlib.flmClose(devicenumber)
        print("flmReadProgramFiles faild")
    if(csrflashlib.flmProgramSpawn(devicenumber) == True):
        print("flmProgramSpawn Successfully")
    else:
        csrflashlib.flmClose(devicenumber)
        print("flmProgramSpawn faild")

    for i in range(devicenumber):
        names = locals()
        names['Progress%s' % i] = csrflashlib.flmGetDeviceProgress(i)
        print ("Progress%d = %s"%(i,names['Progress%s' % i] ))


    while Progress0  < 100 :
        for i in range(devicenumber):
            names = locals()
            names['Progress%s' % i] = csrflashlib.flmGetDeviceProgress(i)
            print ("Progress%d = %s"%(i,names['Progress%s' % i] ))

        time.sleep(1)

    Error = csrflashlib.flmGetLastError()
    print "Read Error Return:"+str(Error)
    if Error ==0 :
        print "Program successfully"

    csrflashlib.flmClose(devicenumber)




