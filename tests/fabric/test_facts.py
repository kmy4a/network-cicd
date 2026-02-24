from network_cicd.devices.factory import create_device


def test_hostname(fabric):
    """Test that the hostname fact is correctly retrieved from each device"""
    credentials = fabric.get("credentials", {})
    devices = fabric.get("devices", {})
    for device_name, device_info in devices.items():
        username = credentials.get(device_name, {}).get("username", "")
        password = credentials.get(device_name, {}).get("password", "")
        device = create_device(
            os_type="eos",
            hostname=f"clab-clos-testbed-{device_name}",
            username=username,
            password=password,
        )
        assert device.get_facts()["hostname"] == device_info.get("hostname", "")
