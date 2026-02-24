from network_cicd.devices.factory import create_device


def test_bgp_neighbors(fabric):
    """Test that BGP neighbors are correctly retrieved from each device"""
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
        bgp_neighbors = device.get_bgp_neighbors()
        expected_neighbors = (
            fabric.get("devices", {})
            .get(device_name, {})
            .get("bgp", {})
            .get("neighbors", {})
        )

        assert set(bgp_neighbors.get("global", {}).get("peers", {}).keys()) == set(
            expected_neighbors.keys()
        )
        for neighbor_ip, neighbor_info in (
            bgp_neighbors.get("global", {}).get("peers", {}).items()
        ):
            assert neighbor_info.get("description") == expected_neighbors[
                neighbor_ip
            ].get("description", "")


def test_bgp_neighbor_state(fabric):
    """Test that BGP neighbor states are correctly retrieved from each device"""
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
        bgp_neighbors = device.get_bgp_neighbors()
        for neighbor_info in bgp_neighbors.get("global", {}).get("peers", {}).values():
            assert neighbor_info.get("is_up", False)
            assert neighbor_info.get("is_enabled", False)


def test_bgp_neighbor_asn(fabric):
    """Test that BGP neighbor ASNs are correctly retrieved from each device"""
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
        bgp_neighbors = device.get_bgp_neighbors()
        expected_neighbors = (
            fabric.get("devices", {})
            .get(device_name, {})
            .get("bgp", {})
            .get("neighbors", {})
        )
        for neighbor_ip, neighbor_info in (
            bgp_neighbors.get("global", {}).get("peers", {}).items()
        ):
            assert neighbor_info.get("remote_as") == expected_neighbors[
                neighbor_ip
            ].get("remote_as")
