<<<<<<< HEAD
=======
#!/usr/bin/env python3

>>>>>>> origin/p4a
from kivy.app import App

# from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

# bind bleak's python logger into kivy's logger before importing python module using logging
from kivy.logger import Logger
import logging

logging.Logger.manager.root = Logger

import asyncio
import bleak


class ExampleApp(App):
    def __init__(self):
        super().__init__()
        self.label = None
        self.running = True

    def build(self):
        self.scrollview = ScrollView(do_scroll_x=False, scroll_type=["bars", "content"])
        self.label = Label(font_size="10sp")
        self.scrollview.add_widget(self.label)
        return self.scrollview

    def line(self, text, empty=False):
        Logger.info("example:" + text)
        if self.label is None:
            return
        text += "\n"
        if empty:
            self.label.text = text
        else:
            self.label.text += text

    def on_stop(self):
        self.running = False

    async def example(self):
        while self.running:
            try:
                self.line("scanning")
                scanned_devices = await bleak.BleakScanner.discover(1)
                self.line("scanned", True)

                if len(scanned_devices) == 0:
                    raise bleak.exc.BleakError("no devices found")

                scanned_devices.sort(key=lambda device: -device.rssi)

                for device in scanned_devices:
<<<<<<< HEAD
                    self.line(f"{device.name} {device.rssi}dB")

                for device in scanned_devices:
                    self.line(f"Connecting to {device.name} ...")
                    try:
                        async with bleak.BleakClient(device) as client:
                            services = await client.get_services()
                            for service in services.services.values():
                                self.line(f"  service {service.uuid}")
                                for characteristic in service.characteristics:
                                    self.line(
                                        f"  characteristic {characteristic.uuid} {hex(characteristic.handle)} ({len(characteristic.descriptors)} descriptors)"
                                    )
                    except bleak.exc.BleakError as e:
                        self.line(f"  error {e}")
                        asyncio.sleep(10)
            except bleak.exc.BleakError as e:
                self.line(f"ERROR {e}")
=======
                    self.line("{0} {1}dB".format(str(device)[:24], device.rssi))

                for device in scanned_devices:
                    self.line("Connecting to {0} ...".format(str(device)[:24]))
                    client = bleak.BleakClient(device.address)
                    try:
                        await client.connect()
                        services = await client.get_services()
                        for service in services.services.values():
                            self.line("  service {0}".format(service.uuid))
                            for characteristic in service.characteristics:
                                self.line(
                                    "  characteristic {0} {1} ({2} descriptors)".format(
                                        characteristic.uuid,
                                        hex(characteristic.handle),
                                        len(characteristic.descriptors),
                                    )
                                )
                    except bleak.exc.BleakError as e:
                        self.line("  error {0}".format(e))
                    finally:
                        await client.disconnect()
            except bleak.exc.BleakError as e:
                self.line("ERROR {0}".format(e))
>>>>>>> origin/p4a
                await asyncio.sleep(1)
        self.line("example loop terminated", True)


<<<<<<< HEAD
async def main(app):
    await asyncio.gather(app.async_run("asyncio"), app.example())


=======
>>>>>>> origin/p4a
if __name__ == "__main__":
    Logger.setLevel(logging.DEBUG)

    # app running on one thread with two async coroutines
    app = ExampleApp()
<<<<<<< HEAD
    asyncio.run(main(app))
=======
    loop = asyncio.get_event_loop()
    coroutines = (app.async_run("asyncio"), app.example())
    firstcompleted = asyncio.wait(coroutines, return_when=asyncio.FIRST_COMPLETED)
    results, ongoing = loop.run_until_complete(firstcompleted)
    for result in results:
        result.result()  # raises exceptions from asyncio.wait
>>>>>>> origin/p4a
