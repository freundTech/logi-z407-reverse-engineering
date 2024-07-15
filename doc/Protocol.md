# Protocol

The dial remote communicates with the speakers using Bluetooth Low Energy's (BLE) Generic Attribute Profile (GATT).
The speaker serves as the GATT server with the remote serving as a GATT client.

## Connection Establishment

When the speaker is not already connected to a remote it periodically sends out BLE advertisements.
The advertisements advertice a service with the UUID `0000fdc2-0000-1000-8000-00805f9b34fb`, which is the service
used to control the speaker.
When a remote is connected to the speaker it will not send advertisements and reject all connection attempts.
The original Logitech remote disconnects after about 5 minutes of no activity or when its batteries are removed.

Once the speaker has been discovered it can be connected to. Immediately after connecting it is necessary to write the 
hex value `0x8405` to the GATT characteristic `c2e758b9-0e78-41e0-b0cb-98a593193fc5` (command characteristic). 
The speaker will respond with `0xd40501` on GATT characteristic `b84ac9c6-29c5-46d4-bba1-9d534784330f` (response
characteristic).
After the response has been received one has to send `0x8400` to the command characteristic, which will cause the speaker
to reply with `0xd40001` on the response characteristic.
After this the connection is established.
Failure to do so will cause the speaker to terminate the connection after a few seconds.

## Taking control

After the connection has been established one can start sending commands to the command characteristic. The following
commands have been discovered:

| Code     | Function                           | Comment                                |
|----------|------------------------------------|----------------------------------------|
| `0x8002` | Volume Up                          |                                        |
| `0x8003` | Volume Down                        |                                        |
| `0x8004` | Play/Pause                         |                                        |
| `0x8101` | Switch to Bluetooth input          |                                        |
| `0x8102` | Switch to AUX input                |                                        |
| `0x8103` | Switch to USB input                |                                        |
| `0x8200` | Enable Bluetooth pairing           |                                        |
| `0x8300` | Reset                              | Responds with `0xc300`                 |
| `0x8400` | Pairing Part 2                     | See "Connection Establishment" section |
| `0x8405` | Pairing Part 1                     | See "Connection Establishment" section |
| `0x8502` | Switch to base/volume control mode | Hold                                   |



