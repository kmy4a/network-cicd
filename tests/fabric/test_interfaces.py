from network_cicd.devices.factory import create_device


def test_interfaces_state(fabric):
    """Test that all interfaces (except Management0) are up and enabled"""
    credentials = fabric.get("credentials", {})
    devices = fabric.get("devices", {})
    for device_name in devices.keys():
        username = credentials.get(device_name, {}).get("username", "")
        password = credentials.get(device_name, {}).get("password", "")
        device = create_device(
            os_type="eos",
            hostname=f"clab-clos-testbed-{device_name}",
            username=username,
            password=password,
        )
        interfaces = device.get_interfaces()
        for interface_name, interface_info in interfaces.items():
            if interface_name == "Management0":
                continue
            assert interface_name in fabric.get("devices", {}).get(device_name, {}).get(
                "interfaces", {}
            )
            assert interface_info.get("is_up", False)
            assert interface_info.get("is_enabled", False)


def test_interfaces_description(fabric):
    """Test that all interfaces have a description"""
    credentials = fabric.get("credentials", {})
    devices = fabric.get("devices", {})
    for device_name in devices.keys():
        username = credentials.get(device_name, {}).get("username", "")
        password = credentials.get(device_name, {}).get("password", "")
        device = create_device(
            os_type="eos",
            hostname=f"clab-clos-testbed-{device_name}",
            username=username,
            password=password,
        )
        interfaces = device.get_interfaces()
        for interface_name, interface_info in interfaces.items():
            assert interface_info.get("description") == fabric.get("devices", {}).get(
                device_name, {}
            ).get("interfaces", {}).get(interface_name, {}).get("description", "")


def test_interfaces_ip(fabric):
    """Test that all interfaces have IP information"""
    credentials = fabric.get("credentials", {})
    devices = fabric.get("devices", {})
    for device_name in devices.keys():
        username = credentials.get(device_name, {}).get("username", "")
        password = credentials.get(device_name, {}).get("password", "")
        device = create_device(
            os_type="eos",
            hostname=f"clab-clos-testbed-{device_name}",
            username=username,
            password=password,
        )
        interfaces_ip = device.get_interfaces_ip()
        for interface_name, ip_info in interfaces_ip.items():
            if interface_name == "Management0":
                continue
            ip_address = (
                str(list(ip_info.get("ipv4", {}).keys())[0])
                if ip_info.get("ipv4")
                else ""
            )
            subnet_mask = (
                ip_info.get("ipv4", {}).get(ip_address, {}).get("prefix_length", "")
            )
            assert interface_name in fabric.get("devices", {}).get(device_name, {}).get(
                "interfaces", {}
            )
            assert (
                ip_address
                == fabric.get("devices", {})
                .get(device_name, {})
                .get("interfaces", {})
                .get(interface_name, {})
                .get("ip_address", "")
                .split("/")[0]
            )
            assert subnet_mask == int(
                fabric.get("devices", {})
                .get(device_name, {})
                .get("interfaces", {})
                .get(interface_name, {})
                .get("ip_address", "")
                .split("/")[1]
            )
