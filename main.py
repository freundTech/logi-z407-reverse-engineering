import asyncio
from datetime import datetime

from bleak import BleakScanner, BleakClient, BleakGATTCharacteristic

SERVICE_UUID = "0000fdc2-0000-1000-8000-00805f9b34fb"
COMMAND_UUID = "c2e758b9-0e78-41e0-b0cb-98a593193fc5"
RESPONSE_UUID = "b84ac9c6-29c5-46d4-bba1-9d534784330f"


class AsyncBleakScanner(BleakScanner):
    _device_queue: asyncio.Queue

    def __init__(self, **kwargs):
        super().__init__(self._device_found, **kwargs)
        self._device_queue = asyncio.Queue()

    async def _device_found(self, device, advertisement_data):
        await self._device_queue.put(device)

    async def async_discover(self, timeout=5):
        discovered_devices = set()
        await self.start()
        try:
            async with asyncio.timeout(timeout):
                while True:
                    device = await self._device_queue.get()
                    if device.address not in discovered_devices:
                        discovered_devices.add(device.address)
                        yield device
        except TimeoutError:
            pass
        await self.stop()


class Z407Remote:
    def __init__(self, address: str):
        self.address = address
        self.client = BleakClient(address)

    async def connect(self):
        await self.client.connect()

        await self.client.start_notify(RESPONSE_UUID, self._receive_data)
        await self._send_command("8405")

    async def disconnect(self):
        await self.client.disconnect()

    async def __aenter__(self):
        await self.connect()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def _receive_data(self, sender: BleakGATTCharacteristic, data: bytearray):
        print(bytes(data))
        match data:
            case b"\xd4\x05\x01":
                await self._send_command("8400")
            case b"\xd4\x00\x01":
                self.connected = True

    async def _send_command(self, command):
        await self.client.write_gatt_char(COMMAND_UUID, bytes.fromhex(command), response=False)

    async def volume_up(self):
        await self._send_command("8002")

    async def volume_down(self):
        await self._send_command("8003")

    async def play_pause(self):
        await self._send_command("8004")

    async def input_bluetooth(self):
        await self._send_command("8101")

    async def input_aux(self):
        await self._send_command("8102")

    async def input_usb(self):
        await self._send_command("8103")

    async def bluetooth_pair(self):
        await self._send_command("8200")

    async def factory_reset(self):
        await self._send_command("8300")

    @staticmethod
    async def _device_found(device, advertising_data):
        pass

    @staticmethod
    async def devices():
        scanner = AsyncBleakScanner(service_uuids=[SERVICE_UUID])
        async for device in scanner.async_discover():
            yield Z407Remote(device)


async def main():
    start = datetime.now()
    first_device = None
    while first_device is None:
        async for device in Z407Remote.devices():
            first_device = device
            break
    end = datetime.now()

    print("Took ", end - start)

    if first_device is None:
        print("No Z407 speaker found. Is your original remote still connected?")

    async with first_device:
        await first_device.play_pause()

asyncio.run(main())
