
"""
.. module:: transducer_services_mock
   :platform: Unix, Windows
   :synopsis: Defines the mock implementation for IEEE1451.0 Transducer Services for
   ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
import abc
from ncaplite.transducer_services_base import TimDiscoveryBase
from ncaplite.transducer_services_base import TransducerAccessBase
from ncaplite.transducer_services_base import TransducerManagerBase
from ncaplite.transducer_services_base import TedsManagerBase
from ncaplite.transducer_services_base import CommManagerBase
from ncaplite.transducer_services_base import ApiCallbackBase


class TimDiscoveryMock(TimDiscoveryBase):

    def report_comm_module(self, module_ids):
        """
        """
        return 0


    def report_tims(self, module_id, tim_ids):
        """
        """
        return 0


    def report_channels(self, tim_id, channel_ids, names):
        """
        """
        return 0

class TransducerAccessMock(TransducerAccessBase):

    def  open(self, timId, channelId, transCommId):
        return 0


    def  openQoS(self, timId, channelId, qosParams, transCommId):
        return 0


    def openGroup(self, timIds, channelIds, transCommId):
        return 0


    def openGroupQoS(self, timIds, channelIds, qosParams, transCommId):
        return 0


    def close(self, transCommId):
        return 0


    def readData (self, transCommId, timeout, SamplingMode, result):
        return 0


    def writeData (self, transCommId, timeout, SamplingMode, value):
        return 0


    def startReadData(self, transCommId, triggerTime, timeout, SamplingMode, callback, operationId):
        return 0


    def startWriteData(self, transCommId, triggerTime, timeout, SamplingMode, value, callback, operationId):
        return 0


    def startStream(self, transCommId, callback, operationId):
        return 0


    def cancel(self, operationId):
        return 0


class TransducerManagerMock(TransducerManagerBase):

    def lock(self, transCommId,  timeout):
        return 0


    def unlock(self, transCommId):
        return 0


    def reportLocks(self, transCommIds):
        return 0


    def breakLock(tself, ransCommId):
        return 0


    def sendCommand( self, transCommId, timeout, cmdClassId, cmdFunctionId, Args, outArgs):
        return 0


    def startCommand(self, transCommId, triggerTime, timeout, cmdClassId, cmdFunctionId, Args, callback, operationId):
        return 0


    def trigger(self, transCommId, triggerTime, timeout, SamplgMode):
        return 0


    def configureAttributes(self, transCommId, attributeNames):
        return 0


    def startTrigger(self, transCommId, triggerTime, timeout, SamplgMode, AppCallbackcallback, operationId):
        return 0


    def clear(self, transCommId, timeout, clearMode):
        return 0


    def registerStatusChange(self, transCommId, timeout, callback, operationId):
        return 0


    def unregisterStatusChange(self, transCommId):
        return 0


class TedsManagerMock(TedsManagerBase):

    def readTeds(self, transCommId, timeout, tedsType, teds):
        return 0


    def writeTeds(self, transCommId, timeout, tedsType, teds):
        return 0


    def readRawTeds(self, transCommId, timeout, tedsType, rawTeds):
        return 0


    def writeRawTeds(self, transCommId, timeout, tedsType, rawTeds):
        return 0


    def updateTedsCache(self, transCommId, timeout, tedsType):
        return 0


class CommManagerMock(CommManagerBase):

    def getCommModule(self, moduleId, commObject, type, technologyId):
        return 0

class ApiCallbackMock(ApiCallbackBase):

    def measurementUpdate(self, operationId, measValues, status):
        return 0


    def  actuationComplete(self, operationId, status):
        return 0


    def statusChange(self, operationId, status):
        return 0


    def commandComplete(self, operationId, outArgs, status):
        return 0


    def triggerComplete(self, operationId, status):
        return 0


if __name__ == '__main__':
    print 'Subclass:', issubclass(TimDiscoveryMock, TimDiscoveryBase)
    print 'Subclass:', issubclass(TransducerAccessMock, TransducerAccessBase)
    print 'Subclass:', issubclass(TransducerManagerMock, TransducerManagerBase)
    print 'Subclass:', issubclass(TedsManagerMock, TedsManagerBase)
    print 'Subclass:', issubclass(CommManagerMock, CommManagerBase)
    print 'Subclass:', issubclass(ApiCallbackMock, ApiCallbackBase)

    print 'Instance:', isinstance(TimDiscoveryMock(), TimDiscoveryBase)
    print 'Instance:', isinstance(TransducerAccessMock(), TransducerAccessBase)
    print 'Instance:', isinstance(TransducerManagerMock(), TransducerManagerBase)
    print 'Instance:', isinstance(TedsManagerMock(), TedsManagerBase)
    print 'Instance:', isinstance(CommManagerMock(), CommManagerBase)
    print 'Instance:', isinstance(ApiCallbackMock(), ApiCallbackBase)
