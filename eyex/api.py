from collections import namedtuple
import ctypes as c
import eyex.types as tx

Sample = namedtuple('Sample', ['data_mode', 'timestamp', 'x', 'y'])


class EyeXInterface(object):
    on_event = []

    def __init__(self, lib_location = 'C:\\Users\\stern\\OneDrive\\Pulpit\\Nowy Folder\\eyetracker_data_colection\\eyetracker_data_colection\\eyex\\Tobii.EyeX.Client.dll'):

        self.eyex_dll = c.cdll.LoadLibrary(lib_location)

        # Define argument and return types for functions
        self.eyex_dll.txInitializeEyeX.argtypes = [c.c_int, c.c_voidp, c.c_voidp, c.c_voidp]
        self.eyex_dll.txInitializeEyeX.restype = c.c_int

        self.eyex_dll.txCreateContext.argtypes = [c.POINTER(c.c_voidp), c.c_int]
        self.eyex_dll.txCreateContext.restype = c.c_int

        self.eyex_dll.txRegisterConnectionStateChangedHandler.argtypes = [c.c_voidp, c.POINTER(c.c_int),
                                                                          tx.CONNECTION_HANDLER, c.c_voidp]
        self.eyex_dll.txRegisterConnectionStateChangedHandler.restype = c.c_int

        self.eyex_dll.txRegisterEventHandler.argtypes = [c.c_voidp, c.POINTER(c.c_int), tx.EVENT_HANDLER, c.c_voidp]
        self.eyex_dll.txRegisterEventHandler.restype = c.c_int

        self.eyex_dll.txEnableConnection.argtypes = [c.c_voidp]
        self.eyex_dll.txEnableConnection.restype = c.c_int

        self.eyex_dll.txDisableConnection.argtypes = [c.c_voidp]
        self.eyex_dll.txDisableConnection.restype = c.c_int

        self.eyex_dll.txShutdownContext.argtypes = [c.c_voidp, c.c_int, c.c_int]
        self.eyex_dll.txShutdownContext.restype = c.c_int

        self.eyex_dll.txReleaseContext.argtypes = [c.POINTER(c.c_voidp)]
        self.eyex_dll.txReleaseContext.restype = c.c_int

        self.eyex_dll.txGetAsyncDataContent.argtypes = [c.c_voidp, c.POINTER(c.c_voidp)]
        self.eyex_dll.txGetAsyncDataContent.restype = c.c_int

        self.eyex_dll.txGetEventBehavior.argtypes = [c.c_voidp, c.POINTER(c.c_voidp), c.c_uint]
        self.eyex_dll.txGetEventBehavior.restype = c.c_int

        self.eyex_dll.txGetGazePointDataEventParams.argtypes = [c.c_voidp, c.POINTER(tx.TX_GAZEPOINTDATAEVENTPARAMS)]
        self.eyex_dll.txGetGazePointDataEventParams.restype = c.c_int

        self.eyex_dll.txReleaseObject.argtypes = [c.POINTER(c.c_voidp)]
        self.eyex_dll.txReleaseObject.restype = c.c_int

        # Initialize EyeX system
        ret = self.eyex_dll.txInitializeEyeX(tx.TX_SYSTEMCOMPONENTOVERRIDEFLAGS.TX_SYSTEMCOMPONENTOVERRIDEFLAG_NONE,
                                             None, None, None)
        if ret != tx.TX_RESULT_OK:
            raise RuntimeError(f"Failed to initialize EyeX: {ret}")

        # Create context
        self.context = c.c_voidp()
        ret = self.eyex_dll.txCreateContext(c.byref(self.context), tx.TX_FALSE)
        if ret != tx.TX_RESULT_OK:
            raise RuntimeError(f"Failed to create context: {ret}")

        # Initialize other variables
        self.latest_sample = None
        self.interactor_snapshot = c.c_voidp()
        self.interactor_id = "3425g"

        # Define callback handlers
        self._c_event_handler = tx.EVENT_HANDLER(self._event_handler)
        self._c_connection_handler = tx.CONNECTION_HANDLER(self._connection_handler)

        # Register handlers
        event_handler_ticket = c.c_int(0)
        connection_state_changed_ticket = c.c_int(0)

        ret = self.eyex_dll.txRegisterConnectionStateChangedHandler(self.context,
                                                                    c.byref(connection_state_changed_ticket),
                                                                    self._c_connection_handler, None)
        if ret != tx.TX_RESULT_OK:
            raise RuntimeError(f"Failed to register connection state handler: {ret}")

        ret = self.eyex_dll.txRegisterEventHandler(self.context, c.byref(event_handler_ticket), self._c_event_handler,
                                                   None)
        if ret != tx.TX_RESULT_OK:
            raise RuntimeError(f"Failed to register event handler: {ret}")

        # Enable connection
        ret = self.eyex_dll.txEnableConnection(self.context)
        if ret != tx.TX_RESULT_OK:
            raise RuntimeError(f"Failed to enable connection: {ret}")

        self._initialize_interactor_snapshot()

    def __del__(self):
        if hasattr(self, 'eyex_dll') and self.eyex_dll is not None:
            self.eyex_dll.txDisableConnection(self.context)
            self.eyex_dll.txShutdownContext(self.context, 500, tx.TX_FALSE)
            self.eyex_dll.txReleaseContext(c.byref(self.context))

    def _initialize_interactor_snapshot(self):
        interactor = c.c_voidp()
        params = tx.TX_GAZEPOINTDATAPARAMS(tx.TX_GAZEPOINTDATAMODE_LIGHTLYFILTERED)

        ret = self.eyex_dll.txCreateGlobalInteractorSnapshot(self.context, self.interactor_id.encode('utf-8'),
                                                             c.byref(self.interactor_snapshot), c.byref(interactor))
        if ret != tx.TX_RESULT_OK:
            raise RuntimeError(f"Failed to create global interactor snapshot: {ret}")

        ret = self.eyex_dll.txCreateGazePointDataBehavior(interactor, c.byref(params))
        if ret != tx.TX_RESULT_OK:
            raise RuntimeError(f"Failed to create gaze point data behavior: {ret}")

        ret = self.eyex_dll.txReleaseObject(c.byref(interactor))
        if ret != tx.TX_RESULT_OK:
            raise RuntimeError(f"Failed to release interactor object: {ret}")

    def _event_handler(self, async_data, user_param):
        event = c.c_voidp(None)
        behavior = c.c_voidp(None)

        # Get async data content
        ret = self.eyex_dll.txGetAsyncDataContent(async_data, c.byref(event))
        if ret != tx.TX_RESULT_OK:
            return

        if self.eyex_dll.txGetEventBehavior(event, c.byref(behavior), 1) == tx.TX_RESULT_OK:
            event_params = tx.TX_GAZEPOINTDATAEVENTPARAMS()
            if self.eyex_dll.txGetGazePointDataEventParams(behavior, c.byref(event_params)) == tx.TX_RESULT_OK:
                sample = Sample(int(event_params.GazePointDataMode),
                                float(event_params.timestamp),
                                float(event_params.x),
                                float(event_params.y))
                self.latest_sample = sample
                for callback in self.on_event:
                    callback(sample)
            self.eyex_dll.txReleaseObject(c.byref(behavior))

        self.eyex_dll.txReleaseObject(c.byref(event))

    def _connection_handler(self, connection_state, user_param):
        if connection_state == tx.TX_CONNECTIONSTATE.TX_CONNECTIONSTATE_CONNECTED:
            ret = self.eyex_dll.txCommitSnapshotAsync(self.interactor_snapshot, None, None)
            if ret != tx.TX_RESULT_OK:
                raise RuntimeError(f"Failed to commit snapshot: {ret}")

