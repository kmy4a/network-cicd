from typing import cast

from napalm.base import NetworkDriver

from network_cicd.devices.protocol import NetworkDevice
from network_cicd.models.fact import DeviceFactsDict
from network_cicd.models.bgp import (
    AddressFamilyDict,
    AFEntry,
    BGPGlobalDict,
    BGPNeighborsDict,
    BGPPeerDict,
)
from network_cicd.models.interface import (
    InterfaceDict,
    InterfaceEntry,
    InterfaceIPDict,
    InterfaceIPEntry,
    IPEntry,
)
from network_cicd.models.route import RouteEntry, RoutesDict


class NapalmDevice(NetworkDevice):
    def __init__(self, driver: NetworkDriver) -> None:
        if not driver:
            raise TypeError("Driver cannot be None")
        self._device: NetworkDriver = driver

    def __enter__(self) -> "NapalmDevice":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._device.close()

    def get_facts(self) -> DeviceFactsDict:
        """Get basic facts about the device"""
        facts =  self._device.get_facts()
        return DeviceFactsDict(**facts)

    def get_interfaces(self) -> InterfaceDict:
        """Get interface information from the EOS device"""
        interfaces = self._device.get_interfaces()
        return {name: InterfaceEntry(**info) for name, info in interfaces.items()}

    def get_interfaces_ip(self) -> InterfaceIPDict:
        """Get interface IP information from the EOS device"""
        raw = self._device.get_interfaces_ip()

        # translate the raw data into our defined type-safe data models
        result: dict[str, InterfaceIPEntry] = {}
        for ifname, ifdata in raw.items():
            ipv4 = ifdata.get("ipv4", {})
            ipv6 = ifdata.get("ipv6", {})

            result[ifname] = InterfaceIPEntry(
                ipv4=cast(dict[str, IPEntry], ipv4),
                ipv6=cast(dict[str, IPEntry], ipv6),
            )

        return result

    def get_bgp_neighbors(self) -> BGPNeighborsDict:
        """Get BGP neighbor information from the EOS device"""
        raw = self._device.get_bgp_neighbors()

        # translate the raw data into our defined type-safe data models
        global_data = raw.get("global", {})
        peers_raw = global_data.get("peers", {})
        peers: dict[str, BGPPeerDict] = {}

        for peer_ip, peer in peers_raw.items():
            af_raw = peer.get("address_family", {})

            address_family: AddressFamilyDict = {
                "ipv4": cast(AFEntry, af_raw.get("ipv4", {})),
                "ipv6": cast(AFEntry, af_raw.get("ipv6", {})),
            }

            peers[peer_ip] = BGPPeerDict(
                local_as=peer["local_as"],
                remote_as=peer["remote_as"],
                remote_id=peer["remote_id"],
                is_up=peer["is_up"],
                is_enabled=peer["is_enabled"],
                description=peer.get("description"),
                uptime=peer["uptime"],
                address_family=address_family,
            )

        result: BGPNeighborsDict = {
            "global": BGPGlobalDict(
                router_id=global_data["router_id"],
                peers=peers,
            )
        }

        return result

    def get_route_to(self, destination: str) -> RoutesDict:
        """Get routing information for a specific destination from the EOS device"""
        formatted_destination: str = destination.strip()
        if not formatted_destination:
            raise ValueError("Destination cannot be empty")

        raw = self._device.get_route_to(destination=formatted_destination)

        # translate the raw data into our defined type-safe data models
        routes = cast(dict[str, list[dict]], raw)
        result: RoutesDict = {}
        for prefix, entries in routes.items():
            route_entries: list[RouteEntry] = []
            for entry in entries:
                route_entries.append(
                    RouteEntry(
                        current_active=entry.get("current_active", False),
                        last_active=entry.get("last_active", False),
                        age=entry.get("age", 0),
                        next_hop=entry.get("next_hop", ""),
                        protocol=entry.get("protocol", ""),
                        outgoing_interface=entry.get("outgoing_interface", ""),
                        preference=entry.get("preference", 0),
                        inactive_reason=entry.get("inactive_reason", ""),
                        routing_table=entry.get("routing_table", ""),
                        selected_next_hop=entry.get("selected_next_hop", False),
                        protocol_attributes=entry.get("protocol_attributes", {}),
                    )
                )
            result[prefix] = route_entries
        return result
