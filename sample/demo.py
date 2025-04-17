"""This is a sample script to show how to use the Ngenic API."""

import os

from ngenicpy import Ngenic
from ngenicpy.models.measurement import Measurement
from ngenicpy.models.node import Node
from ngenicpy.models.node_status import NodeStatus
from ngenicpy.models.tune import Tune


def main():
    """Main function to demonstrate the Ngenic API usage."""
    token = os.environ["NGENIC_TOKEN"]

    if not token:
        print("Set NGENIC_TOKEN as a environment var")
        exit(1)

    with Ngenic(token=token) as ngenic:
        tunes: list[Tune] = ngenic.tunes()
        for tune in tunes:
            print(
                f"Tune {tune.uuid()}, Name: {tune['name']}, Tune Name: {tune['tuneName']}"
            )

            nodes: list[Node] = tune.nodes()
            for node in nodes:
                node_status: NodeStatus = node.status()

                print(f"\tNode {node.uuid()}, Type: {node.get_type()}")

                if node_status:
                    print(
                        f"\t\tBattery: {node_status.battery_percentage()}\n\t\tRadio Signal: {node_status.radio_signal_percentage()}"
                    )

                measurements: Measurement = node.measurements()
                if len(measurements) == 0:
                    print("\t\t(no measurements)")

                for measurement in measurements:
                    print(f"\t\t{measurement.get_type()}: {measurement.json()}")


if __name__ == "__main__":
    main()
