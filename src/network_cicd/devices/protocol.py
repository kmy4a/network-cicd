from typing import Protocol, runtime_checkable

from network_cicd.models.bgp import BGPNeighborsDict
from network_cicd.models.fact import DeviceFactsDict
from network_cicd.models.interface import InterfaceDict, InterfaceIPDict
from network_cicd.models.route import RoutesDict


@runtime_checkable
class NetworkDevice(Protocol):
    """Protocol for all network devices"""

    def get_facts(self) -> DeviceFactsDict: ...

    def get_interfaces(self) -> InterfaceDict: ...

    def get_interfaces_ip(self) -> InterfaceIPDict: ...

    def get_bgp_neighbors(self) -> BGPNeighborsDict: ...

    def get_route_to(self, destination: str) -> RoutesDict: ...
