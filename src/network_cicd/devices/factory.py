from network_cicd.devices.eos import EOS
from network_cicd.devices.protocol import NetworkDevice


def create_device(
    os_type: str,
    hostname: str,
    username: str,
    password: str,
) -> NetworkDevice:
    if os_type == "eos":
        return EOS(hostname, username, password)

    raise ValueError(f"Unsupported OS: {os_type}")
