"""Constants for the NgenicPy library."""

from typing import Final

API_URL: Final[str] = "https://app.ngenic.se/api/v3"

API_PATH: Final[dict[str, str]] = {
    "tunes": "tunes/{tune_uuid}",
    "rooms": "tunes/{tune_uuid}/rooms/{room_uuid}",
    "nodes": "tunes/{tune_uuid}/gateway/nodes/{node_uuid}",
    "node_status": "tunes/{tune_uuid}/nodestatus",
    "measurements": "tunes/{tune_uuid}/measurements/{node_uuid}",
    "measurements_types": "tunes/{tune_uuid}/measurements/{node_uuid}/types",
    "measurements_latest": "tunes/{tune_uuid}/measurements/{node_uuid}/latest",
    "setpoint_schedules": "tunes/{tune_uuid}/setpointschedules",
}
