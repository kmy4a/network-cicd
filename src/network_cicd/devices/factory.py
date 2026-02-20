from network_cicd.devices.eos import EOS
from network_cicd.devices.protocol import NetworkDevice


def create_device(
    os_type: str,
    hostname: str,
    username: str,
    password: str,
) -> NetworkDevice:
    formatted_os_type: str = os_type.strip().lower()
    formatted_hostname: str = hostname.strip()
    formatted_username: str = username.strip()
    formatted_password: str = password.strip()

    if not formatted_os_type:
        raise ValueError("OS type cannot be empty")
    if not formatted_hostname:
        raise ValueError("Hostname cannot be empty")
    if not formatted_username:
        raise ValueError("Username cannot be empty")
    if not formatted_password:
        raise ValueError("Password cannot be empty")

    if formatted_os_type == "eos":
        return EOS(formatted_hostname, formatted_username, formatted_password)

    raise ValueError(f"Unsupported OS: {formatted_os_type}")
