from typing import TypedDict


class AFEntry(TypedDict):
    received_prefixes: int
    accepted_prefixes: int
    sent_prefixes: int


class AddressFamilyDict(TypedDict):
    ipv4: AFEntry
    ipv6: AFEntry


class BGPPeerDict(TypedDict):
    local_as: int
    remote_as: int
    remote_id: str
    is_up: bool
    is_enabled: bool
    description: str | None
    uptime: int
    address_family: AddressFamilyDict


class BGPGlobalDict(TypedDict):
    router_id: str
    peers: dict[str, BGPPeerDict]


# "global" is a reserved keyword in Python, so we use function style definition for TypedDict
BGPNeighborsDict = TypedDict(
    "BGPNeighborsDict",
    {
        "global": BGPGlobalDict,
    },
)
