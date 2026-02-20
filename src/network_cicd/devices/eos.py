from napalm import get_network_driver
from network_cicd.devices.napalm_base import NapalmDevice


class EOS(NapalmDevice):
    def __init__(self, hostname: str, username: str, password: str):
        formatted_hostname = hostname.strip()
        formatted_username = username.strip()
        formatted_password = password.strip()
        if not formatted_hostname:
            raise ValueError("Hostname cannot be empty")
        if not formatted_username:
            raise ValueError("Username cannot be empty")
        if not formatted_password:
            raise ValueError("Password cannot be empty")

        driver_cls = get_network_driver("eos")
        driver = driver_cls(
            hostname=formatted_hostname,
            username=formatted_username,
            password=formatted_password,
        )
        driver.open()
        super().__init__(driver)
