import os

from ngenicpy import Ngenic
from ngenicpy.models.measurement import Measurement
from ngenicpy.models.node import Node
from ngenicpy.models.node_status import NodeStatus
from ngenicpy.models.tune import Tune

def main():
    token = os.environ['NGENIC_TOKEN']
    
    if not token:
        print("Set NGENIC_TOKEN as a environment var")
        exit(1)

    with Ngenic(token=token) as ngenic:
        tunes: list[Tune] = ngenic.tunes()
        for tune in tunes:
            print("Tune %s, Name: %s, Tune Name: %s" %
                    (
                        tune.uuid(),
                        tune["name"],
                        tune["tuneName"]
                    )
            )

            nodes: list[Node] = tune.nodes()
            for node in nodes:
                node_status: NodeStatus = node.status()

                print("\tNode %s, Type: %s" %
                        (
                            node.uuid(),
                            node.get_type()
                        )
                )

                if node_status:
                    print("\t\tBattery: %s\n\t\tRadio Signal: %s" %
                            (
                                str(node_status.battery_percentage()),
                                str(node_status.radio_signal_percentage())
                            )
                    )

                measurements: Measurement = node.measurements()
                if len(measurements) == 0:
                    print("\t\t(no measurements)")

                for measurement in measurements:
                    print("\t\t%s: %s" %
                            (
                                measurement.get_type(),
                                measurement.json()
                            )
                    )



if __name__ == "__main__":
    main()