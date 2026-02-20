from napalm import get_network_driver
from network_cicd.devices.napalm_base import NapalmDevice


class EOS(NapalmDevice):
    def __init__(self, hostname: str, username: str, password: str):
        if not hostname:
            raise ValueError("Hostname cannot be empty")
        if not username:
            raise ValueError("Username cannot be empty")
        if not password:
            raise ValueError("Password cannot be empty")

        driver_cls = get_network_driver("eos")
        driver = driver_cls(
            hostname=hostname.strip(),
            username=username.strip(),
            password=password.strip(),
        )
        driver.open()
        super().__init__(driver)
