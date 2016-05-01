
"""
.. module:: transducer_services_Simple
   :platform: Unix, Windows
   :synopsis: Defines a simple example implementation for IEEE1451.0
   Transducer Services for ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""


from ncaplite.transducer_services_base import TransducerAccessBase


class TransducerAccessSimple(TransducerAccessBase):

    def __init__(self):
        self.transducer_interfaces = {
                                      1: (0, 0),  # comm_id0 : tim_id0, chanid0
                                      2: (0, 1),  # comm_id1 : tim_id0, chanid1
                                      3: (1, 0),  # comm_id2 : tim_id1, chanid0
                                      }

        self.out_data = {1: 0, 2: 0, 3: 0}
        self.in_data = {1: 0, 2: 0, 3: 0}

    def find_com_id(self, tim_id, channel_id):
        """ Simple helper function to find trans_comm_id given
        a tim_id and channel_id. Assumes 0 is not a valid trans_comm_id.
        """
        for comid, tim in self.transducer_interfaces.iteritems():
            if tim == (tim_id, channel_id):
                return comid
        return 0  # assumes 0 not valid comid

    def open(self, tim_id, channel_id):
        trans_comm_id = self.find_com_id(tim_id, channel_id)
        print("open: " + str(trans_comm_id))
        return trans_comm_id

    def open_qos(self, tim_id, channel_id, qos_params, trans_comm_id):
        return 0

    def open_group(self, tim_ids, channel_ids, trans_comm_id):
        return 0

    def open_group_qos(self, tim_ids, channel_ids, qos_params, trans_comm_id):
        return 0

    def close(self, trans_comm_id):
        return 0

    def read_data(self, trans_comm_id, timeout, sampling_mode, result):
        data = self.out_data[trans_comm_id]
        result.append(data)
        tmp = (trans_comm_id, self.out_data[trans_comm_id])
        print("read data: " + str(tmp))
        data = data+1
        self.out_data[trans_comm_id] = data
        return 0

    def write_data(self, trans_comm_id, timeout, sampling_mode, value):
        self.in_data[trans_comm_id] = value
        tmp = (trans_comm_id, self.in_data[trans_comm_id])
        print("write data: " + str(tmp))
        return

    def start_read_data(self, trans_comm_id, trigger_time, timeout,
                        sampling_mode, callback, operation_id):
        return

    def start_write_data(self, trans_comm_id, trigger_time, timeout,
                         sampling_mode, value, callback, operation_id):
        return

    def start_stream(self, trans_comm_id, callback, operation_id):
        return

    def cancel(self, operation_id):
        return

if __name__ == '__main__':

    print('Subclass:', issubclass(TransducerAccessSimple,
                                  TransducerAccessBase))

    print('Instance:', isinstance(TransducerAccessSimple(),
                                  TransducerAccessBase))
