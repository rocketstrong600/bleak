# -*- coding: utf-8 -*-

import asyncio
import logging
from typing import List
import warnings

from bleak.backends.scanner import BaseBleakScanner, AdvertisementData
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError

from android.broadcast import BroadcastReceiver
<<<<<<< HEAD
from android.permissions import request_permissions, Permission
=======
from android.permissions import request_permissions
>>>>>>> origin/p4a
from jnius import cast, java_method

from . import defs
from . import utils

logger = logging.getLogger(__name__)


class BleakScannerP4Android(BaseBleakScanner):

    __scanner = None

    """The python-for-android Bleak BLE Scanner.

    Keyword Args:
<<<<<<< HEAD
=======
        adapter (str): Bluetooth adapter to use for discovery. [ignored]
>>>>>>> origin/p4a
        filters (dict): A dict of filters to be applied on discovery. [unimplemented]

    """

    def __init__(self, **kwargs):
        super(BleakScannerP4Android, self).__init__(**kwargs)

<<<<<<< HEAD
=======
        # kwarg "device" is for backwards compatibility
        self.__adapter = kwargs.get("adapter", kwargs.get("device", None))

>>>>>>> origin/p4a
        self._devices = {}
        self.__javascanner = None
        self.__callback = None

        # Discovery filters
        self._filters = kwargs.get("filters", {})

    def __del__(self):
        self.__stop()

    async def start(self):
        if BleakScannerP4Android.__scanner is not None:
            raise BleakError("A BleakScanner is already scanning on this adapter.")

        logger.debug("Starting BTLE scan")

        loop = asyncio.get_event_loop()

        if self.__javascanner is None:
            if self.__callback is None:
                self.__callback = _PythonScanCallback(self, loop)

            permission_acknowledged = loop.create_future()

            def handle_permissions(permissions, grantResults):
                if any(grantResults):
                    loop.call_soon_threadsafe(
                        permission_acknowledged.set_result, grantResults
                    )
                else:
                    loop.call_soon_threadsafe(
                        permission_acknowledged.set_exception(
                            BleakError("User denied access to " + str(permissions))
                        )
                    )

            request_permissions(
                [
<<<<<<< HEAD
                    Permission.ACCESS_FINE_LOCATION,
                    Permission.ACCESS_COARSE_LOCATION,
=======
                    defs.ACCESS_FINE_LOCATION,
                    defs.ACCESS_COARSE_LOCATION,
                    defs.ACCESS_BACKGROUND_LOCATION,
>>>>>>> origin/p4a
                ],
                handle_permissions,
            )
            await permission_acknowledged

            self.__adapter = defs.BluetoothAdapter.getDefaultAdapter()
            if self.__adapter is None:
                raise BleakError("Bluetooth is not supported on this hardware platform")
<<<<<<< HEAD
            if self.__adapter.getState() != defs.BluetoothAdapter.STATE_ON:
=======
            if self.__adapter.getState() != defs.STATE_ON:
>>>>>>> origin/p4a
                raise BleakError("Bluetooth is not turned on")

            self.__javascanner = self.__adapter.getBluetoothLeScanner()

        BleakScannerP4Android.__scanner = self

        filters = cast("java.util.List", defs.List())
        # filters could be built with defs.ScanFilterBuilder

        scanfuture = self.__callback.perform_and_wait(
            dispatchApi=self.__javascanner.startScan,
            dispatchParams=(
                filters,
                defs.ScanSettingsBuilder()
                .setScanMode(defs.ScanSettings.SCAN_MODE_LOW_LATENCY)
                .setReportDelay(0)
                .setPhy(defs.ScanSettings.PHY_LE_ALL_SUPPORTED)
                .setNumOfMatches(defs.ScanSettings.MATCH_NUM_MAX_ADVERTISEMENT)
                .setMatchMode(defs.ScanSettings.MATCH_MODE_AGGRESSIVE)
                .setCallbackType(defs.ScanSettings.CALLBACK_TYPE_ALL_MATCHES)
                .build(),
                self.__callback.java,
            ),
            resultApi="onScan",
            return_indicates_status=False,
        )
        self.__javascanner.flushPendingScanResults(self.__callback.java)

        try:
            await asyncio.wait_for(scanfuture, timeout=0.2)
        except asyncio.exceptions.TimeoutError:
            pass
        except BleakError as bleakerror:
            await self.stop()
            if bleakerror.args != (
                "onScan",
                "SCAN_FAILED_APPLICATION_REGISTRATION_FAILED",
            ):
                raise bleakerror
            else:
                # there might be a clearer solution to this if android source and vendor
                # documentation are reviewed for the meaning of the error
                # https://stackoverflow.com/questions/27516399/solution-for-ble-scans-scan-failed-application-registration-failed
                warnings.warn(
                    "BT API gave SCAN_FAILED_APPLICATION_REGISTRATION_FAILED.  Resetting adapter."
                )

                def handlerWaitingForState(state, stateFuture):
                    def handleAdapterStateChanged(context, intent):
                        adapter_state = intent.getIntExtra(
<<<<<<< HEAD
                            defs.BluetoothAdapter.EXTRA_STATE,
                            defs.BluetoothAdapter.STATE_ERROR,
                        )
                        if adapter_state == defs.BluetoothAdapter.STATE_ERROR:
                            loop.call_soon_threadsafe(
                                stateOffFuture.set_exception,
                                BleakError(f"Unexpected adapter state {adapter_state}"),
=======
                            defs.EXTRA_STATE, defs.STATE_ERROR
                        )
                        if adapter_state == defs.STATE_ERROR:
                            loop.call_soon_threadsafe(
                                stateOffFuture.set_exception,
                                BleakError(
                                    "Unexpected adapter state {}".format(adapter_state)
                                ),
>>>>>>> origin/p4a
                            )
                        elif adapter_state == state:
                            loop.call_soon_threadsafe(
                                stateFuture.set_result, adapter_state
                            )

                    return handleAdapterStateChanged

                logger.info(
                    "disabling bluetooth adapter to handle SCAN_FAILED_APPLICATION_REGSTRATION_FAILED ..."
                )
                stateOffFuture = loop.create_future()
                receiver = BroadcastReceiver(
<<<<<<< HEAD
                    handlerWaitingForState(
                        defs.BluetoothAdapter.STATE_OFF, stateOffFuture
                    ),
                    actions=[defs.BluetoothAdapter.ACTION_STATE_CHANGED],
=======
                    handlerWaitingForState(defs.STATE_OFF, stateOffFuture),
                    actions=[defs.ACTION_STATE_CHANGED],
>>>>>>> origin/p4a
                )
                receiver.start()
                try:
                    self.__adapter.disable()
                    await stateOffFuture
                finally:
                    receiver.stop()

                logger.info("re-enabling bluetooth adapter ...")
                stateOnFuture = loop.create_future()
                receiver = BroadcastReceiver(
<<<<<<< HEAD
                    handlerWaitingForState(
                        defs.BluetoothAdapter.STATE_ON, stateOnFuture
                    ),
                    actions=[defs.BluetoothAdapter.ACTION_STATE_CHANGED],
=======
                    handlerWaitingForState(defs.STATE_ON, stateOnFuture),
                    actions=[defs.ACTION_STATE_CHANGED],
>>>>>>> origin/p4a
                )
                receiver.start()
                try:
                    self.__adapter.enable()
                    await stateOnFuture
                finally:
                    receiver.stop()
                logger.debug("restarting scan ...")

                return await self.start()

    def __stop(self):
        if self.__javascanner is not None:
            logger.debug("Stopping BTLE scan")
            self.__javascanner.stopScan(self.__callback.java)
            BleakScannerP4Android.__scanner = None
            self.__javascanner = None
        else:
            logger.debug("BTLE scan already stopped")

    async def stop(self):
        self.__stop()

    async def set_scanning_filter(self, **kwargs):
        self._filters = kwargs.get("filters", {})

<<<<<<< HEAD
    @property
    def discovered_devices(self) -> List[BLEDevice]:
=======
    async def get_discovered_devices(self) -> List[BLEDevice]:
>>>>>>> origin/p4a
        return [*self._devices.values()]


class _PythonScanCallback(utils.AsyncJavaCallbacks):
    __javainterfaces__ = ["com.github.hbldh.bleak.PythonScanCallback$Interface"]

    def __init__(self, scanner, loop):
        super().__init__(loop)
        self._scanner = scanner
        self.java = defs.PythonScanCallback(self)

    def result_state(self, status_str, name, *data):
        self._loop.call_soon_threadsafe(
            self._result_state_unthreadsafe, status_str, name, data
        )

    @java_method("(I)V")
    def onScanFailed(self, errorCode):
        self.result_state(defs.SCAN_FAILED_NAMES[errorCode], "onScan")

    @java_method("(Landroid/bluetooth/le/ScanResult;)V")
    def onScanResult(self, result):
        device = result.getDevice()
        record = result.getScanRecord()
        service_uuids = record.getServiceUuids()
        if service_uuids is not None:
            service_uuids = [
<<<<<<< HEAD
                service_uuid.getUuid().toString() for service_uuid in service_uuids
=======
                service_uuids[index].getUuid().toString()
                for index in range(len(service_uuids))
>>>>>>> origin/p4a
            ]
        manufacturer_data = record.getManufacturerSpecificData()
        manufacturer_data = {
            manufacturer_data.keyAt(index): bytearray(
                manufacturer_data.valueAt(index).tolist()
            )
            for index in range(manufacturer_data.size())
        }
        service_data_iterator = record.getServiceData().entrySet().iterator()
        service_data = {}
        while service_data_iterator.hasNext():
            entry = service_data_iterator.next()
            service_data[entry.getKey().toString()] = bytearray(
                entry.getValue().tolist()
            )
        advertisement = AdvertisementData(
            local_name=record.getDeviceName(),
            manufacturer_data=manufacturer_data,
            service_data=service_data,
            service_uuids=service_uuids,
            platform_data=(result,),
        )
        device = BLEDevice(
            device.getAddress(),
            device.getName(),
            rssi=result.getRssi(),
            uuids=service_uuids,
            manufacturer_data=manufacturer_data,
        )
        self._scanner._devices[device.address] = device
        if "onScan" not in self.states:
            self.result_state(None, "onScan", device)
        if self._scanner._callback:
            self._loop.call_soon_threadsafe(
                self._scanner._callback, device, advertisement
            )
