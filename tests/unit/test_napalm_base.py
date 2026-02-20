import pytest
from napalm.base import NetworkDriver
from network_cicd.devices.protocol import NetworkDevice
from network_cicd.devices.napalm_base import NapalmDevice, InterfaceIPEntry
from network_cicd.models.interface import InterfaceEntry


def test_napalm_device_init_with_valid_driver(mocker):
    """Test successful NapalmDevice initialization with valid driver"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    device = NapalmDevice(mock_driver)
    assert device._device == mock_driver


def test_napalm_device_init_with_none_driver_raises_type_error():
    """Test that None driver raises TypeError"""
    with pytest.raises(TypeError, match="Driver cannot be None"):
        NapalmDevice(None)  # type: ignore


def test_napalm_device_init_with_falsy_driver_raises_type_error():
    """Test that falsy driver raises TypeError"""
    with pytest.raises(TypeError, match="Driver cannot be None"):
        NapalmDevice(False)  # type: ignore


def test_napalm_device_context_manager_enter(mocker):
    """Test __enter__ returns self"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    device = NapalmDevice(mock_driver)
    result = device.__enter__()
    assert result is device


def test_napalm_device_context_manager_exit_calls_close(mocker):
    """Test __exit__ calls driver.close()"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    device = NapalmDevice(mock_driver)
    device.__exit__(None, None, None)
    mock_driver.close.assert_called_once()


def test_napalm_device_context_manager_exit_with_exception(mocker):
    """Test __exit__ calls driver.close() even with exception"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    device = NapalmDevice(mock_driver)
    device.__exit__(ValueError, ValueError("test"), None)
    mock_driver.close.assert_called_once()


def test_napalm_device_with_statement(mocker):
    """Test using NapalmDevice with context manager"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    with NapalmDevice(mock_driver) as device:
        assert isinstance(device, NapalmDevice)
    mock_driver.close.assert_called_once()


def test_napalm_device_get_interfaces_success(mocker):
    """Test get_interfaces returns transformed interface data"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_interfaces.return_value = {
        "Ethernet1": {
            "description": "Link to core",
            "enabled": True,
            "mtu": 1500,
            "speed": 1000.0,
            "is_up": True,
            "last_flapped": -1.0,
        }
    }

    device = NapalmDevice(mock_driver)
    result = device.get_interfaces()

    assert "Ethernet1" in result
    assert isinstance(result["Ethernet1"], InterfaceEntry)
    assert result["Ethernet1"].description == "Link to core"
    assert result["Ethernet1"].enabled is True
    assert result["Ethernet1"].mtu == 1500


def test_napalm_device_get_interfaces_empty(mocker):
    """Test get_interfaces with empty interface list"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_interfaces.return_value = {}

    device = NapalmDevice(mock_driver)
    result = device.get_interfaces()

    assert result == {}


def test_napalm_device_get_interfaces_multiple(mocker):
    """Test get_interfaces with multiple interfaces"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_interfaces.return_value = {
        "Ethernet1": {
            "description": "Link 1",
            "enabled": True,
            "mtu": 1500,
            "speed": 1000.0,
            "is_up": True,
            "last_flapped": -1.0,
        },
        "Ethernet2": {
            "description": "Link 2",
            "enabled": False,
            "mtu": 1500,
            "speed": 10000.0,
            "is_up": False,
            "last_flapped": 1234567890.0,
        },
    }

    device = NapalmDevice(mock_driver)
    result = device.get_interfaces()

    assert len(result) == 2
    assert "Ethernet1" in result
    assert "Ethernet2" in result


def test_napalm_device_get_interfaces_ip_success(mocker):
    """Test get_interfaces_ip returns transformed IP data"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_interfaces_ip.return_value = {
        "Ethernet1": {
            "ipv4": {"10.0.0.1": {"prefix_length": 24}},
            "ipv6": {"2001:db8::1": {"prefix_length": 64}},
        }
    }

    device = NapalmDevice(mock_driver)
    result = device.get_interfaces_ip()

    assert "Ethernet1" in result
    assert isinstance(result["Ethernet1"], InterfaceIPEntry)
    assert "10.0.0.1" in result["Ethernet1"].ipv4
    assert "2001:db8::1" in result["Ethernet1"].ipv6


def test_napalm_device_get_interfaces_ip_with_ipv4_only(mocker):
    """Test get_interfaces_ip with IPv4 only"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_interfaces_ip.return_value = {
        "Ethernet1": {"ipv4": {"192.168.1.1": {"prefix_length": 24}}, "ipv6": {}}
    }

    device = NapalmDevice(mock_driver)
    result = device.get_interfaces_ip()

    assert len(result["Ethernet1"].ipv4) == 1
    assert len(result["Ethernet1"].ipv6) == 0


def test_napalm_device_get_interfaces_ip_with_ipv6_only(mocker):
    """Test get_interfaces_ip with IPv6 only"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_interfaces_ip.return_value = {
        "Ethernet1": {"ipv4": {}, "ipv6": {"fe80::1": {"prefix_length": 10}}}
    }

    device = NapalmDevice(mock_driver)
    result = device.get_interfaces_ip()

    assert len(result["Ethernet1"].ipv4) == 0
    assert len(result["Ethernet1"].ipv6) == 1


def test_napalm_device_get_interfaces_ip_empty(mocker):
    """Test get_interfaces_ip with no interfaces"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_interfaces_ip.return_value = {}

    device = NapalmDevice(mock_driver)
    result = device.get_interfaces_ip()

    assert result == {}


def test_napalm_device_get_interfaces_ip_missing_keys(mocker):
    """Test get_interfaces_ip handles missing ipv4/ipv6 keys"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_interfaces_ip.return_value = {"Ethernet1": {}}

    device = NapalmDevice(mock_driver)
    result = device.get_interfaces_ip()

    assert "Ethernet1" in result
    assert result["Ethernet1"].ipv4 == {}
    assert result["Ethernet1"].ipv6 == {}


def test_napalm_device_get_bgp_neighbors_success(mocker):
    """Test get_bgp_neighbors returns transformed BGP data"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_bgp_neighbors.return_value = {
        "global": {
            "router_id": "10.0.0.1",
            "peers": {
                "10.0.0.2": {
                    "local_as": 65000,
                    "remote_as": 65001,
                    "remote_id": "10.0.0.2",
                    "is_up": True,
                    "is_enabled": True,
                    "description": "Peer1",
                    "uptime": 3600,
                    "address_family": {
                        "ipv4": {"received_prefixes": 100},
                        "ipv6": {"received_prefixes": 50},
                    },
                }
            },
        }
    }

    device = NapalmDevice(mock_driver)
    result = device.get_bgp_neighbors()

    assert "global" in result
    assert result["global"].router_id == "10.0.0.1"
    assert "10.0.0.2" in result["global"].peers
    assert result["global"].peers["10.0.0.2"].local_as == 65000


def test_napalm_device_get_bgp_neighbors_multiple_peers(mocker):
    """Test get_bgp_neighbors with multiple peers"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_bgp_neighbors.return_value = {
        "global": {
            "router_id": "10.0.0.1",
            "peers": {
                "10.0.0.2": {
                    "local_as": 65000,
                    "remote_as": 65001,
                    "remote_id": "10.0.0.2",
                    "is_up": True,
                    "is_enabled": True,
                    "description": "Peer1",
                    "uptime": 3600,
                    "address_family": {"ipv4": {}, "ipv6": {}},
                },
                "10.0.0.3": {
                    "local_as": 65000,
                    "remote_as": 65002,
                    "remote_id": "10.0.0.3",
                    "is_up": False,
                    "is_enabled": True,
                    "description": "Peer2",
                    "uptime": 0,
                    "address_family": {"ipv4": {}, "ipv6": {}},
                },
            },
        }
    }

    device = NapalmDevice(mock_driver)
    result = device.get_bgp_neighbors()

    assert len(result["global"].peers) == 2
    assert result["global"].peers["10.0.0.2"].is_up is True
    assert result["global"].peers["10.0.0.3"].is_up is False


def test_napalm_device_get_bgp_neighbors_no_description(mocker):
    """Test get_bgp_neighbors with peer missing description"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_bgp_neighbors.return_value = {
        "global": {
            "router_id": "10.0.0.1",
            "peers": {
                "10.0.0.2": {
                    "local_as": 65000,
                    "remote_as": 65001,
                    "remote_id": "10.0.0.2",
                    "is_up": True,
                    "is_enabled": True,
                    "uptime": 3600,
                    "address_family": {"ipv4": {}, "ipv6": {}},
                }
            },
        }
    }

    device = NapalmDevice(mock_driver)
    result = device.get_bgp_neighbors()

    assert result["global"].peers["10.0.0.2"].description is None


def test_napalm_device_get_bgp_neighbors_empty_peers(mocker):
    """Test get_bgp_neighbors with no peers"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_bgp_neighbors.return_value = {
        "global": {"router_id": "10.0.0.1", "peers": {}}
    }

    device = NapalmDevice(mock_driver)
    result = device.get_bgp_neighbors()

    assert len(result["global"].peers) == 0


def test_napalm_device_get_bgp_neighbors_missing_address_family(mocker):
    """Test get_bgp_neighbors handles missing address_family"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_bgp_neighbors.return_value = {
        "global": {
            "router_id": "10.0.0.1",
            "peers": {
                "10.0.0.2": {
                    "local_as": 65000,
                    "remote_as": 65001,
                    "remote_id": "10.0.0.2",
                    "is_up": True,
                    "is_enabled": True,
                    "description": "Peer1",
                    "uptime": 3600,
                    "address_family": {},
                }
            },
        }
    }

    device = NapalmDevice(mock_driver)
    result = device.get_bgp_neighbors()

    af = result["global"].peers["10.0.0.2"].address_family
    assert af["ipv4"] == {}
    assert af["ipv6"] == {}


def test_napalm_device_get_route_to_success(mocker):
    """Test get_route_to returns transformed route data"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_route_to.return_value = {
        "10.0.0.0/24": [
            {
                "current_active": True,
                "last_active": False,
                "age": 3600,
                "next_hop": "10.1.1.1",
                "protocol": "bgp",
                "outgoing_interface": "Ethernet1",
                "preference": 20,
                "inactive_reason": "",
                "routing_table": "main",
                "selected_next_hop": True,
                "protocol_attributes": {},
            }
        ]
    }

    device = NapalmDevice(mock_driver)
    result = device.get_route_to("10.0.0.0/24")

    assert "10.0.0.0/24" in result
    assert len(result["10.0.0.0/24"]) == 1
    assert result["10.0.0.0/24"][0].next_hop == "10.1.1.1"
    mock_driver.get_route_to.assert_called_once_with(destination="10.0.0.0/24")


def test_napalm_device_get_route_to_whitespace_stripping(mocker):
    """Test get_route_to strips destination whitespace"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_route_to.return_value = {}

    device = NapalmDevice(mock_driver)
    device.get_route_to("  10.0.0.0/24  ")

    mock_driver.get_route_to.assert_called_once_with(destination="10.0.0.0/24")


def test_napalm_device_get_route_to_empty_destination_raises_value_error(mocker):
    """Test get_route_to with empty destination raises ValueError"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    device = NapalmDevice(mock_driver)

    with pytest.raises(ValueError, match="Destination cannot be empty"):
        device.get_route_to("")


def test_napalm_device_get_route_to_whitespace_only_destination_raises_value_error(
    mocker,
):
    """Test get_route_to with whitespace-only destination raises ValueError"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    device = NapalmDevice(mock_driver)

    with pytest.raises(ValueError, match="Destination cannot be empty"):
        device.get_route_to("   ")


def test_napalm_device_get_route_to_multiple_routes(mocker):
    """Test get_route_to with multiple routes for same prefix"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_route_to.return_value = {
        "10.0.0.0/24": [
            {
                "current_active": True,
                "last_active": False,
                "age": 3600,
                "next_hop": "10.1.1.1",
                "protocol": "bgp",
                "outgoing_interface": "Ethernet1",
                "preference": 20,
                "inactive_reason": "",
                "routing_table": "main",
                "selected_next_hop": True,
                "protocol_attributes": {},
            },
            {
                "current_active": False,
                "last_active": True,
                "age": 1800,
                "next_hop": "10.1.1.2",
                "protocol": "bgp",
                "outgoing_interface": "Ethernet2",
                "preference": 20,
                "inactive_reason": "higher_preference",
                "routing_table": "main",
                "selected_next_hop": False,
                "protocol_attributes": {},
            },
        ]
    }

    device = NapalmDevice(mock_driver)
    result = device.get_route_to("10.0.0.0/24")

    assert len(result["10.0.0.0/24"]) == 2
    assert result["10.0.0.0/24"][0].current_active is True
    assert result["10.0.0.0/24"][1].current_active is False


def test_napalm_device_get_route_to_no_routes(mocker):
    """Test get_route_to when no routes found"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_route_to.return_value = {}

    device = NapalmDevice(mock_driver)
    result = device.get_route_to("10.0.0.0/24")

    assert result == {}


def test_napalm_device_get_route_to_missing_optional_fields(mocker):
    """Test get_route_to with missing optional route fields"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_route_to.return_value = {
        "10.0.0.0/24": [
            {
                "local_as": 65000,
                "remote_as": 65001,
            }
        ]
    }

    device = NapalmDevice(mock_driver)
    result = device.get_route_to("10.0.0.0/24")

    route = result["10.0.0.0/24"][0]
    assert route.current_active is False
    assert route.age == 0
    assert route.next_hop == ""


def test_napalm_device_get_route_to_with_protocol_attributes(mocker):
    """Test get_route_to includes protocol attributes"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    mock_driver.get_route_to.return_value = {
        "10.0.0.0/24": [
            {
                "current_active": True,
                "last_active": False,
                "age": 3600,
                "next_hop": "10.1.1.1",
                "protocol": "bgp",
                "outgoing_interface": "Ethernet1",
                "preference": 20,
                "inactive_reason": "",
                "routing_table": "main",
                "selected_next_hop": True,
                "protocol_attributes": {"as_path": "65001"},
            }
        ]
    }

    device = NapalmDevice(mock_driver)
    result = device.get_route_to("10.0.0.0/24")

    assert result["10.0.0.0/24"][0].protocol_attributes == {"as_path": "65001"}


def test_napalm_device_is_network_device(mocker):
    """Test that NapalmDevice is a NetworkDevice"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    device = NapalmDevice(mock_driver)
    assert isinstance(device, NetworkDevice)


def test_napalm_device_driver_storage(mocker):
    """Test that driver is properly stored"""
    mock_driver = mocker.Mock(spec=NetworkDriver)
    device = NapalmDevice(mock_driver)
    assert device._device is mock_driver
