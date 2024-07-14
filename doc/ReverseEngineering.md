# Reverse Engineering

This document describes how to do your own reverse engineering work on the Z407 remote and speaker.

## Tools

The Z407 uses Bluetooth Low Energy (BLE). While many phones and computers are able to communicate using BLE, most
devices don't support a sniffing mode that allows listening in on other devices' communication.

For this reason I used a Nordic Semiconductors
[nrF52840 Dongle](https://www.nordicsemi.com/Products/Development-hardware/nrf52840-dongle) for reverse engineering.
The dongle can be used with Wireshark and the nRF Sniffer Wireshark plugin to listen in on BLE communication between the
remote and the speaker. I followed the
[great tutorial by Stuart Patterson](https://www.youtube.com/watch?v=JIh2YYwkzoE).
You can also ready the
[nRF Sniffer Manual](https://infocenter.nordicsemi.com/index.jsp?topic=%2Fug_sniffer_ble%2FUG%2Fsniffer_ble%2Fintro.html)
by Nordic Semiconductors.