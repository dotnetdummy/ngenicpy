import json
from .base import NgenicBase
from ..const import API_PATH

class NodeStatus(NgenicBase):
    def __init__(self, token, json, node):
        self._parentNode = node

        super(NodeStatus, self).__init__(token, json)

    def getBatteryPercentage(self):
        if self["maxBattery"] == 0:
            # not using batteries
            return 100

        return int((self["battery"] / self["maxBattery"]) * 100)

    def getRadioSignalPercentage(self):
        if self["maxRadioStatus"] == 0:
            # shouldn't happen as of now (always maxRadioStatus is always 4)
            return 100

        return int((self["radioStatus"] / self["maxRadioStatus"]) * 100)