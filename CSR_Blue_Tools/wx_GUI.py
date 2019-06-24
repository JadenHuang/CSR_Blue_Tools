# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import os
import time
import datetime
import subprocess
from customization import *
from global_settings import g
from CSR_Test_Flash_API import*
import re
import thread 
from wx.lib.masked import numctrl
wx.ID_Choice = 1000
wx.ID_but1 = 1001
wx.ID_but2 = 1002
wx.ID_but3 = 1003
wx.ID_but4 = 1004
wx.ID_edit = 1005




###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"GT_QCFlash", pos = wx.DefaultPosition, size = wx.Size( 685,573 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
	
	  	self.g = g()
	  	self.working = 0  #Show current idle status
		self.devicenumber = 1
		self.portnumber = 0
		self.DeviceErrorsNumber = 0 
		self.command = None
		self.firmware = None
		self.ThreadStart = False
		self.cst=Customization() 
		#self.NumCtrl_Colour =NumCtrl(self)
		self.flag =0
		self.csrflashlib = CSRFlashSPIDevice()
		self.Version = self.csrflashlib.flmGetVersion()
		(self.portsBuf,self.transBuf,self.numPortFound) = self.csrflashlib.flmGetAvailableSpiPorts()
		
		self.csrflashlib.flmGetAvailableSpiPorts()
		self.devicenumber = int(self.numPortFound)
		self.DeviceList = self.portsBuf.split(",")
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		gbSizer2 = wx.GridBagSizer( 0, 0 )
		gbSizer2.SetFlexibleDirection( wx.BOTH )
		gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		m_choice1Choices = self.DeviceList
		self.m_choice1 = wx.Choice( self, wx.ID_Choice, wx.DefaultPosition, wx.Size( 130,-1 ), m_choice1Choices, 0 )
		self.m_choice1.SetSelection( 0 )
		gbSizer2.Add( self.m_choice1, wx.GBPosition( 0, 5 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"Device", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText21.Wrap( -1 )
		self.m_staticText21.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText21, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_button1 = wx.Button( self, wx.ID_but1, u"Choose File", wx.DefaultPosition, wx.Size( 95,-1 ),  0 )
		gbSizer2.Add( self.m_button1, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 425,-1 ), 0 )
		gbSizer2.Add( self.m_textCtrl1, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 4 ), wx.ALIGN_BOTTOM|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )
		
		self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer2.Add( self.m_textCtrl2, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer2.Add( self.m_textCtrl3, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl4 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer2.Add( self.m_textCtrl4, wx.GBPosition( 2, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText23 = wx.StaticText( self, wx.ID_ANY, u"xxxx(nap)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		self.m_staticText23.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText23, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText24 = wx.StaticText( self, wx.ID_ANY, u"xx(uap)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )
		self.m_staticText24.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText24, wx.GBPosition( 3, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"xxxxxx(lap)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )
		self.m_staticText25.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText25, wx.GBPosition( 3, 4 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_button6 = wx.Button( self, wx.ID_ANY, u"ReadAddress", wx.DefaultPosition, wx.Size( 95,-1 ), 0 )
		gbSizer2.Add( self.m_button6, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button2 = wx.Button( self, wx.ID_but2, u"About", wx.DefaultPosition, wx.Size( 95,-1 ),  0 )
		gbSizer2.Add( self.m_button2, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_button7 = wx.Button( self, wx.ID_ANY, u"Start Addr", wx.DefaultPosition, wx.Size( 95,-1 ), 0 )
		gbSizer2.Add( self.m_button7, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button3 = wx.Button( self, wx.ID_but3, u"Flash Erase", wx.DefaultPosition, wx.Size( 95,-1 ),  0 )
		gbSizer2.Add( self.m_button3, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_button4 = wx.Button( self, wx.ID_but4, u"Download", wx.DefaultPosition, wx.Size( 95,60 ),  0 )
		gbSizer2.Add( self.m_button4, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_gauge1 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 420,20 ), wx.GA_HORIZONTAL )
		self.m_gauge1.SetValue( 0 ) 
		self.m_gauge1.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		self.m_gauge1.SetBackgroundColour( wx.Colour( 0, 255, 0 ) )
		
		gbSizer2.Add( self.m_gauge1, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 4 ), wx.ALL, 5 )
		
		self.m_gauge2 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 420,20 ), wx.GA_HORIZONTAL )
		self.m_gauge2.SetValue( 0 ) 
		gbSizer2.Add( self.m_gauge2, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 4 ), wx.ALL, 5 )
		
		self.m_gauge3 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 420,20 ), wx.GA_HORIZONTAL )
		self.m_gauge3.SetValue( 0 ) 
		gbSizer2.Add( self.m_gauge3, wx.GBPosition( 9, 1 ), wx.GBSpan( 1, 4 ), wx.ALL, 5 )
		
		self.m_gauge4 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 420,20 ), wx.GA_HORIZONTAL )
		self.m_gauge4.SetValue( 0 ) 
		gbSizer2.Add( self.m_gauge4, wx.GBPosition( 10, 1 ), wx.GBSpan( 1, 4 ), wx.ALL, 5 )
		
		m_choice4Choices = [ u"BC867x", u"QCC300x" ]
		self.m_choice4 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 95,-1 ), m_choice4Choices, 0 )
		self.m_choice4.SetSelection( 0 )
		gbSizer2.Add( self.m_choice4, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_gauge5 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 420,20 ), wx.GA_HORIZONTAL )
		self.m_gauge5.SetValue( 0 ) 
		gbSizer2.Add( self.m_gauge5, wx.GBPosition( 11, 1 ), wx.GBSpan( 1, 4 ), wx.ALL, 5 )
		
		self.m_gauge6 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 420,20 ), wx.GA_HORIZONTAL )
		self.m_gauge6.SetValue( 0 ) 
		gbSizer2.Add( self.m_gauge6, wx.GBPosition( 12, 1 ), wx.GBSpan( 1, 4 ), wx.ALL, 5 )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_edit, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		self.m_staticText1.Wrap( -1 )
		self.m_staticText1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		self.m_staticText1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		gbSizer2.Add( self.m_staticText1, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 5 ), wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText211 = wx.StaticText( self, wx.ID_ANY, u"ReadPort", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText211.Wrap( -1 )
		self.m_staticText211.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText211, wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"unknow", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		self.m_staticText3.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText3, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"unknow", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		self.m_staticText4.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText4, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"unknow", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText5, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"unknow", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText6, wx.GBPosition( 10, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"unknow", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText7, wx.GBPosition( 11, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"unknow", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		self.m_staticText8.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText8, wx.GBPosition( 12, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"unknow", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		self.m_staticText9.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText9, wx.GBPosition( 13, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"unknow", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		self.m_staticText10.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText10, wx.GBPosition( 14, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Current Addr", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		self.m_staticText11.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText11, wx.GBPosition( 2, 5 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"BT Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		self.m_staticText13.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText13, wx.GBPosition( 7, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"BT Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		self.m_staticText14.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText14, wx.GBPosition( 8, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, u"BT Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		self.m_staticText15.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText15, wx.GBPosition( 9, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"BT Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		self.m_staticText16.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText16, wx.GBPosition( 10, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, u"BT Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		self.m_staticText17.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText17, wx.GBPosition( 11, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"BT Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		self.m_staticText18.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText18, wx.GBPosition( 12, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"BT Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		self.m_staticText19.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText19, wx.GBPosition( 13, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"BT Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		self.m_staticText20.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		gbSizer2.Add( self.m_staticText20, wx.GBPosition( 14, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_gauge7 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 420,20 ), wx.GA_HORIZONTAL )
		self.m_gauge7.SetValue( 0 ) 
		gbSizer2.Add( self.m_gauge7, wx.GBPosition( 13, 1 ), wx.GBSpan( 1, 4 ), wx.ALL, 5 )
		
		self.m_gauge8 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 420,20 ), wx.GA_HORIZONTAL )
		self.m_gauge8.SetValue( 0 ) 
		gbSizer2.Add( self.m_gauge8, wx.GBPosition( 14, 1 ), wx.GBSpan( 1, 4 ), wx.ALL, 5 )

		self.m_button71 = wx.Button( self, wx.ID_ANY, u"DetectDrive", wx.DefaultPosition, wx.Size( 95,60 ), 0 )
		gbSizer2.Add( self.m_button71, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
				
		
		self.SetSizer( gbSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		# Connect Events
		self.m_choice1.Bind( wx.EVT_CHOICE, self.BoxChoice )
		self.m_button1.Bind( wx.EVT_BUTTON, self.ChooseClick )
		self.m_button6.Bind( wx.EVT_BUTTON, self.ReadChick )
		self.m_button2.Bind( wx.EVT_BUTTON, self.OnCloseMe )
		self.m_button7.Bind( wx.EVT_BUTTON, self.WriteChick )
		self.m_button3.Bind( wx.EVT_BUTTON, self.EraseClick )
		self.m_button4.Bind( wx.EVT_BUTTON, self.DownLoadChick )
		self.m_button71.Bind( wx.EVT_BUTTON, self.DetectDrive )
		self.m_choice4.Bind( wx.EVT_CHOICE, self.DeviceChoice )


		self.Show(True)  


	#Restore the original interface
	def RecoveryInterface(self):
		if  self.working == 0:
			(self.portsBuf,self.transBuf,self.numPortFound) = self.csrflashlib.flmGetAvailableSpiPorts()
			self.devicenumber = int(self.numPortFound)
			for i in range(8):
				getattr(self, 'm_staticText' +str(i+13)).SetLabel("BT Address") 
				getattr(self, 'm_staticText' +str(i+3)).SetForegroundColour( wx.Colour( 0, 0, 0 ) )
				#getattr(self, 'm_staticText' +str(i+3)).SetLabel("Device %d"%(i+1))   
				if i < self.numPortFound:
					getattr(self, 'm_staticText' +str(i+3)).SetLabel(self.DeviceList[i]) 
				else:
					getattr(self, 'm_staticText' +str(i+3)).SetLabel("unknow") 
				getattr(self, 'm_gauge' +str(i+1)).SetValue(0)         
				self.m_staticText1.SetLabel(" ")
				self.m_staticText1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
				self.m_staticText1.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )

	def DownloadProcess(self,filename):   
		#Turn on multi-burning
		Errordetect = []
		StartTime = datetime.datetime.now()
		if(self.csrflashlib.flmOpen(self.devicenumber) == True):
			print("flmOpem successfully")
		else:
			for i in range(self.devicenumber):
				Error = self.csrflashlib.flmGetDeviceError(i)
				print(Error)
				if Error != 0:
					getattr(self, 'm_staticText' +str(i+3)).SetForegroundColour( wx.Colour( 255, 0, 0 ) )
					getattr(self, 'm_staticText' +str(i+3)).SetLabel(self.DeviceList[i])
					Errordetect.append((self.DeviceList[i])[:16])
				self.m_staticText1.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
				self.m_staticText1.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
				self.m_staticText1.SetLabel('Connection chip error.\nError Number:'+str(Errordetect)[:80]+'\n                     '+str(Errordetect)[80:])
		if(self.csrflashlib.flmReadProgramFiles(filename) == True):
			print("flmReadProgramFiles successfully")
		else:
			self.csrflashlib.flmClose(self.devicenumber)
		if(self.csrflashlib.flmProgramSpawn(self.devicenumber) != True):
			self.csrflashlib.flmClose(self.devicenumber)
			print("flmProgramSpawn faild")
			#self.m_staticText1.SetLabel("Download all Fail")
		else:
			print("flmProgramSpawn Successfully")
			#Get the download progress bar
			ProgressValue = 0
			ProgressStop = False
			#Determine if all burning processes are 100%
			while ProgressStop== False :
				self.working = 1
				for i in range(self.devicenumber):
					time.sleep(0.3)
					ProgressValue  +=self.csrflashlib.flmGetDeviceProgress(i)
					print("Process_%d = %d"%(i,self.csrflashlib.flmGetDeviceProgress(i))) 
					#Get progress parameters and set progress bar
					getattr(self, 'm_gauge' +str(i+1)).SetValue(self.csrflashlib.flmGetDeviceProgress(i)) 
				#Get the total number of running processes
				if ProgressValue == (i+1)*100:
					ProgressStop= True
				ProgressValue = 0
			DeviceErrors = locals()
			#Access programming error drive
			ErrorText = []
			for i in range(self.devicenumber):
				DeviceErrors['Device_%s' % i] = self.csrflashlib.flmGetDeviceError(i)
				print ("%s = %s"%(self.DeviceList[i],DeviceErrors['Device_%s' % i] ))
				#Determine if the returned value is 0
				if DeviceErrors['Device_%s' % i] != 0:
					#Error drive number plus 1
					self.DeviceErrorsNumber += 1
					print self.DeviceErrorsNumber
					#Error driver added to list
					ErrorText.append((self.DeviceList[i])[:16])
					getattr(self, 'm_staticText' +str(i+3)).SetForegroundColour( wx.Colour( 255, 0, 0 ) )
					getattr(self, 'm_staticText' +str(i+3)).SetLabel(self.DeviceList[i])
					getattr(self, 'm_gauge' +str(i+1)).SetValue(0)     

			self.csrflashlib.flmClose(self.devicenumber)
			self.m_staticText1.SetLabel("Write address in progress...")
			#Judge the write address error driver
			for i in range(self.devicenumber):
				self.WriteAddressFlag = self.AutomaticWriteAddress(i)
				if self.WriteAddressFlag == False:
					getattr(self, 'm_staticText' +str(i+3)).SetForegroundColour( wx.Colour( 255, 0, 0 ) )
					getattr(self, 'm_staticText' +str(i+3)).SetLabel(self.DeviceList[i])
					getattr(self, 'm_gauge' +str(i+1)).SetValue(0)   
					#Error driver added to list
					ErrorText.append((self.DeviceList[i])[:16])
						
				self.WriteAddressFlag == True

			ListError = list(set(ErrorText))
			EndTime = datetime.datetime.now()
			alltime = (EndTime-StartTime).seconds
			if self.DeviceErrorsNumber != 0:
				#Set the text font size displayed by the GUI interface
				self.m_staticText1.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
				self.m_staticText1.SetForegroundColour('blue')
				self.m_staticText1.SetLabel('Download completed.\nError Number:'+str(ListError))
			else:
				self.m_staticText1.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) )
				self.m_staticText1.SetForegroundColour('green')
				self.m_staticText1.SetLabel("Download all passed. Spend time = "+str(alltime)+"s")

			self.DeviceErrorsNumber = 0 
			self.working = 0


	def BoxChoice( self, event ):
		if  self.working == 0:
			self.RecoveryInterface()
			m_choice1Choices = self.DeviceList
			for i in range(self.devicenumber):
				print(self.m_choice1.GetString(self.m_choice1.GetSelection()))
				if (self.DeviceList[i])[:16] == self.m_choice1.GetString(self.m_choice1.GetSelection()):
					self.portnumber = i
					print("port number:")
					print (self.portnumber)
			self.m_staticText1.SetFont( wx.Font( 15, 70, 90, 90, False, wx.EmptyString ) )
			self.m_staticText1.SetLabel("The number of select read address drivers is: "+self.m_choice1.GetString(self.m_choice1.GetSelection()))
			print self.portnumber

	def ReadAddress( self ):
		try:
			if  self.working == 0:
				self.working = 1
				self.RecoveryInterface()
				(lap,uap,nap) = self.cst.ReadSerial(self.portnumber)
				print self.working
				#Determine if the read address is empty
				if(lap,uap,nap) != (0,0,0):
					self.m_staticText1.SetLabel("read success:{:04X}{:02X}{:06X}".format(nap, uap, lap ))
					self.m_textCtrl2.SetValue("{:04X}".format(nap))
					self.m_textCtrl3.SetValue("{:02X}".format(uap))
					self.m_textCtrl4.SetValue("{:06X}".format(lap))
					getattr(self, 'm_gauge' +str(self.portnumber+1)).SetValue(100) 
					self.m_staticText1.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) )
					self.m_staticText1.SetForegroundColour('green')
					self.m_staticText1.SetLabel("Read address successfully")
				else:
					getattr(self, 'm_staticText' +str(self.portnumber+3)).SetForegroundColour( wx.Colour( 255, 0, 0 ) )
					getattr(self, 'm_gauge' +str(self.portnumber+1)).SetValue(0) 
					self.m_staticText1.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) ) 
					self.m_staticText1.SetForegroundColour('red')
					self.m_staticText1.SetLabel("Read address Faile")
		except:
			self.m_staticText1.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) )
			self.m_staticText1.SetForegroundColour('red')
			self.m_staticText1.SetLabel("Read address fail")

		finally:
			self.working = 0

	def ReadChick( self, event ):
		if  self.working == 0:
			thread.start_new_thread(self.ReadAddress,())
		

	def AutomaticWriteAddress( self, devicenumber ):  
		#Read the Bluetooth address of the GUI interface
		nap=self.m_textCtrl2.GetValue()
		uap=self.m_textCtrl3.GetValue()
		lap=self.m_textCtrl4.GetValue()
		verify_ID = nap+uap+lap
		#Determine whether the read Bluetooth address length meets the requirements of 4+2+6
		if(len(verify_ID) ==12 and len(nap) ==4 and len(uap) == 2 and len(lap) == 6):
			print("input here OK")
			rex = re.compile('^[A-Fa-f0-9]{12}$')
		if rex.match(verify_ID):
			fag = self.cst.writeSerial(nap, uap, lap,devicenumber)
			if fag ==True:
				getattr(self, 'm_staticText' +str(devicenumber+13)).SetLabel(nap+"-"+uap+"-"+lap)
				#Bluetooth address is automatically added 1`
				self.g.serial = "{:012x}".format(int(verify_ID, 16) + 1)

				nap = int(self.g.serial[0:4], 16)
				uap = int(self.g.serial[4:6], 16)
				lap = int(self.g.serial[6:12], 16)
				
				self.m_textCtrl2.SetValue("{:04X}".format(nap))
				self.m_textCtrl3.SetValue("{:02X}".format(uap))
				self.m_textCtrl4.SetValue("{:06X}".format(lap))
				#getattr(self, 'm_staticText' +str(devicenumber+13)).SetLabel("{:04X}".format(nap)+"-"+"{:02X}".format(uap)+"-"+"{:06X}".format(lap))
				self.m_staticText1.SetLabel("Write address succeeded")
				return True
			else:
				self.m_staticText1.SetLabel("Write address fail")
				return False


		else:
			self.m_staticText1.SetLabel( "Input format error!!!\nThe correct format is: xxxx xx xxxxxx")
			return False

			


	#-----------------------------------------------------------------------------------------------------
	def WriteChick( self, event ):
		thread.start_new_thread(self.WriteAddress,())

	def WriteAddress( self ):
		try :
			if  self.working == 0:
				self.working = 1
				#Clear GUI display data
				self.RecoveryInterface()
				#Read the Bluetooth address of the GUI interface
				nap=self.m_textCtrl2.GetValue()
				uap=self.m_textCtrl3.GetValue()
				lap=self.m_textCtrl4.GetValue()
				print nap
				print uap
				print lap
				verify_ID = nap+uap+lap
		        #Determine whether the read Bluetooth address length meets the requirements of 4+2+6
				if(len(verify_ID) ==12 and len(nap) ==4 and len(uap) == 2 and len(lap) == 6):
					print("input here OK")
					rex = re.compile('^[A-Fa-f0-9]{12}$')
					if rex.match(verify_ID):
						#Open thread for multiple groups of burning
						#fag = thread.start_new_thread(self.cst.writeSerial,(nap, uap, lap,self.portnumber))
						fag = self.cst.writeSerial(nap, uap, lap,self.portnumber)
						if fag ==True:
							getattr(self, 'm_gauge' +str(self.portnumber+1)).SetValue(100) 
							self.m_staticText1.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) )
							self.m_staticText1.SetForegroundColour('green')
							self.m_staticText1.SetLabel("Write address succeeded")
						else:
							getattr(self, 'm_staticText' +str(self.portnumber+3)).SetForegroundColour( wx.Colour( 255, 0, 0 ) )
							getattr(self, 'm_gauge' +str(self.portnumber+1)).SetValue(0)  
							self.m_staticText1.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) )
							self.m_staticText1.SetForegroundColour('red')
							self.m_staticText1.SetLabel("Write address fail")


				else:
					getattr(self, 'm_staticText' +str(self.portnumber+3)).SetForegroundColour( wx.Colour( 255, 0, 0 ) )
					getattr(self, 'm_gauge' +str(self.portnumber+1)).SetValue(0)  
					self.m_staticText1.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) )
					self.m_staticText1.SetForegroundColour('red')
					self.m_staticText1.SetLabel( "Input format error!!!\nThe correct format is: xxxx xx xxxxxx")
		except:
			self.m_staticText1.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) )
			self.m_staticText1.SetForegroundColour('red')
			self.m_staticText1.SetLabel("Write address fail")

		finally:
			self.working = 0


	def ChooseClick( self, event ):
		if  self.working == 0:
			#Clear GUI display data
			self.RecoveryInterface()
			#Specify read file type
			wildcard = "*.xpv|*.xpv|*.xuv|*.xuv" 
			dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)

			if dlg.ShowModal() == wx.ID_OK:
				#Read successful return path 
				self.firmware = dlg.GetPath()
				self.m_textCtrl1.SetLabel( self.firmware)
				dlg.Destroy() 
				self.m_staticText1.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) ) 
				self.m_staticText1.SetLabel("Select the burning file as:\n"+self.firmware)
				self.working = 0


	def DownLoadChick( self, event ):
		try:
			if  self.working == 0:
				self.working = 1

				#Clear GUI display data
				self.RecoveryInterface()
				if self.firmware != None:
		            #Read the Bluetooth address of the GUI interface
					nap=self.m_textCtrl2.GetValue()
					uap=self.m_textCtrl3.GetValue()
					lap=self.m_textCtrl4.GetValue()
					verify_ID = nap+uap+lap
					#Determine whether the read Bluetooth address length meets the requirements of 4+2+6
					if(len(verify_ID) ==12 and len(nap) ==4 and len(uap) == 2 and len(lap) == 6):
						#Set the text font size displayed by the GUI interface
						self.m_staticText1.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) )
						self.m_staticText1.SetLabel( "Downloading.....")
						#Open thread for multiple groups of burning
						thread.start_new_thread(self.DownloadProcess,(self.firmware,))
					else: #An error message will appear if the production Bluetooth address is not entered correctly
						self.m_staticText1.SetFont( wx.Font( 15, 70, 90, 90, False, wx.EmptyString ) )
						self.m_staticText1.SetForegroundColour('red')
						self.m_staticText1.SetLabel("\n   Please enter the production Bluetooth address correctly!!!")

				else:
					self.m_staticText1.SetFont( wx.Font( 15, 70, 90, 90, False, wx.EmptyString ) )
					self.m_staticText1.SetForegroundColour('red')
					self.m_staticText1.SetLabel("\n   Please select the software you need to download!!!")

		finally:
			self.working = 0


	def IncrementSerial(self):     
		self.g.serial = "{:012x}".format(int(self.g.serial, 16) + 1)

	def DumpClick( self, event ):
		if  self.working == 0:
			#Clear GUI display data
			self.RecoveryInterface()
			self.m_staticText1.SetLabel("\n   This feature is not implemented!")
			pass

	def EraseClick( self, event ):
		if  self.working == 0:
			#Clear GUI display data
			self.RecoveryInterface()
			self.m_staticText1.SetFont( wx.Font( 25, 70, 90, 90, False, wx.EmptyString ) ) 
			if(self.csrflashlib.flmOpen(self.devicenumber) == True):
				print("flmOpem successfully")
				EraseState = self.csrflashlib.flmEraseBlock(self.devicenumber)
				if EraseState == 0:
					self.m_staticText1.SetForegroundColour('green')
					#self.m_staticText1.SetLabel("\n   This feature is not implemented!")
					self.m_staticText1.SetLabel("All Erase Successfully")
				else:
					self.m_staticText1.SetForegroundColour('red')
					self.m_staticText1.SetLabel("   Erase Fail!")

			self.csrflashlib.flmClose(self.devicenumber)
			

	def OnCloseMe(self, event):
		wx.MessageBox("Version information:\nv0.0.1", "About GT_QCFlash" ,wx.OK | wx.ICON_INFORMATION)

	def DetectDrive(self,event):
		if  self.working == 0:
			#Clear GUI display data
			self.RecoveryInterface()
			self.csrflashlib.flmClose(self.devicenumber)
			self.csrflashlib.flInit()
			(self.portsBuf,self.transBuf,self.numPortFound) = self.csrflashlib.flmGetAvailableSpiPorts()
			self.devicenumber = int(self.numPortFound)
			self.DeviceList = self.portsBuf.split(",")
			for i in range(8):
				if i < self.numPortFound:
					getattr(self, 'm_staticText' +str(i+3)).SetLabel(self.DeviceList[i]) 
				else:
					getattr(self, 'm_staticText' +str(i+3)).SetLabel("unknow") 

	def DeviceChoice( self, event ):
		self.RecoveryInterface()
		if self.m_choice4.GetString(self.m_choice4.GetSelection()) == "BC867x":
			self.working = 0
			print(self.m_choice4.GetString(self.m_choice4.GetSelection()))
			self.m_staticText1.SetLabel("Selected BC867x module")
		if self.m_choice4.GetString(self.m_choice4.GetSelection()) == "QCC300x":
			self.working = 1
			print(self.m_choice4.GetString(self.m_choice4.GetSelection()))
			self.m_staticText1.SetForegroundColour('red')
			self.m_staticText1.SetLabel("Selected QCC300x module.\nThis module function is not enabled")
			print("This module function is not enabled")