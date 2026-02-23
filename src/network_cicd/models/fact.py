from typing import TypedDict


class DeviceFactsDict(TypedDict):
    hostname: str
    fqdn: str
    vendor: str
    model: str
    serial_number: str
    os_version: str
    uptime: float
    interface_list: list[str]
