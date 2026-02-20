from napalm import get_network_driver
from network_cicd.devices.napalm_base import NapalmDevice


class EOS(NapalmDevice):
    def __init__(self, hostname: str, username: str, password: str):
        driver_cls = get_network_driver("eos")
        driver = driver_cls(
            hostname=hostname,
            username=username,
            password=password,
        )
        driver.open()
        super().__init__(driver)
