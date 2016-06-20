# -*- coding: utf-8 -*-
"""
.. module:: transducer_services_base
   :platform: Unix, Windows
   :synopsis: Defines the abstract base class for IEEE1451.0
   Transducer Services for ncaplite.

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
    def report_comm_module(self):
        """This method reports the available communication module
        interfaces that have been registered with this standard. See the:
        IEEE1451Dot0::ModuleCommunication::NetRegistration::registerModule( )
        method, which the IEEE 1451.X layer will invoke when it is ready for
        operation. In that method, the IEEE 1451.0 layer will assign a unique
        moduleId to each IEEE 1451.X interface. Note that the NCAP may have:
        A single IEEE 1451.X interface of a given technology
        (for example, Clause 7 of IEEE Std 1451.5- 2007 [B4]) .
        Multiple interfaces of the same technology
        (for example, IEEE 1451.2-RS232 on COM1 and COM2).
        Multiple IEEE 1451.X interfaces of different technologies
        (for example, Clause 7 of IEEE Std 1451.5-2007
        [B4] and IEEE 1451.3 multidrop).

        Returns:
        ErrorCode error_code: an error code
        UInt8Array module_ids: an array of module ids
        """
        error_code = 0
        module_ids = []
        return {'error_code': error_code, 'module_ids': module_ids}

    @abc.abstractmethod
    def report_tims(self, module_id):
        """This returns the known TIM devices on this interface. See
        IEEE1451Dot0::ModuleCommunication::Registration::registerDestination
        method, IEEE 1451.X layer will invoke when registering new TIMs
        to the NCAP.

        Args:
        UInt8 module_id: The “moduleId” parameter is the desired IEEE 1451.X
                    communication module ID. 11.6.2, the which the
        Returns:
        ErrorCode error_code: an error code
        UInt16Array tim_ids: a list which ontains all known TIMs on the
                            IEEE 1451.X module.
        """
        error_code = 0
        tim_ids = []
        return {'error_code': error_code, 'tim_ids': tim_ids}

    @abc.abstractmethod
    def report_channels(self, tim_id, channel_ids, names):
        """ This returns the TransducerChannel list and names for this TIM.
        This information is retrieved from the cached TEDS.

        Arga:
        UInt16 tim_id: the desired TIM.

        Returns:
        ErrorCode error_code: an error code
        UInt16Array channel_ids: is returned to the application and contains
                                all known TransducerChannels on this TIM.
        StringArray names: is returned to the application and contains the
               Transducer Channel names.
        """
        error_code = 0
        channel_ids = []
        names = []
        result = {'error_code': error_code,
                  'channel_ids': channel_ids,
                  'names': names}
        return result


class TransducerAccessBase(object):
    """
    The TransducerAccess interface is provided by the IEEE 1451.0 layer and is
    called by the application to provide access to TransducerChannels.
    For most applications, they will primarily be interacting with this
    interface to perform TIM read and write operations. To keep this interface
    small, more advanced methods are placed in the TransducerManager interface.
    Each method is listed in Table 85.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def open(self, tim_id, channel_id):
        """
        This method opens a communication link to the desired TIM and Channel
        and returns a "trans_comm_id" that will be used in subsequent calls.
        The default QoS will be used.

        Args:
            UInt16 tim_id: ID of the desired TIM
            UInt16 channel_id: the desired transducer channel
        Returns:
            ErrorCode error_code: an error code
            UInt16 trans_comm_id: The transport communications id. This acts
                                    as the handle for the current comms session
                                    with the TIM and Channel. This handle will
                                    be used in subsequent method calls to
                                    TransducerAccess
        """
        error_code = 0
        trans_comm_id = 0
        return {'error_code': error_code, 'trans_comm_id': trans_comm_id}

    @abc.abstractmethod
    def open_qos(self, tim_id, channel_id, qos_params):
        """This method opens a communication channel to the desired
        TIM/TransducerChannel and returns a “transCommId” that will be used in
        subsequent calls. Special Quality of Service communications are used.
        If the call fails, the “qosParams” will be modified and returned to the
        application in order to provide a “hint” on what QoS may be acceptable.

        Args:
        UInt16 tim_id: specifies the desired TIM.
        UInt16 channel_id: specifies the desired TransducerChannel.
                    This field allows addressing a single TransducerChannel,
                    a TransducerChannel proxy, a group of TransducerChannels
                    or all TransducerChannels connected to an NCAP. To address
                    the TIM use a TransducerChannel of zero.
                    See 5.3 for details.
        QosParams qos_params: the desired quality of service parameters.
                    See 9.3.1.3 for details.
        Returns:
        ErrorCode error_code: an error code
        QosParams qos_params: the desired quality of service parameters.
                    See 9.3.1.3 for details.
        UInt16 trans_comm_id: The transport communications id. This acts as the
        handle for the current comms session with the TIM and Channel.
        This handle will be used in subsequent method calls to
        TransducerAccess
        """
        error_code = 0
        qos_params = ()
        trans_comm_id = 0
        result = {'error_code': error_code,
                  'qos_params': qos_params,
                  'trans_comm_id': trans_comm_id}
        return result

    @abc.abstractmethod
    def open_group(self, tim_ids, channel_ids):
        """ This method opens a group communication channel to the desired set
        of TIMs/TransducerChannels and returns a “transCommId” that will be
        used in subsequent calls. The default Quality of Service is used. There
        is a one-to-one correspondence between the positions for the timIds and
        channelIds arrays. The TransducerChannels may be on the same or
        different TIMs. All TIMs shall be attached to the same communication
        module. If there are multiple channelIds for a given timId, the timId
        shall be repeated for each channelId within that TIM so that the two
        lists are of equal length.

        Args:
        UInt16Array tim_ids: ID of the desired TIMs
        UInt16Array channel_ids: specifies the desired TransducerChannels.
                                This field allows addressing a single
                                TransducerChannel, a TransducerChannel proxy,
                                a group of TransducerChannels, or all
                                TransducerChannels connected to an NCAP.
                                See 5.3 for details.
        Returns:
        ErrorCode error_code: an error code
        UInt16 trans_comm_id: The transport communications id. This acts as the
                                handle for the current comms session with the
                                TIM and Channel. This handle will be used in
                                subsequent method calls to TransducerAccess
        """
        error_code = 0
        trans_comm_id = 0
        return {'error_code': error_code, 'trans_comm_id': trans_comm_id}

    @abc.abstractmethod
    def open_group_qos(self, tim_ids, channel_ids, qos_params):
        """This method opens a group communication channel to the desired
        TIMs/TransducerChannels and returns a “transCommId” that will be used
        in subsequent calls. Special Quality of Service communications are
        used. If the call fails, the “qosParams” will be modified and returned
        to the application in order to provide a “hint” on what QoS may
        be acceptable. There is a one-to-one correspondence between the
        positions for the timIds and channelIds arrays.
        The TransducerChannels may be on the same or different TIMs.
        All TIMs must be attached to the same communication module.

        Args:
        UInt16Array tim_ids:     specifies the desired TIMs.
        UInt16Array channel_ids: specifies the desired TransducerChannels.
                    This field allows addressing a single TransducerChannel,
                    a TransducerChannel proxy, a group of TransducerChannels
                    or all TransducerChannels connected to an NCAP. To address
                    the TIM use a TransducerChannel of zero.
                    See 5.3 for details.
        QosParams qos_params: the desired quality of service parameters.
                    See 9.3.1.3 for details.

        Returns:
        ErrorCode error_code: an error code
        QosParams qos_params: the desired quality of service parameters.
                    See 9.3.1.3 for details.
        UInt16 trans_comm_id: The transport communications id. This acts as the
        handle for the current comms session with the TIM and Channel.
        This handle will be used in subsequent method calls to
        TransducerAccess
        """
        error_code = 0
        qos_params = ()
        trans_comm_id = 0
        result = {'error_code': error_code,
                  'qos_params': qos_params,
                  'trans_comm_id': trans_comm_id}
        return result

    @abc.abstractmethod
    def close(self, trans_comm_id):
        """ This method closes a transducer communication session.
        The application shall consider the transCommId as invalid.
        Note that a subsequent “open” call may return the old value.
        See TransducerManager::unlock( ) for information on calling close( )
        on a locked transCommId.

        Args:
        UInt16 trans_comm_id: The transport communications id indicates which
                                communication to close.

        Returns:
        error_code: an error code

        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def read_data(self, trans_comm_id, timeout, sampling_mode):
        """
        This method performs a blocking read of the specified
        TransducerChannel(s). The ArgumentArray can have many attributes
        as discussed in Clause 7 and Clause 8; each attribute is represented by
        a separate “Argument” in the ArgumentArray. The application can control
        which attributes are returned through the use of the
        TransducerManager::configureAttributes( ) call.

        In cases where this is a read of a single TransducerChannel, there will
        always be a “result” Argument that contains the TransducerChannel
        reading. The type of this Argument is determined by the
        TransducerChannel’s data model and if the TransducerChannel has a
        Calibration TEDS. For example, a read of a simple TransducerChannel
        that does not specify Calibration TEDS will always be in the
        TransducerChannel’s native format (for example, UInt8 or Float32Array).
        If the TransducerChannel does specify NCAP-side correction via the
        Calibration TEDS, the data type will always be Float32 or Float32Array.

        In cases where this is a read of a group of TransducerChannels, there
        will always be a nested “result” ArgumentArray that contains an
        Argument for each TransducerChannel in the group. These will be
        accessed in numerical order beginning with array position “0”.
        This organization corresponds to the order of TIM/TransducerChannel
        pairs in the openGroup( ) or openGroupQoS( ) call. The data type for
        each returned Argument will be like the single TransducerChannel read
        discussed in the previous paragraph. .

        Args:
        UInt16 trans_comm_id: the transport communications id
        TimeDuration timeout: the timeout
        UInt8 sampling_mode:  the desired sampling_mode


        Returns:
        ErrorCode error_code: an error_code
        ArgumentArray result: oputput ArgumentArray is the returned values.
        """
        error_code = 0
        result = ()
        return {'error_code': error_code, 'result': result}

    @abc.abstractmethod
    def write_data(self, trans_comm_id, timeout, sampling_mode, value):
        """
        This method performs a blocking write of the specified
        TransducerChannels. The ArgumentArray will have many attributes as
        discussed in Clause 7; each attribute will be represented by a separate
        “Argument” in the ArguemntArray. In cases where this is a write of a
        single TransducerChannel, the caller shall provide a “value” Argument
        that contains the TransducerChannel’s value. The caller should provide
        the result in a compatible data type to what the TransducerChannel
        requires as specified in the TransducerChannel TEDS. The IEEE 1451.0
        layer on the NCAP will perform simple conversions among all numeric
        data types. Note that this may lose precision if the resulting data
        type is smaller. For example, if the actuator required a UInt8, a
        provided Float32 would be downconverted to a UInt8 with appropriate
        loss of precision before being passed to the TransducerChannel.
        In cases where the NCAP will be performing correction (as specified in
        the Calibration TEDSfor this TransducerChannel), the value’s data type
        shall be numeric. It will be converted to a Float32 or Float32Array
        type before passing through the correction engine. The output of the
        correction engine will be converted to the form required by the
        actuators Data Model as defined in the TransducerChannel TEDS.

        In cases where this is a write to a group of TransducerChannels,
        there is always a nested “value” ArgumentArray that contains an
        Argument for each TransducerChannel in the group. These will be
        accessed in numerical order beginning with array position “0.”
        This organization corresponds to the order of TIM/TransducerChannel
        pairs in the openGroup( ) or openGroupQoS( ) call. The data type for
        each Argument shall follow the rules for the single TransducerChannel
        write case discussed in the previous paragraph

        Args:
        UInt16 trans_comm_id: indicates which transducer communication session
                            to use.
        TimeDuration timeout: specifies how long to wait to perform the reading
            without generating a time-out error. Note a time-out can occur due
            to communication or trigger failures.
        UInt8 sampling_mode: specifies the triggering mechanism. See 5.11 and
            7.1.2.4 for details. The “value” ArgumentArray is the provided
            actuator input values.
        ArgumentArray value: the ArgumentArray containing the value to send

        Returns:
        ErrorCode error_code: an error_code

        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def start_read_data(self, trans_comm_id, trigger_time, timeout,
                        sampling_mode, callback):
        """This method begins a non-blocking read of the specified
        TransducerChannels. When the read completes, the
        AppCallback::measurementUpdate( ) callback will be invoked on
        the callback object.

        Args:
        UInt16 trans_comm_id: indicates which transducer communication session
                                to use.
        TimeInstance trigger_time: specifies when to begin the read operation.
                        A value specified in the past will result in an
                        immediate time-out failure. A value of
                        secs == 0, nsecs == 0 is aspecial case that
                        implies read immediately.
        TimeDuration timeout: specifies how long to wait after initiating the
                        read operation without generating a time-out error.
                        Note a time-out can occur due to communication or
                        trigger failures.
        UInt8 sampling_mode: pecifies the triggering mechanism. See 5.11 and
                        7.1.2.4 for details. The “value” ArgumentArray
                        is the provided actuator input values.
        AppCallback callback: the interface to invoke when the read has
                            completed. It will also be invoked upon failures.

        Returns:
        ErrorCode error_code: an error code
        UInt16 operation_id: an identifier that can be used to cancel
                      the read request.
        """
        error_code = 0
        operation_id = 0
        return {'error_code': error_code, 'operation_id': operation_id}

    @abc.abstractmethod
    def start_write_data(self, trans_comm_id, trigger_time, timeout,
                         sampling_mode, value, callback):
        """This method begins a non-blocking read of the specified
        TransducerChannels. When the read completes, the
        AppCallback::measurementUpdate( ) callback will be invoked on the
        callback object.

        Args:
        UInt16 trans_comm_id: indicates which transducer communication session
                                to use.
        TimeInstance trigger_time: specifies when to begin the read operation.
                        A valuespecified in the past will result in an
                        immediate time-out failure.
                        A value of secs == 0, nsecs == 0 is a
                        special case that implies read immediately.
        TimeDuration timeout: specifies how long to wait after initiating
                    the read operation without generating a time-out error.
                    Note a time-out can occur due to communication or trigger
                    failures.
        UInt8 sampling_mode: pecifies the triggering mechanism. See 5.11 and
                        7.1.2.4 for details. The “value” ArgumentArray
                        is the provided actuator input values.
        ArgumentArray value: the value to send
        AppCallback callback: the interface to invoke when the read has
                    completed. It will also be invoked upon failures.
        Returns:
        ErrorCode error_code: an error code
        UInt16 operation_id: an identifier that can be used to cancel
                      the read request.
        """
        error_code = 0
        operation_id = 0
        return {'error_code': error_code, 'operation_id': operation_id}

    @abc.abstractmethod
    def start_stream(self, trans_comm_id, callback, operation_id):
        """This method begins operation of a measurement stream.
        The transCommId shall be created with either the openQoS( ) or the
        openGroupQoS( ) call. In the later case, all TransducerChannels shall
        be from the same TIM. Each time new measurements are available from the
        stream, the AppCallback::measurementUpdate( ) callback will be invoked
        on the callback object.

        Args:
        UInt16 trans_comm_id: indicates which transducer communication
                                session to use.
        AppCallback callback: the interface to invoke when a data set has been
                            written to an actuator or received from a sensor.
                            It will also be invoked upon failures.

        Returns:
        ErrorCode error_code: an error code
        UInt16 operation_id: an identifier that can be used to cancel
                      the read request.

        """
        error_code = 0
        operation_id = 0
        return {'error_code': error_code, 'operation_id': operation_id}

    @abc.abstractmethod
    def cancel(self, operation_id):
        """This method will cancel a blocking read, blocking write, or
        measurement stream. The callback will be invoked with a CANCEL status
        error code.

        Args:
        UInt16 operation_id: specifies the operation to cancel.

        Returns:
        ErrorCode error_code: an error code
        """
        error_code = 0
        return {'error_code': error_code}


class TransducerManagerBase(object):
    """The TransducerManager interface (see Table 86) is provided by this
    system and is called by the application to provide access to more advanced
    features. For most applications, they will not interact with this interface
    but will primarily be interacting with the TransducerAccess interface to
    perform TransducerChannel read and write operations. Advanced methods are
    placed in the TransducerManager interface to keep the
    TransducerAccess class small.

    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def lock(self, trans_comm_id, timeout):
        """This method will lock the TIM/TransducerChannels represented by the
        transCommId. This will prevent other applications from accessing those
        resources. To prevent deadlocks in multi-threaded environments, it is
        the application’s responsibility to lock resources
        in agreed upon order.

        The implementation shall allow multiple locks by the same calling
        thread without blocking. In cases where the transCommId specifies a
        group, all TIM/TransducerChannels in that group will be locked
        sequentially in the order specified in the openGroup( ) or
        openGroupQoS( ) call.

        Args:
        UInt16 trans_comm_id: specifies the desired transducer communication
                            session.
        TimeDuration timeout: specifies the duration to wait when acquiring the
                    lock. A value of secs == 0, nsecs == 0 implies no wait and
                    can be used to test for an existing lock.
                    A value of secs == 0, nsecs == –1 implies wait forever.
                    Using a value of “wait forever”
                    is extremely dangerous as it can create deadlocks.

        Returns:
        ErrorCode rror_code: an error code
        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def unlock(self, trans_comm_id):
        """This method will unlock the TIM/TransducerChannels represented by
        the transCommId. This will allow other applications to access those
        resources. In cases where the application has called lock( ) multiple
        times with the same calling thread, the application shall ensure that
        unlock( ) is called the same number of times. When the last unlock( )
        is invoked, the resources are now available. The implementation shall
        allow an alternative calling thread to invoke unlock( ).
        This alternative only is valid when lock( ) has been called a single
        time. An example would be a non-blocking operation. The initiating
        thread calls open( ), lock( ), and the non-blocking read( ).
        When the read completes, the AppCallback::measurementUpdate( ) callback
        will be invoked. That thread may then call unlock( ). A call to
        close( ) will result in unlock( ) being called the correct number of
        times. A warning error code will be returned to signal that a close on
        a locked resource was performed.

        Args:
        UInt16 trans_comm_id: specifies the desired transducer communication
                                session.

        Returns:
        ErrorCode error_code: an error code
        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def report_locks(self):
        """ This method will report all transCommIds that are currently locked.

        Returns:
        ErrorCode error_code: an error code
        UInt16 trans_comm_ids: an array of locked IDs.
        """
        error_code = 0
        trans_comm_ids = []
        return {'error_code': error_code, 'trans_comm_ids': trans_comm_ids}

    @abc.abstractmethod
    def break_lock(self, trans_comm_id):
        """This method will break a lock. If a non-blocking read or write or
        measurement stream is in progress, the callback will be invoked with an
        appropriate error code. See Table 78 for the list of error codes.

        Args:
        UInt16 trans_comm_id: specifies the desired transducer communication
                                session.

        Returns:
        ErrorCode error_code: an error code
        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def send_command(self, trans_comm_id, timeout, cmd_class_id,
                     cmd_function_id, in_args):
        """This method will perform a blocking operation. The format of input
        and output arguments are command dependent. The caller shall make sure
        to use the correct data types for each input argument.

        If this is a custom command, the application must use Command TEDS and
        this argument array must contain the octetArray containing the command.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        TimeDuration timeout: the maximum time to wait before a time-out error.
                    A value of secs == 0, nsecs == –1 means “wait forever.”
        UInt8 cmd_class_id: the desired command class code. See Table 15 for
                            details.
        UInt8 cmd_function_id: the desired command function code. See Clause 7
                            for details.
        ArgumentArray in_args: the input arguments in ArgumentArray form.

        Returns:
        ErrorCode error_code: an error code
        ArgumentArray out_args: returned output arguments.
        """
        out_args = []
        error_code = 0
        return {'error_code': error_code, 'out_args': out_args}

    @abc.abstractmethod
    def send_command_raw(self, trans_comm_id, timeout, cmd_class_id,
                         cmd_function_id, in_args):
        """This method will perform a blocking operation. The format of input
        and output arguments are command dependent. The caller shall make sure
        to use the correct data types for each input argument.

        If this is a custom command, the application must use Command TEDS and
        this argument array must contain the octetArray containing the command.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        TimeDuration timeout: the maximum time to wait before a time-out error.
                    A value of secs == 0, nsecs == –1 means “wait forever.”
        UInt8 cmd_class_id: the desired command class code.
        See Table 15 for details.
        UInt8 cmd_function_id: the desired command function code. See Clause 7
                            for details.
        OctetArray in_args: the input arguments in OctetArray form.

        Returns:
        ErrorCode error_code: an error code
        OctetArray out_args: returned output arguments.
        """
        out_args = []
        error_code = 0
        return {'error_code': error_code, 'out_args': out_args}

    @abc.abstractmethod
    def start_command(self, trans_comm_id, trigger_time, timeout, cmd_class_id,
                      cmd_function_id, in_args, callback):
        """This method starts a non-blocking operation. The format of input
        arguments are command dependent. The caller shall make sure to use the
        correct data types for each input argument.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        TimeInstance trigger_time: specifies when to begin the operation.
                        A value specified in the past will result in an
                        immediate time-out failure. A value of
                        secs == 0, nsecs == 0 is a special
                        case that implies immediate action.
        TimeDuration timeout: the maximum time to wait before a time-out error.
                    A value of secs == 0, nsecs == –1 means “wait forever.”
        UInt8 cmd_class_id: the desired command class code. See Table 15 for
                            details.
        UInt8 cmd_function_id: the desired command function code. See Clause 7
                            for details.
        ArgumentArray in_args: the input arguments in ArgumentArray form.
        AppCallback callback: specifies the callback interface.
                    The AppCallback::commandComplete( ) method will be invoked.
        Returns:
        ErrorCode error_code: an error code
        ArgumentArray operation_id: the returned operation ID

        """
        operation_id = 0
        error_code = 0
        return {'error_code': error_code, 'operation_id': operation_id}

    @abc.abstractmethod
    def configure_attributes(self, trans_comm_id, attribute_names):
        """This method configures a transCommId for read or measurement stream
        operations. It specifies which attributes to include in the returned
        ArgumentArray. See Clause 7 and Clause 8 for details on appropriate
        names.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        StringArray attribute_names: specifies the names of desired attributes

        Returns:
        ErrorCode error_code: an error code
        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def trigger(self, trans_comm_id, trigger_time, timeout, sampling_mode):
        """This method performs a blocking trigger on the specified transCommId.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        TimeInstance trigger_time: specifies when to begin the read operation.
                            A value specified in the past will result in an
                            immediate time-out failure.
                            A value of secs == 0, nsecs == 0 is a
                            special case that implies read immediately.
        TimeDuration timeout: specifies how long to wait to perform the reading
                        without generating a time-out error. Note a time-out
                        can occur due to communication or trigger failures.
        UInt8 sampling_mode: pecifies the triggering mechanism. See 5.11 and
        7.1.2.4 for details. The “value” ArgumentArray is the provided
        actuator input values.

        Returns:
        ErrorCode error_code: an error code
        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def start_trigger(self, trans_comm_id, trigger_time, timeout,
                      sampling_mode, callback):
        """This method begins a non-blocking trigger on the specified
        transCommId.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        TimeInstance trigger_time: specifies when to begin the read operation.
                        A value specified in the past will result in an
                        immediate time-out failure.
                        A value of secs == 0, nsecs == 0 is a
                        special case that implies read immediately.
        TimeDuration timeout: specifies how long to wait to perform the reading
                    without generating a time-out error. Note a time-out can
                    occur due to communication or trigger failures.
        UInt8 sampling_mode: pecifies the triggering mechanism. See 5.11 and
                        7.1.2.4 for details. The “value” ArgumentArray is the
                        provided actuator input values
        AppCallback callback: the interface to invoke when the read has
                    completed. It will also be invoked upon failures.

        Returns:
        ErrorCode error_code: an error code
        UInt16 operation_id: an identifier that can be used to cancel
                      the read request.
        """
        operation_id = 0
        error_code = 0
        return {'error_code': error_code, 'operation_id': operation_id}

    @abc.abstractmethod
    def clear(self, trans_comm_id, timeout, clear_mode):
        """ This method performs a clear on the specified transCommId.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        TimeDuration timeout: the maximum time to wait before a time-out error.
                    A value of secs == 0, nsecs == –1 means “wait forever.”
        UInt8 clear_mode: The “clearMode” specifies the clear mode as shown
                            below

                        0: Reserved
                        1: Clear All
                        2: Clear communications channel
                        3: Clear buffers
                        4: Reset TIM state machine
                        5: Clear TEDS cache
                        6-127: Reserved
                        128-255: Open to manufacturers

        Returns:
        ErrorCode error_code: an error code
        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def register_status_change(self, trans_comm_id, timeout, callback):
        """This method registers an application callback for TIM status change
        events on the specified transCommId.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        TimeDuration timeout: the maximum time to wait before a time-out error.
                    A value of secs == 0, nsecs == –1 means “wait forever.”
        AppCallback : specifies the callback interface.
                    The AppCallback::statusChange( ) method will be invoked.
        Returns:
        ErrorCode rror_code: an error code
        UInt16 operation_id: the returned operation ID
        """
        operation_id = 0
        error_code = 0
        return {'error_code': error_code, 'operation_id': operation_id}

    @abc.abstractmethod
    def unregister_status_change(self, trans_comm_id):
        """ This method unregisters an application callback for TIM status
        change events on the specified transCommId.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.

        Returns:
        ErrorCode error_code: an error code
        """
        error_code = 0
        return {'error_code': error_code}


class TedsManagerBase(object):
    """
    The TedsManager interface is provided by the IEEE 1451.0 layer and is
    called by the application to provide access to the TEDS. The methods in
    this interface are listed in Table 88.
    """
    _metaclass_ = abc.ABCMeta

    @abc.abstractmethod
    def read_teds(self, trans_comm_id, timeout, teds_type, teds):
        """This method will read the desired TEDS block from the TEDS cache. If
        the TEDS is not available from the cache, it will read the TEDS from
        the TIM. The TEDS information is returned in an ArgumentArray.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        TimeDuration timeout: specifies the duration to wait before returning
                    a time-out error if no response is received.
                    A value of secs == 0, nsecs == 0 implies no wait and may be
                    used to only read from the cache.
                    A value of secs == 0, nsecs == –1 implies wait forever.
        UInt8 teds_type:  specifies what TEDS to return. See Table 17 for TEDS
                    access codes.

        Returns:
        ErrorCode rror_code: an error code
        ArgumentArray teds: ArgumentArray that contains the TEDS information.
                            The values may be retrieved by attribute name.
                            See Clause 8 for TEDS field names.

        """
        error_code = 0
        teds = []
        return {'error_code': error_code, 'teds': teds}

    @abc.abstractmethod
    def write_teds(self, trans_comm_id, timeout, teds_type, teds):
        """This method will write the desired TEDS block to the TIM. The TEDS
        cache is also updated if the write succeeds. The provided TEDS
        information is encoded in an ArgumentArray. It will be converted
        internally to the correct “tuple” form and will be transferred to the
        TIM in an OctetArray.

        The ArgumentArray shall include all the required TEDS fields for the
        type of TEDS being written. An error will be returned if a required
        TEDS field is missing.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        TimeDuration timeout: specifies the duration to wait before returning
                    a time-out error if no response is received. A value of
                    secs == 0, nsecs == 0 implies no wait and may be used to
                    only read from the cache. A value of secs == 0, nsecs == –1
                    implies wait forever.
        UInt8 teds_type:  specifies what TEDS to return. See Table 17 for TEDS
                    access codes.
        ArgumentArray teds: ArgumentArray contains the TEDS information.
                            The values may be retrieved by attribute name.
                            See Clause 8 for TEDS field names.

        Returns:
        ErrorCode error_code: an error code
        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def read_raw_teds(self, trans_comm_id, timeout, teds_type):
        """This method will read the desired TEDS block from the TEDS bypassing
         the TEDS cache. The TEDS information is returned in its raw OctetArray
         form. The TEDS cache will not be updated.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        TimeDuration timeout: specifies the duration to wait before returning a
                    time-out error if no response is received.
                    A value of secs == 0, nsecs == 0 implies no wait and may
                    be used to only read from the cache.
                    A value of secs == 0, nsecs == –1 implies wait forever.
        UInt8 teds_type:  specifies what TEDS to return. See Table 17 for TEDS
                    access codes.

        Returns:
        ErrorCode error_code: an error code
        OctetArray raw_teds: OctetArray contains the raw TEDS information
                             in “tuple” form.
        """
        error_code = 0
        raw_teds = ()
        return {'error_code': error_code, 'raw_teds': raw_teds}

    @abc.abstractmethod
    def write_raw_teds(self, trans_comm_id, timeout, teds_type, raw_teds):
        """This method will write the desired TEDS block to the TIM bypassing
        the TEDS cache. The provided TEDS information is encoded in “tuple”
        form in an OctetArray. No verification of the OctetArray will be
        performed.

        CAUTION:
        Be sure to include all required TEDS fields in the OctetArray because
        what is written by this method will replace the entire TEDS.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        TimeDuration timeout: specifies the duration to wait before returning
                    a time-out error if no response is received.
                    A value of secs == 0, nsecs == 0 implies no wait and may
                    be used to only read from the cache.
                    A value of secs == 0, nsecs == –1 implies wait forever.
        UInt8 teds_type:  specifies what TEDS to return. See Table 17 for TEDS
                    access codes.
        OctetArray raw_teds: OctetArray contains the raw TEDS information in
                            “tuple” form.

        Returns:
        ErrorCode error_code: an error code
        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def update_teds_cache(self, trans_comm_id, timeout, teds_type):
        """This method will update the TEDS cache. The TEDS checksum will be
        read from the TIM and compared with the cached TEDS checksum.
        If the checksums differ, the TEDS will be read from the TIM and stored
        in the cache.

        Args:
        UInt16 trans_comm_id: specifies the transducer communication session.
        TimeDuration timeout: specifies the duration to wait before returning a
                    time-out error if no response is received.
                    A value of secs == 0, nsecs == 0 implies no wait and may be
                    used to only read from the cache.
                    A value of secs == 0, nsecs == –1 implies wait forever.
        UInt8 teds_type:  specifies what TEDS to return. See Table 17 for TEDS
                    access codes.

        Returns:
        ErrorCode error_code: an error code
        """
        error_code = 0
        return {'error_code': error_code}


class CommManagerBase(object):
    """The CommManager interface is provided by the IEEE 1451.0 layer and is
    called by the application to provide a common mechanism to manage available
    communications on an NCAP.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_comm_module(self, module_id):
        """ This returns the abstract “Comm” object for applications that need
        to bypass IEEE 1451.0 processing and interact directly with the
        underlying communications object. By consulting the “type” parameter,
        the application can safely downcast to either the “P2PComm” or the
        “NetComm” object. Applications must use extreme caution when accessing
        the underlying “Comm” objects as incorrect usage may compromise the
        IEEE 1451.0 layer. This method is provided to allow expansion beyond
        the IEEE 1451.0 architecture.

        Args:
        UInt8 module_id: the desired communications module ID.

        Returns:
        ErrorCode rror_code: an error code
        ModuleCommunication comm_object: a reference to the underlying comms
                                        object.
        UInt8 comm_type: “type” parameter is returned to the application in
                    order to allow a safe downcast. Valid values are
                    represented in the technology_id which specifies the
                    underlying IEEE 1451.X technology. See Table 90.
        UInt8 technology_id: specifies the underlying IEEE 1451.X technology.
                        See Table 99

        Table 90: Comm type enumerations
        0: P2P_TYPE
        1: NET_COMM_TYPE
        2-255: Reserved
        """
        error_code = 0
        comm_object = None
        comm_type = 255
        technology_id = 0
        result = {'error_code': error_code,
                  'comm_object': comm_object,
                  'comm_type': comm_type,
                  'technology_id': technology_id}

        return result


class ApiCallbackBase(object):
    """ The AppCallback interface is provided by applications and is called by
    the IEEE 1451.0 layer to provide access to non-blocking I/O and
    measurement streams.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def measurement_update(self, operation_id, meas_values, status):
        """ This method will be invoked following a startRead( ) or
        startStream( ) call. For non-blocking operations, it provides
        measurements back to the application. For the stream case, this
        callback will be invoked every time new measurement data are available.

        Args:
        UInt16 operation_id: the desired operation ID that was returned in the
                      startRead( ) or startStream( ) call.
        ArgumentArray meas_values: contains the measurement information.
                        The values may be retrieved by attribute name.
                        See Clause 7 for attribute names. See 10.2.6 read( )
                        for more details
        UInt16 status: specifies the error code from the non-blocking read or
                        stream operation

        Returns:
        ErrorCode error_code: The application shall return a status code back
                            to the IEEE 1451.0 layer. See 9.3.1.2 for
                            error codes.
        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def actuation_complete(self, operation_id, status):
        """ This method will be invoked following a startWrite( ) call.
        For non-blocking operations, it provides status information back to the
        application.

        Args:
        UInt16 operation_id: the desired operation ID that was returned in the
                        startWrite( ) call.
        UInt16 status: specifies the error code from the non-blocking write
                        operation

        Returns:
        ErrorCode error_code: The application shall return a status code back
                        to the IEEE 1451.0 layer. See 9.3.1.2 for error codes.
        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def status_change(self, operation_id, status):
        """This method will be invoked following a registerStatusChange( ) call.

        Args:
        UInt16 operation_id: specifies the desired operation ID that was
                    returned in the registerStatusChange( ) call.

        UInt16 status: specifies the TIM or TransducerChannel status
                        information.

        Returns:
        ErrorCode error_code: The application shall return a status code back
                        to the IEEE 1451.0 layer. See 9.3.1.2 for error codes.
        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def command_complete(self, operation_id, out_args, status):
        """This method will be invoked following a startCommand( ).
        It provides the output ArgumentArray back to the application.

        Args:
        UInt16 operation_id: specifies the desired operation ID that was
                            returned in the startRead( ) or
                            startStream( ) call.
        ArgumentArray out_args: contains the returned ArgumentArray.
                            This informationis specific to each command.
        UInt16 status: specifies the error code from the non-blocking
                    send command operation..

        Returns:
        ErrorCode error_code: The application shall return a status code back
                        to the IEEE 1451.0 layer. See 9.3.1.2 for error codes.

        """
        error_code = 0
        return {'error_code': error_code}

    @abc.abstractmethod
    def trigger_complete(self, operation_id, status):
        """This method will be invoked following a startTrigger( ). It provides
        status information to inform the application when the trigger has
        completed.

        Args:
        UInt16 operation_id: specifies the desired operation ID that was
            returned in the startTrigger( ) call.
        UInt16 status: specifies the error code from the non-blocking trigger
                    command operation.

        Returns:
        ErrorCode error_code: The application shall return a status code back
                    to the IEEE 1451.0 layer. See 9.3.1.2 for error codes.
        """
        error_code = 0
        return {'error_code': error_code}
