# -*- coding:utf8 -*-


class RDPInstance:

    def __init__(self):
        self.data = {}


    def enable_displayconnectionbar(self):
        self.data["displayconnectionbar"] = '1'

    def disable_displayconnectionbar(self):
        self.data["displayconnectionbar"] = '0'

    def enable_redirectprinters(self):
        self.data["redirectprinters"] = '1'

    def disable_redirectprinters(self):
        self.data["redirectprinters"] = '0'

    def enable_redirectclipboard(self):
        self.data["redirectclipboard"] = '1'

    def disable_redirectclipboard(self):
        self.data["redirectclipboard"] = '0'

    def