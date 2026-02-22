from typing import Any, TypedDict


class RouteEntry(TypedDict):
    current_active: bool
    last_active: bool
    age: int
    next_hop: str
    protocol: str
    outgoing_interface: str
    preference: int
    inactive_reason: str
    routing_table: str
    selected_next_hop: bool
    protocol_attributes: dict[str, Any]


class RoutesDict(TypedDict):
    pass
