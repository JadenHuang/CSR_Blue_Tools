# -*- coding: utf-8 -*-
from six import with_metaclass
from ctypes import *
import ctypes.wintypes
import os
import time
import re
#from ModuleTest_Tool.helpers import Singleton, AppError
from helpers import Singleton, AppError

STRING_BUFFER_SIZE = 128

# PSKEY number defines (for QC30xFxA)
PSKEY_HOST_INTERFACE = 0x0119
PSKEY_VM_DISABLE = 0x025d
PSKEY_SELECT_CLOCK_OUTPUT_PIO = 0x2594
PSKEY_SELECT_CLOCK_OUTPUT_RATE = 0x2595
PSKEY_SELECT_CLOCK_OUTPUT_SOURCE = 0x25a3
PSKEY_PIO_PROTECT_MASK = 0x0202
PSKEY_PIO_PROTECT_MASK2 = 0x0592

# PS Store defines
PS_STORES_DEFAULT = 0x0000    #default
PS_STORES_I       = 0x0001    #implementation (normal) 
PS_STORES_F       = 0x0002    #factory-set 
PS_STORES_R       = 0x0004    #ROM (read-only) 
PS_STORES_T       = 0x0008    #transient (RAM) 
PS_STORES_A       = 0x0010    #PSFS 

PS_STORES_FR      = 0x0006
PS_STORES_IF      = 0x0003
PS_STORES_IFR     = 0x0007
PS_STORES_IFAR    = 0x0017

retVal_dict = {-1 : 'Invalid handle', 0:'Error', 1:'Success', 2:'Unsupported function'}

#BT2.1 packet type and payload definitions
packetType_dict = {
                    "DM1" : 3,
                    "DH1" : 4,
                    "HV1" : 5, 
                    "HV2" : 6,
                    "HV3" : 7,
                    "DV"  : 8,
                    "AUX1": 9,
                    "DM3" : 10,
                    "EV4" : 12,
                    "EV5" : 13,
                    "DM5" : 14,
                    "DH5" : 15,
                    "2-DH1" : 20,
                    "2-EV3" : 22,
                    "3-EV3" : 23,  
                    "3-DH1" : 24,  
                    "2-DH3" : 26, 
                    "3-DH3" : 27,  
                    "2-EV5" : 28,  
                    "3-EV5" : 29,  
                    "2-DH5" : 30,  
                    "3-DH5" : 31  }

packetPayload_dict = {
                    "DM1" : 17,  
                    "DH1" : 27,  
                    "HV1" : 10,  
                    "HV2" : 20,  
                    "HV3" : 30,  
                    "DV" : 19,  
                    "AUX1" : 29,  
                    "DM3" : 121,  
                    "DH3" : 183,  
                    "EV4" : 120,  
                    "EV5" : 180,  
                    "DM5" : 224,  
                    "DH5" : 339,  
                    "2-DH1" : 54,  
                    "2-EV3" : 60,  
                    "3-EV3" : 90,  
                    "3-DH1" : 83,  
                    "2-DH3" : 367,  
                    "3-DH3" : 552,  
                    "2-EV5" : 360,  
                    "3-EV5" : 540,  
                    "2-DH5" : 679,  
                    "3-DH5" : 1021 }

#
# CSR error class
#


class CSRAPIError(AppError):
    pass

#class SLABHIDDevice(with_metaclass(Singleton, object)):
class CSRSPIDevice(with_metaclass(Singleton, object)):

    def __init__(self):
        self.csrLib = self.__getLib()
        self.spiHandle = 0
        self.comHandle = 0
        self.refport = 0
        self.dutport = 0

    def __getLib(self):
        if __name__ == "__main__":
             _environ = dict(os.environ)
             _DIRNAME = os.path.dirname(os.path.abspath(__file__))
             dll_path = os.path.join(_DIRNAME, "dlls", "CSR_BT")
             os.environ['PATH'] += os.pathsep + dll_path
             #print (os.environ['PATH'])
             _dll = ctypes.windll.LoadLibrary("TestEngine.dll")
             print ("load library passed")
             os.environ.clear()
             os.environ.update(_environ)        
        else :
            _environ = dict(os.environ)
            _DIRNAME = os.path.dirname(os.path.abspath(__file__))
            dll_path = os.path.join(_DIRNAME, "dlls", "CSR_BT")
            os.environ['PATH'] += os.pathsep + dll_path
            _dll = ctypes.windll.LoadLibrary("TestEngine.dll")
            print ("TestEngine.dll loaded successfully")
            os.environ.clear()
            os.environ.update(_environ)

        return _dll

    #def _convert_str(self, buffer, length):
    #    return ''.join(map(chr, buffer[:length]))

    def openTestEngineSpi(self,portnumber):
        port = ctypes.wintypes.DWORD(portnumber)
        multi = ctypes.wintypes.DWORD(0)
        transport = ctypes.wintypes.DWORD(2)
        transStr = "SPITRANS=USB"

        if self.spiHandle != 0 :
            print ("Found test engine already opened, try to close it first")
            self.closeTestEngine(self.spiHandle)
            self.spiHandle == 0

        print ("Opening test engine...")
        self.spiHandle = self.csrLib.openTestEngineSpi(port, multi, transport)
        #handle = self.csrLib.openTestEngineSpiTrans(transStr, multi)
        
        if self.spiHandle == 0:  #try one more time
            # print ("Try one more time...")
            # self.spiHandle = self.csrLib.openTestEngineSpi(port, multi, transport)
            # if self.spiHandle == 0:
                #raise CSRAPIError("openTestEngineSpi call failed")
            return False
        else:
            print ("Test engine spi sucessfully opened.")
            return True
    
    def openTestEngineCOM(self, comportStr):
        transport_INT32 = ctypes.wintypes.DWORD(1) #BCSP transport
        transportDevice_STR = "\\\\.\\"+comportStr
        
        dataRate_UNIT32 = ctypes.wintypes.DWORD(115200) # baud rate
        retryTimeOut_UNIT32 = ctypes.wintypes.DWORD(2000) #1000 ms
        usbTimeOut_INT32 = ctypes.wintypes.DWORD(2000) #1000ms

        print ("Opening test engine at {}".format(comportStr))
        self.comHandle = self.csrLib.openTestEngine(transport_INT32, transportDevice_STR, dataRate_UNIT32, retryTimeOut_UNIT32, usbTimeOut_INT32)
        if self.comHandle == 0:  #try one more time
            print ("Try one more time...")
            self.comHandle = self.csrLib.openTestEngine(transport_INT32, transportDevice_STR, dataRate_UNIT32, retryTimeOut_UNIT32, usbTimeOut_INT32)
            if self.comHandle == 0:
                raise CSRAPIError("openTestEngineCOM call failed")
        else:
            print ("Test engine at {} sucessfully opened.".format(comportStr))
  
    def closeTestEngine(self, deviceHandle):
        if deviceHandle != 0:
            value = self.csrLib.closeTestEngine(deviceHandle)
            if value != 1:
                raise CSRAPIError("closeTestEngine call failed, return value {}".format(retVal_dict[value]))

#
# This version of merge_CSR_pscli will parses the PSR file and write the PSKEYs one by one
# Only works for DUT.
#
    def merge_CSR_pscli(self, deviceHandle, psrFile):
        print ("Merging {}".format(psrFile))
        try :
            file = open(psrFile, "r")
            pskeyAddr = 0
            for line in file:
                #print line
                InvalidData = 0
                dataBuf = []
                if not (bool(re.match('^ *//',line)) | bool(re.match('^ *$',line))): #comment line or blank line
                    m = re.match("^ *&([0-9A-Fa-f]{4}) *= *(.*$)", line)
                    if m:
                        pskeyAddr = int(m.groups(0)[0],16)
                        #print ("0x{:x}".format(pskeyAddr))
                        
                        dataTubleList=m.groups(0)[1].split()
                        #check each tuble
                        for tuple in dataTubleList:
                           if not (re.match('[0-9A-Fa-f]{4}', tuple)):
                              print ("invalid data {}".format(tuple))
                              raise ProgrammerError("Mering psr file failed")
                           else:
                              #print "Tuple {} is valid".format(tuple)
                              dataBuf.append(int(tuple,16))
                        
                        #writing PSKEYs
                        self.psWrite(deviceHandle, pskeyAddr, PS_STORES_DEFAULT, len(dataBuf), dataBuf)
            #time.sleep(1)     
            self.bccmdSetWarmReset(self.dutport)    
                
        finally:
            print ("End of merging")

#
# This version of merge_CSR_pscli is to use test enginer command "psMergeFromFile" to merge PSR
#
    def ymerge_CSR_pscli(self, psrFile, deviceHandle):
        print ("Merging {}".format(psrFile))
      
        self.csrLib.psMergeFromFile(deviceHandle, psrFile)
        #raw_input("Press any key to warm reset")
        self.bccmdSetWarmReset(deviceHandle)
       
        print ("End of merging")

    def psSize(self, deviceHandle, pskeyID, storeMask):
        pskeyID_UINT16 = ctypes.wintypes.WORD(pskeyID)
        storeMask_UINT16 = ctypes.wintypes.WORD(storeMask)
        result_UINT16 = ctypes.wintypes.WORD()
        
        retVal = self.csrLib.psSize (deviceHandle, pskeyID_UINT16, storeMask_UINT16, ctypes.byref(result_UINT16))
        if retVal != 1:
            raise CSRAPIError("psSize call failed : {}".format(retVal_dict[retVal]))
        return result_UINT16.value


    def psRead(self, deviceHandle, pskeyID, storeMask, arrayLen, dataArray):
        
        pskeyID_UINT16 = ctypes.wintypes.WORD(pskeyID)
        storeMask_UINT16 = ctypes.wintypes.WORD(storeMask)
        arrayLen_UINT16 = ctypes.wintypes.WORD(arrayLen)   
       
        dataArray_UINT16 = (ctypes.wintypes.WORD * arrayLen)()
        pskeySize = self.psSize(pskeyID, storeMask)
        #print ("pskeysize is {}".format(pskeySize))
        len_UINT16 = ctypes.wintypes.WORD(pskeySize)
        #print ("psSize of {} is {}".format(pskeyID, len_UINT16.value))
        retVal = self.csrLib.psRead(deviceHandle, pskeyID_UINT16, storeMask_UINT16, arrayLen_UINT16, dataArray_UINT16, ctypes.byref(len_UINT16))
        #print (dataArray_UINT16)
        if retVal != 1:
            raise CSRAPIError("psRead call failed : {}".format(retVal_dict[retVal]))

        for item in range(0,arrayLen):
            dataArray.append(dataArray_UINT16[item])
        return  #nothing to return


    def psWrite(self, deviceHandle, pskeyID, storeMask, arrayLen, dataArray):
    
        pskeyID_UINT16 = ctypes.wintypes.WORD(pskeyID)
        storeMask_UINT16 = ctypes.wintypes.WORD(storeMask)
        arrayLen_UINT16 = ctypes.wintypes.WORD(arrayLen)   
       
        dataArray_UINT16 = (ctypes.wintypes.WORD * arrayLen)()
        #print dataArray
        for item in range (0, arrayLen):
            dataArray_UINT16[item] = ctypes.wintypes.WORD(dataArray[item])

        #print dataArray_UINT16

        retVal = self.csrLib.psWrite(deviceHandle, pskeyID_UINT16, storeMask_UINT16, arrayLen_UINT16, dataArray_UINT16)
        
        if retVal != 1:
            raise CSRAPIError("psWrite call failed : {}".format(retVal_dict[retVal]))
        print ("psWrite successful : pskeyID = {}, storeMask = {}, data = {}".format(pskeyID, storeMask, dataArray))
        return  #nothing to return


    def psReadBdAddr(self, deviceHandle):

        lap_UINT32 = ctypes.wintypes.DWORD(0)
        uap_UINT8 = ctypes.wintypes.BYTE(0)
        nap_UINT16 = ctypes.wintypes.WORD(0)

        retVal = self.csrLib.psReadBdAddr(deviceHandle, ctypes.byref(lap_UINT32), ctypes.byref(uap_UINT8), ctypes.byref(nap_UINT16))

        if retVal != 1:
            raise CSRAPIError("psReadBdAddr call failed : {}".format(retVal_dict[retVal]))

        return  lap_UINT32.value, uap_UINT8.value, nap_UINT16.value


    def psWriteBdAddr(self, deviceHandle, lap, uap, nap):

        # BD_ADDR : aa:bb:cc:dd:ee:ff
        # where aa:bb is nap, cc is uap, dd:ee:ff is lap
        lap_UINT32 = ctypes.wintypes.DWORD(lap)
        uap_UINT32 = ctypes.wintypes.DWORD(uap)
        nap_UINT32 = ctypes.wintypes.DWORD(nap)

        retVal = self.csrLib.psWriteBdAddr(deviceHandle, lap_UINT32, uap_UINT32, nap_UINT32)
        if retVal != 1:
            raise CSRAPIError("psWriteBdAddr call failed : {}".format(retVal_dict[retVal]))

        return #Nothing to return

    def bccmdSetWarmReset(self, deviceHandle):

        usbTimeOut_INT32 = ctypes.wintypes.DWORD(2)  #set 2 seconds for timeout
        retVal = self.csrLib.bccmdSetWarmReset(deviceHandle, usbTimeOut_INT32)
        if retVal != 1:
            raise CSRAPIError("bccmdSetWarmReset call failed : {}".format(retVal_dict[retVal]))

        return #Nothing to return

    def bccmdSetColdReset(self, deviceHandle):

        usbTimeOut_INT32 = ctypes.wintypes.DWORD(0)  #set 0 seconds for timeout
        retVal = self.csrLib.bccmdSetColdReset(deviceHandle, usbTimeOut_INT32)
        if retVal != 1:
            raise CSRAPIError("bccmdSetColdReset call failed : {}".format(retVal_dict[retVal]))

        return #Nothing to return

    def psMergeFromFile(self, deviceHandle, psrFilePathStr):

        retVal = self.csrLib.psMergeFromFile(deviceHandle, psrFilePathStr)
        if retVal != 1:
            raise CSRAPIError("psMergeFromFile call failed : {}".format(retVal_dict[retVal]))

    def radiotestTxstart(self, deviceHandle, frequency, intPA, extPA, modulation):
    #deviceHandle coult be self.spiHandle (SPI) or self.comHandle (COM)
        freq_UINT16 = ctypes.wintypes.WORD(frequency)
        intPA_UINT16 = ctypes.wintypes.WORD(intPA)
        extPA_UINT16 = ctypes.wintypes.WORD(extPA)
        mod_UINT16 = ctypes.wintypes.WORD(modulation)

        retVal = self.csrLib.radiotestTxstart(deviceHandle,freq_UINT16, intPA_UINT16, extPA_UINT16, mod_UINT16 )
        if retVal != 1:
            raise CSRAPIError("radiotestTxstart call failed : {}".format(retVal_dict[retVal]))

    def radiotestPause(self, deviceHandle):
        retVal = self.csrLib.radiotestPause(deviceHandle)
        if retVal != 1:
            raise CSRAPIError("radiotestPause call failed : {}".format(retVal_dict[retVal]))

    def radiotestRxstart2(self, deviceHandle, frequency, sampleSize):
        freq_UINT16 = ctypes.wintypes.WORD(frequency)
        hiside_UINT8 = ctypes.wintypes.BYTE(0)  #low side modulation
        rx_attenuation_UINT16 = ctypes.wintypes.WORD(0) 
        sampleSize_UNIT16 = ctypes.wintypes.WORD(sampleSize) #take 20 samples

        retVal = self.csrLib.radiotestRxstart2(deviceHandle, freq_UINT16, hiside_UINT8, rx_attenuation_UINT16, sampleSize_UNIT16)
        if retVal != 1:
            raise CSRAPIError("radiotestRxstart2 call failed : {}".format(retVal_dict[retVal]))
        else:
            print ("radiotestRxstart2 call successful")

    def hqGetRssi (self, deviceHandle, maxSize):
        #time in ms. This is a mysterious parameter. Value smaller than this will cause 
        #fucntion call error
        timeout_UINT32 = ctypes.wintypes.DWORD(5000)  
        maxSize_UINT16 = ctypes.wintypes.WORD(maxSize)
        dataArray_UINT16 = (ctypes.wintypes.WORD * maxSize)(0)

        retVal = self.csrLib.hqGetRssi(deviceHandle, timeout_UINT32, maxSize_UINT16, dataArray_UINT16)
        if retVal != 1:
            raise CSRAPIError("hqGetRssi call failed : {}".format(retVal_dict[retVal]))
        else:  #calculate average rssi result 
            #for index in range (0,maxSize):
            #    print dataArray_UINT16[index]
            rssi = float(sum(dataArray_UINT16)) / maxSize
            return rssi


    def radiotestTxdata(self, deviceHandle, hop_en, frequency, intPA, extPA): #use this if hopping is disabled
        frequency_UINT32 = ctypes.wintypes.DWORD(frequency)
        intPA_UINT16 = ctypes.wintypes.WORD(intPA)
        extPA_UINT16 = ctypes.wintypes.WORD(extPA)
        countryCode_UINT16 = ctypes.wintypes.WORD(0)

        if hop_en == 0:
            print ("radiotestTxdata1 with hopping disabled")
            retVal = self.csrLib.radiotestTxdata1(deviceHandle, frequency_UINT32, intPA_UINT16, extPA_UINT16)
            if retVal != 1:
                raise CSRAPIError("radiotestTxdata1 call failed : {}".format(retVal_dict[retVal]))
        else:
            print ("radiotestTxdata2 with hopping enabled")
            retVal = self.csrLib.radiotestTxdata2(deviceHandle, countryCode_UINT16, intPA_UINT16, extPA_UINT16)
            if retVal != 1:
                raise CSRAPIError("radiotestTxdata2 call failed : {}".format(retVal_dict[retVal]))

    def radiotestBer(self, deviceHandle, hop_en, frequency, rx_attenuation, sampleSize):
        freq_UINT16 = ctypes.wintypes.WORD(frequency)
        hiside_UINT8 = ctypes.wintypes.BYTE(0)
        rx_attenuation_UINT16 = ctypes.wintypes.WORD(rx_attenuation)
        sampleSize_UINT32 = ctypes.wintypes.DWORD(sampleSize)
        countryCode_UINT16 = ctypes.wintypes.WORD(0)

        if hop_en == 0:
            print ("radiotestBer1 with hopping disabled")
            retVal = self.csrLib.radiotestBer1(deviceHandle, freq_UINT16, hiside_UINT8, rx_attenuation_UINT16, sampleSize_UINT32)
            if retVal != 1:
                raise CSRAPIError("radiotestBer1 call failed : {}".format(retVal_dict[retVal]))
        else:
            print ("radiotestBer2 with hopping enabled")
            retVal = self.csrLib.radiotestBer2(deviceHandle, countryCode_UINT16, hiside_UINT8, rx_attenuation_UINT16, sampleSize_UINT32)
            if retVal != 1:
                raise CSRAPIError("radiotestBer2 call failed : {}".format(retVal_dict[retVal]))
        

    def radiotestCfgPkt(self, deviceHandle, type):
        if type not in packetType_dict:
            print ("Packet type : {} undefined".format(type))
            raise CSRAPIError("radiotestCfgPkt call failed : packet type {} undefined".format(type))

        type_UINT16 = ctypes.wintypes.WORD(packetType_dict[type])
        payload_UINT16 = ctypes.wintypes.WORD(packetPayload_dict[type])

        retVal = self.csrLib.radiotestCfgPkt(deviceHandle, type_UINT16, payload_UINT16)
        if retVal != 1:
            raise CSRAPIError("radiotestCfgPkt call failed : {}".format(retVal_dict[retVal]))

    def radiotestCfgFreq(self, deviceHandle, txrxInterval, loopback, report):
        txrxInterval_UINT16 = ctypes.wintypes.WORD(txrxInterval)
        loopback_UINT16 = ctypes.wintypes.WORD(loopback)
        report_UINT16 = ctypes.wintypes.WORD(report)

        retVal = self.csrLib.radiotestCfgFreq(deviceHandle, txrxInterval_UINT16, loopback_UINT16, report_UINT16)
        if retVal != 1:
            raise CSRAPIError("radiotestCfgFreq call failed : {}".format(retVal_dict[retVal]))

    def hqGetBer(self, deviceHandle, dataBuf):
        timeout_INT32 = ctypes.wintypes.DWORD(2000)
        dataBuf_UINT32 = (ctypes.wintypes.DWORD * 9)(0)

        for count in range (0, 9):
            retVal = self.csrLib.hqGetBer(deviceHandle, timeout_INT32, dataBuf_UINT32)
            if retVal != 1:
                raise CSRAPIError("hqGetBer call failed : {}".format(retVal_dict[retVal]))
        for i in range(0,9):
            dataBuf[i] = dataBuf_UINT32[i]

    def radiotestBerLoopback(self, deviceHandle, frequency, intPA, extPA, sampleSize):
        freq_UINT16 = ctypes.wintypes.WORD(frequency)
        intPA_UINT16 = ctypes.wintypes.WORD(intPA)
        extPA_UINT16 = ctypes.wintypes.WORD(extPA)
        sampleSize_UINT32 = ctypes.wintypes.DWORD(sampleSize)

        retVal = self.csrLib.radiotestBerLoopback(deviceHandle, freq_UINT16, intPA_UINT16, extPA_UINT16,sampleSize_UINT32 )
        if retVal != 1:
            raise CSRAPIError("radiotestBerLoopback call failed : {}".format(retVal_dict[retVal]))
        pass

    def radiotestLoopback(self, deviceHandle, frequency, intPA, extPA):
        freq_UINT16 = ctypes.wintypes.WORD(frequency)
        intPA_UINT16 = ctypes.wintypes.WORD(intPA)
        extPA_UINT16 = ctypes.wintypes.WORD(extPA)

        retVal = self.csrLib.radiotestLoopback(deviceHandle, freq_UINT16, intPA_UINT16, extPA_UINT16 )
        if retVal != 1:
            raise CSRAPIError("radiotestLoopback call failed : {}".format(retVal_dict[retVal]))


if __name__ == "__main__":
    csrapi = CSRSPIDevice()
    csrapi.openTestEngineSpi()

    dataArray = []
    csrapi.psRead(0x0001, PS_STORES_R, 4, dataArray)
    print ("psSize of 0x0001 is {}".format(csrapi.psSize(0x0001,PS_STORES_IFR)))
    print dataArray
    dataArray[3] = 1
    csrapi.psWrite(0x0001, PS_STORES_T, 4, dataArray)
    dataArray = []
    csrapi.psRead (0x0001, PS_STORES_T, 4, dataArray)
    print dataArray
    
    # Test psReadBdAddr
    lap, uap, nap = csrapi.psReadBdAddr()
    print ("lap = {}, uap = {}, nap = {}".format(lap, uap, nap))

    # Test bccmdSetWarmReset
    csrapi.bccmdSetWarmReset()
    print "bccmdSetWarmReset successful"
    dataArray = []
    csrapi.psRead (0x0001, PS_STORES_T, 4, dataArray)
    print dataArray

    csrapi.closeTestEngine()
