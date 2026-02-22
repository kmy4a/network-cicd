from typing import Dict, TypedDict


###### Interface models ######
class InterfaceEntry(TypedDict):
    is_up: bool
    is_enabled: bool
    description: str | None
    last_flapped: float | None
    mtu: int
    speed: float | None
    mac_address: str | None


# interface_name -> InterfaceEntry
InterfaceDict = Dict[str, InterfaceEntry]


###### Interface IP models ######
class IPEntry(TypedDict):
    prefix_length: int


class InterfaceIPEntry(TypedDict):
    ipv4: Dict[str, IPEntry]
    ipv6: Dict[str, IPEntry]


# interface_name -> InterfaceIPEntry
InterfaceIPDict = Dict[str, InterfaceIPEntry]
