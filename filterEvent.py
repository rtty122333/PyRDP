# -*- coding: utf-8 -*- #
import pythoncom
import pyHook

class Filter():

    def __init__(self):
        #scancode nums esc ctl alt
        self.filterObj = [1,29,56]
        self.hm = pyHook.HookManager()
        self.hm.KeyDown = self.onKeyboardEvent
        self.hm.HookKeyboard()
        # hm.MouseAll = onMouseEvent
        # hm.HookMouse()
        pythoncom.PumpMessages(100000)

    def onKeyboardEvent(self,event):
        if event.ScanCode in self.filterObj:
            return False
        else:
            return True

# if __name__ == "__main__":
#     filterObj = Filter()
