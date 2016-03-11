
"""
.. module:: transducer_services_base
   :platform: Unix, Windows
   :synopsis: Defines the abstract base class for IEEE1451.0 Transducer Services for
   ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""

import abc

class TimDiscoveryBase(object):
    """
    The TimDiscovery interface is provided by the IEEE 1451.0 layer
    and is called by the application to provide a common mechanism to
    discover available TIMs and TransducerChannels.
    The methods are listed in Table 84 and discussed in 10.1.1 through 10.1.3.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def report_comm_module(self, module_ids):
        """
        """
        return

    @abc.abstractmethod
    def report_tims(self, module_id, tim_ids):
        """
        """
        return

    @abc.abstractmethod
    def report_channels(self, tim_id, channel_ids, names):
        """
        """
        return


class TransducerAccessBase(object):
    """
    The TransducerAccess interface is provided by the IEEE 1451.0 layer and is called by the application to
    provide access to TransducerChannels. For most applications, they will primarily be interacting with this interface
    to perform TIM read and write operations. To keep this interface small, more advanced methods are placed in the
    TransducerManager interface. Each method is listed in Table 85.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def  open(self, timId, channelId, transCommId):
        return

    @abc.abstractmethod
    def  openQoS(self, timId, channelId, qosParams, transCommId):
        return

    @abc.abstractmethod
    def openGroup(self, timIds, channelIds, transCommId):
        return

    @abc.abstractmethod
    def openGroupQoS(self, timIds, channelIds, qosParams, transCommId):
        return

    @abc.abstractmethod
    def close(self, transCommId):
        return

    @abc.abstractmethod
    def readData (self, transCommId, timeout, SamplingMode, result):
        return

    @abc.abstractmethod
    def writeData (self, transCommId, timeout, SamplingMode, value):
        return

    @abc.abstractmethod
    def startReadData(self, transCommId, triggerTime, timeout, SamplingMode, callback, operationId):
        return

    @abc.abstractmethod
    def startWriteData(self, transCommId, triggerTime, timeout, SamplingMode, value, callback, operationId):
        return

    @abc.abstractmethod
    def startStream(self, transCommId, callback, operationId):
        return

    @abc.abstractmethod
    def cancel(self, operationId):
        return

class TransducerManagerBase(object):
    """

    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def lock(self, transCommId,  timeout):
        return

    @abc.abstractmethod
    def unlock(self, transCommId):
        return

    @abc.abstractmethod
    def reportLocks(self, transCommIds):
        return

    @abc.abstractmethod
    def breakLock(tself, ransCommId):
        return

    @abc.abstractmethod
    def sendCommand( self, transCommId, timeout, cmdClassId, cmdFunctionId, Args, outArgs):
        return

    @abc.abstractmethod
    def startCommand(self, transCommId, triggerTime, timeout, cmdClassId, cmdFunctionId, Args, callback, operationId):
        return

    @abc.abstractmethod
    def trigger(self, transCommId, triggerTime, timeout, SamplgMode):
        return

    @abc.abstractmethod
    def configureAttributes(self, transCommId, attributeNames):
        return

    @abc.abstractmethod
    def startTrigger(self, transCommId, triggerTime, timeout, SamplgMode, AppCallbackcallback, operationId):
        return

    @abc.abstractmethod
    def clear(self, transCommId, timeout, clearMode):
        return

    @abc.abstractmethod
    def registerStatusChange(self, transCommId, timeout, callback, operationId):
        return

    @abc.abstractmethod
    def unregisterStatusChange(self, transCommId):
        return


class TedsManagerBase(object):
    """

    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def readTeds(self, transCommId, timeout, tedsType, teds):
        return

    @abc.abstractmethod
    def writeTeds(self, transCommId, timeout, tedsType, teds):
        return

    @abc.abstractmethod
    def readRawTeds(self, transCommId, timeout, tedsType, rawTeds):
        return

    @abc.abstractmethod
    def writeRawTeds(self, transCommId, timeout, tedsType, rawTeds):
        return

    @abc.abstractmethod
    def updateTedsCache(self, transCommId, timeout, tedsType):
        return


class CommManagerBase(object):
    """

    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getCommModule(self, moduleId, commObject, type, technologyId):
        return

class ApiCallbackBase(object):
    """

    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def measurementUpdate(self, operationId, measValues, status):
        return

    @abc.abstractmethod
    def  actuationComplete(self, operationId, status):
        return

    @abc.abstractmethod
    def statusChange(self, operationId, status):
        return

    @abc.abstractmethod
    def commandComplete(self, operationId, outArgs, status):
        return

    @abc.abstractmethod
    def triggerComplete(self, operationId, status):
        return
