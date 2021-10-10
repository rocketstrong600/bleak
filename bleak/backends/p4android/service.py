from typing import List

from bleak.backends.service import BleakGATTService
from bleak.backends.p4android.characteristic import BleakGATTCharacteristicP4Android


class BleakGATTServiceP4Android(BleakGATTService):
    """GATT Service implementation for the python-for-android backend"""

    def __init__(self, java):
        super().__init__(java)
        self.__uuid = self.obj.getUuid().toString()
        self.__handle = self.obj.getInstanceId()
        self.__characteristics = []

    @property
    def uuid(self) -> str:
        """The UUID to this service"""
        return self.__uuid

    @property
<<<<<<< HEAD
    def handle(self) -> int:
        """A unique identifier for this service"""
        return self.__handle

    @property
=======
>>>>>>> origin/p4a
    def characteristics(self) -> List[BleakGATTCharacteristicP4Android]:
        """List of characteristics for this service"""
        return self.__characteristics

    def add_characteristic(self, characteristic: BleakGATTCharacteristicP4Android):
<<<<<<< HEAD
        """Add a :py:class:`~BleakGATTCharacteristicP4Android` to the service.
=======
        """Add a :py:class:`~BleakGATTCharacteristicBlueZDBus` to the service.
>>>>>>> origin/p4a

        Should not be used by end user, but rather by `bleak` itself.
        """
        self.__characteristics.append(characteristic)
