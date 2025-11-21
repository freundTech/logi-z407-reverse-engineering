# Protocol

The dial remote communicates with the speakers using Bluetooth Low Energy's (BLE) Generic Attribute Profile (GATT).
The speaker serves as the GATT server with the remote serving as a GATT client.

## Connection Establishment

When the speaker is not already connected to a remote it periodically sends out BLE advertisements.
The advertisements advertise a service with the UUID `0000fdc2-0000-1000-8000-00805f9b34fb`, which is the service
used to control the speaker.
When a remote is connected to the speaker it will not send advertisements and reject all connection attempts.
The original Logitech remote disconnects after about 5 minutes of no activity or when its batteries are removed.

Once the speaker has been discovered it can be connected to. Immediately after connecting it is necessary to write the 
hex value `0x8405` to the GATT characteristic `c2e758b9-0e78-41e0-b0cb-98a593193fc5` (command characteristic). 
The speaker will respond with `0xd40501` on GATT characteristic `b84ac9c6-29c5-46d4-bba1-9d534784330f` (response
characteristic).
After the response has been received one has to send `0x8400` to the command characteristic, which will cause the speaker
to reply with `0xd40001` on the response characteristic, followed by `0xd40003` to signal the connection is fully established.
After this the connection is established.
Failure to do so will cause the speaker to terminate the connection after a few seconds.

## Commands

After the connection has been established one can start sending commands to the command characteristic. The following
commands have been discovered:

### Audio Control

| Code     | Function     | Description                 |
|----------|--------------|-----------------------------|
| `0x8000` | Bass Up      | Increases the bass level    |
| `0x8001` | Bass Down    | Decreases the bass level    |
| `0x8002` | Volume Up    | Increases the master volume |
| `0x8003` | Volume Down  | Decreases the master volume |

### Playback Control

| Code     | Function      | Description                                      |
|----------|---------------|--------------------------------------------------|
| `0x8004` | Play/Pause    | Toggles play/pause for the Bluetooth source      |
| `0x8005` | Next Track    | Skips to the next track                          |
| `0x8006` | Previous Track| Goes to the previous track                       |

### Source Switching

| Code     | Function                    | Description                                |
|----------|-----------------------------|-------------------------------------------|
| `0x8101` | Switch to Bluetooth input   | Switches the active input to Bluetooth    |
| `0x8102` | Switch to AUX input         | Switches the active input to 3.5mm AUX    |
| `0x8103` | Switch to USB input         | Switches the active input to USB          |

### System Commands

| Code     | Function                 | Description                                    |
|----------|--------------------------|------------------------------------------------|
| `0x8200` | Enable Bluetooth pairing | Puts the speaker into Bluetooth pairing mode   |
| `0x8300` | Factory Reset            | Resets the speaker to factory defaults         |
| `0x8400` | Pairing Acknowledge      | Second step of connection handshake            |
| `0x8405` | Pairing Initiate         | First step of connection handshake             |

### Auditory Cues

| Code     | Function | Description                           |
|----------|----------|---------------------------------------|
| `0x8501` | Sound 1  | Plays failure/disconnect chime        |
| `0x8502` | Sound 2  | Plays mode switch chime               |
| `0x8503` | Sound 3  | Plays connection chime                |

### Unknown Commands

| Code     | Function   | Description              |
|----------|------------|--------------------------|
| `0x8500` | Unknown 1  | Has no noticeable effect |

## Response Codes

The speaker sends responses on the response characteristic (`b84ac9c6-29c5-46d4-bba1-9d534784330f`):

### Handshake Responses

| Code       | Function                | Description                                                  |
|------------|-------------------------|--------------------------------------------------------------|
| `0xd40501` | Initiate Response       | Sent in response to `0x8405` (INITIATE)                      |
| `0xd40001` | Acknowledge Response    | Sent in response to `0x8400` (ACKNOWLEDGE)                   |
| `0xd40003` | Connected               | Sent after `0xd40001` to signal connection is fully established |

### Command Confirmations

| Code       | Confirming Command |
|------------|--------------------|
| `0xc000`   | Bass Up            |
| `0xc001`   | Bass Down          |
| `0xc002`   | Volume Up          |
| `0xc003`   | Volume Down        |
| `0xc004`   | Play/Pause         |
| `0xc005`   | Next Track         |
| `0xc006`   | Previous Track     |
| `0xc101`   | Switch Bluetooth   |
| `0xc102`   | Switch AUX         |
| `0xc103`   | Switch USB         |
| `0xc200`   | Pairing            |
| `0xc300`   | Factory Reset      |
| `0xc501`   | Sound 3            |
| `0xc502`   | Sound 2            |
| `0xc503`   | Sound 1            |
| `0xc500`   | Unknown 1          |

### Status Updates

These are sent only if the source actually changes:

| Code       | Status                           |
|------------|----------------------------------|
| `0xcf04`   | Switched to Bluetooth (complete) |
| `0xcf05`   | Switched to AUX (complete)       |
| `0xcf06`   | Switched to USB (complete)       |
