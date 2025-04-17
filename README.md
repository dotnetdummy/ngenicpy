# Ngenic Tune Python API Wrapper

This python package simplifies access to the Ngenic Tune API.
It can be used for viewing or edit your Tune configuration.

Both sync and async APIs are provided - async APIs are prefixed with `async_`.

**NOTE**: This API wrapper is not yet finished, and only implements a subset of all the APIs. The interface may very well change.

## Prerequisite

### Obtain an API token

An API token may be obtained here: https://developer.ngenic.se/

## Installation

```
$ pip install ngenicpy
```

## Example

```python
import json

from ngenicpy import Ngenic

# try/finally
try:
    ngenic = Ngenic(token="YOUR-API-TOKEN")
except NgenicException as e:
        print(str(e))
finally:
    ngenic.close()

# as context manager
with Ngenic(token="YOUR-API-TOKEN") as ngenic:
    tunes = ngenic.tunes()
    for tune in tunes:
        print("Tune %s\nName: %s\nTune Name: %s" %
                (
                    tune.uuid(),
                    tune["name"],
                    tune["tuneName"]
                )
        )

    tune = ngenic.tune("TUNE-UUID")

    rooms = tune.rooms()
    for room in rooms:
        print("Room %s\nName: %s\nTarget Temperature: %d" %
                (
                    room.uuid(),
                    room["name"],
                    room["targetTemperature"]
                )
        )

    # Update a room
    room = tune.room(room_uuid="ROOM-UUID")
    room["name"] = "Livingroom"
    room.update()

    nodes = tune.nodes()
    for node in nodes:
        node_status = node.status()

        print("Node %s\nType: %s" %
                (
                    node.uuid(),
                    node.get_type()
                )
        )

        if node_status:
            print("Battery: %s\nRadio Signal: %s" %
                    (
                        str(node_status.battery_percentage()),
                        str(node_status.radio_signal_percentage())
                    )
            )

        measurements = node.measurements()
        for measurement in measurements:
            print("%s: %d" %
                    (
                        measurement.get_type(),
                        measurement["value"]
                    )
            )
```

Async example

```python
import json

from ngenicpy import Ngenic

async with AsyncNgenic(token="YOUR-API-TOKEN") as ngenic:
    tunes = await ngenic.async_tunes()
    for tune in tunes:
        print("Tune %s\nName: %s\nTune Name: %s" %
                (
                    tune.uuid(),
                    tune["name"],
                    tune["tuneName"]
                )
        )
```

## Reference

[Ngenic Tune Public API](https://developer.ngenic.se/)
