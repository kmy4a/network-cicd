from network_cicd.devices.factory import create_device


def test_bgp_routes(fabric):
    """Test that BGP routes are correctly retrieved from each device"""
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
        expected_routes = (
            fabric.get("devices", {})
            .get(device_name, {})
            .get("bgp", {})
            .get("routes", [])
        )
        for route in expected_routes:
            bgp_routes = device.get_route_to(route)
            for route_info in bgp_routes.get(route, []):
                assert "bgp" in route_info.get("protocol", "").lower()
