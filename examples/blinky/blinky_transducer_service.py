
"""
.. module:: transducer_services_Simple
   :platform: Unix, Windows
   :synopsis: Defines a simple example implementation for IEEE1451.0
   Transducer Services for ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
from ncaplite.transducer_services_base import TransducerAccessBase
import RPi.GPIO as GPIO


class TransducerAccessBlinky(TransducerAccessBase):

    def __init__(self):

        # LED0 (Pin7, GPIO4)  is channel 0
        # LED1 (Pin11, GPIO17) is channel 1
        self.LED0_PIN = 7
        self.LED1_PIN = 11

        # dictionary to store mapping between trans_comm_id and (tim,channel)
        self.transducer_interfaces = {
                                      1: (0, 0),  # comm_id0 : tim_id0, chanid0
                                      2: (0, 1),  # comm_id1 : tim_id0, chanid1
                                      }

        # dictionary to store mapping between trans_comm_id and LED_PIN
        self.led_pins = {
                        1: self.LED0_PIN,  # comm_id0 : LED0
                        2: self.LED1_PIN   # comm_id1 : LED1
                        }

        # initialize the board GPIO
        # to use Raspberry Pi board pin numbers
        GPIO.setmode(GPIO.BOARD)
        # set up GPIO output channels
        GPIO.setup(self.LED0_PIN, GPIO.OUT)
        GPIO.setup(self.LED1_PIN, GPIO.OUT)

    def find_com_id(self, tim_id, channel_id):
        """ Simple helper function to find trans_comm_id given
        a tim_id and channel_id. Assumes 0 is not a valid trans_comm_id.
        """
        for comid, tim in iter(self.transducer_interfaces.items()):
            if tim == (tim_id, channel_id):
                return comid
        return 0  # assumes 0 not valid comid

    def open(self, tim_id, channel_id):
        trans_comm_id = self.find_com_id(tim_id, channel_id)
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)
        return (error_code, trans_comm_id)

    def open_qos(self, tim_id, channel_id, qos_params):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)
        qos_params = ()
        trans_comm_id = 0
        return (error_code, qos_params, trans_comm_id)

    def open_group(self, tim_ids, channel_ids):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)
        trans_comm_id = 0
        return (error_code, trans_comm_id)

    def open_group_qos(self, tim_ids, channel_ids, qos_params):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)
        qos_params = ()
        trans_comm_id = 0
        return (error_code, qos_params, trans_comm_id)

    def close(self, trans_comm_id):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)
        return error_code

    def read_data(self, trans_comm_id, timeout, sampling_mode):
        # lookup pin and check state
        data = GPIO.input(self.led_pins[trans_comm_id])
        # append to result list
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)
        result = data
        return (error_code, result)

    def write_data(self, trans_comm_id, timeout, sampling_mode, value):
        pin = self.led_pins[trans_comm_id]

        if(value):
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)
        return error_code

    def start_read_data(self, trans_comm_id, trigger_time, timeout,
                        sampling_mode, callback):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)
        operation_id = 0
        return (error_code, operation_id)

    def start_write_data(self, trans_comm_id, trigger_time, timeout,
                         sampling_mode, value, callback):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)
        operation_id = 0
        return (error_code, operation_id)

    def start_stream(self, trans_comm_id, callback, operation_id):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)
        operation_id = 0
        return (error_code, operation_id)

    def cancel(self, operation_id):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)
        return error_code

if __name__ == '__main__':

    print('Subclass:', issubclass(TransducerAccessBlinky,
                                  TransducerAccessBase))

    print('Instance:', isinstance(TransducerAccessBlinky(),
                                  TransducerAccessBase))
