from typing import Protocol

from network_cicd.models.bgp import BGPNeighborsDict
from network_cicd.models.interface import InterfaceDict, InterfaceIPDict
from network_cicd.models.route import RoutesDict


class NetworkDevice(Protocol):
    """Protocol for all network devices"""
    def get_interfaces(self) -> InterfaceDict:
        ...

    def get_interfaces_ip(self) -> InterfaceIPDict:
        ...

    def get_bgp_neighbors(self) -> BGPNeighborsDict:
        ...

    def get_route_to(self, destination: str) -> RoutesDict:
        ...
