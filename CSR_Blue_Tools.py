# -*- coding: utf-8 -*-
import wx
import subprocess
import thread  
from six import with_metaclass
from CSR_Blue_Tools.wx_GUI import MyFrame1


if __name__ == '__main__':
  filename = r"C:\Users\Jaden\Desktop\test\TestTool\CSR_Blue_Tools\LR_Receiver_20170323.xpv"
  ex = wx.App() 
  WX_GUI = MyFrame1(None) 
#  thread.start_new_thread(WX_GUI.gauge_process,(filename,))
  ex.MainLoop()


