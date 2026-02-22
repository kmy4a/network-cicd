import pytest

from network_cicd.devices.eos import EOS
from network_cicd.devices.napalm_base import NapalmDevice


def test_eos_initialization_success(mocker):
    """Test successful EOS initialization with valid credentials"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver = mocker.Mock()
    mock_get_driver.return_value.return_value = mock_driver

    eos = EOS("hostname", "user", "pass")

    assert isinstance(eos, EOS)
    assert isinstance(eos, NapalmDevice)
    mock_driver.open.assert_called_once()


def test_eos_initialization_whitespace_stripping(mocker):
    """Test that whitespace is stripped from all parameters"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver = mocker.Mock()
    mock_driver_cls.return_value = mock_driver
    mock_get_driver.return_value = mock_driver_cls

    EOS("  hostname  ", "  user  ", "  pass  ")

    mock_driver_cls.assert_called_once_with(
        hostname="hostname",
        username="user",
        password="pass",
    )


def test_eos_empty_hostname_raises_value_error():
    """Test that empty hostname raises ValueError"""
    with pytest.raises(ValueError, match="Hostname cannot be empty"):
        EOS("", "user", "pass")


def test_eos_empty_username_raises_value_error():
    """Test that empty username raises ValueError"""
    with pytest.raises(ValueError, match="Username cannot be empty"):
        EOS("hostname", "", "pass")


def test_eos_empty_password_raises_value_error():
    """Test that empty password raises ValueError"""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        EOS("hostname", "user", "")


def test_eos_whitespace_only_hostname_raises_value_error():
    """Test that whitespace-only hostname raises ValueError"""
    with pytest.raises(ValueError, match="Hostname cannot be empty"):
        EOS("   ", "user", "pass")


def test_eos_whitespace_only_username_raises_value_error():
    """Test that whitespace-only username raises ValueError"""
    with pytest.raises(ValueError, match="Username cannot be empty"):
        EOS("hostname", "   ", "pass")


def test_eos_whitespace_only_password_raises_value_error():
    """Test that whitespace-only password raises ValueError"""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        EOS("hostname", "user", "   ")


def test_eos_get_network_driver_called_with_eos(mocker):
    """Test that get_network_driver is called with 'eos'"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver = mocker.Mock()
    mock_driver_cls.return_value = mock_driver
    mock_get_driver.return_value = mock_driver_cls

    EOS("hostname", "user", "pass")

    mock_get_driver.assert_called_once_with("eos")


def test_eos_driver_open_called(mocker):
    """Test that driver.open() is called during initialization"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver = mocker.Mock()
    mock_driver_cls = mocker.Mock(return_value=mock_driver)
    mock_get_driver.return_value = mock_driver_cls

    EOS("hostname", "user", "pass")

    mock_driver.open.assert_called_once()


def test_eos_all_credentials_passed_to_driver(mocker):
    """Test that all credentials are passed to driver constructor"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver = mocker.Mock()
    mock_driver_cls.return_value = mock_driver
    mock_get_driver.return_value = mock_driver_cls

    EOS("test-host", "admin", "secret123")

    mock_driver_cls.assert_called_once_with(
        hostname="test-host",
        username="admin",
        password="secret123",
    )


def test_eos_inheritance_from_napalm_device(mocker):
    """Test that EOS properly inherits from NapalmDevice"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver = mocker.Mock()
    mock_driver_cls = mocker.Mock(return_value=mock_driver)
    mock_get_driver.return_value = mock_driver_cls

    eos = EOS("hostname", "user", "pass")

    assert isinstance(eos, NapalmDevice)


def test_eos_constructor_call_order(mocker):
    """Test that get_network_driver is called before driver instantiation"""
    call_order = []

    def track_get_driver(os_type):
        call_order.append("get_driver")
        mock_driver_cls = mocker.Mock(
            side_effect=lambda **kwargs: (
                call_order.append("driver_init") or mocker.Mock()
            )
        )
        return mock_driver_cls

    with mocker.patch(
        "network_cicd.devices.eos.get_network_driver", side_effect=track_get_driver
    ):
        EOS("hostname", "user", "pass")
        assert call_order[0] == "get_driver"
        assert call_order[1] == "driver_init"


def test_eos_get_network_driver_exception_propagates(mocker):
    """Test that exceptions from get_network_driver propagate"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_get_driver.side_effect = Exception("Driver not found")

    with pytest.raises(Exception, match="Driver not found"):
        EOS("hostname", "user", "pass")


def test_eos_driver_instantiation_exception_propagates(mocker):
    """Test that exceptions from driver instantiation propagate"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock(side_effect=Exception("Connection failed"))
    mock_get_driver.return_value = mock_driver_cls

    with pytest.raises(Exception, match="Connection failed"):
        EOS("hostname", "user", "pass")


def test_eos_driver_open_exception_propagates(mocker):
    """Test that exceptions from driver.open() propagate"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver = mocker.Mock()
    mock_driver.open.side_effect = Exception("Open failed")
    mock_driver_cls = mocker.Mock(return_value=mock_driver)
    mock_get_driver.return_value = mock_driver_cls

    with pytest.raises(Exception, match="Open failed"):
        EOS("hostname", "user", "pass")


def test_eos_validation_order_hostname_first():
    """Test that hostname is validated before username"""
    with pytest.raises(ValueError, match="Hostname cannot be empty"):
        EOS("", "", "")


def test_eos_validation_order_username_second():
    """Test that username is validated after hostname"""
    with pytest.raises(ValueError, match="Username cannot be empty"):
        EOS("hostname", "", "pass")


def test_eos_validation_order_password_third():
    """Test that password is validated after username"""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        EOS("hostname", "user", "")


def test_eos_with_special_characters_in_password(mocker):
    """Test initialization with special characters in password"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver = mocker.Mock()
    mock_driver_cls.return_value = mock_driver
    mock_get_driver.return_value = mock_driver_cls

    special_pass = "p@ss!w0rd#$%^&*()"
    EOS("hostname", "user", special_pass)

    mock_driver_cls.assert_called_once_with(
        hostname="hostname",
        username="user",
        password=special_pass,
    )


def test_eos_with_hostname_containing_dots(mocker):
    """Test initialization with FQDN hostname"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver = mocker.Mock()
    mock_driver_cls.return_value = mock_driver
    mock_get_driver.return_value = mock_driver_cls

    EOS("spine01.example.com", "user", "pass")

    mock_driver_cls.assert_called_once_with(
        hostname="spine01.example.com",
        username="user",
        password="pass",
    )


def test_eos_with_ip_address_hostname(mocker):
    """Test initialization with IP address as hostname"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver = mocker.Mock()
    mock_driver_cls.return_value = mock_driver
    mock_get_driver.return_value = mock_driver_cls

    EOS("192.168.1.1", "user", "pass")

    mock_driver_cls.assert_called_once_with(
        hostname="192.168.1.1",
        username="user",
        password="pass",
    )


def test_eos_multiple_instances_independent(mocker):
    """Test that multiple EOS instances are independent"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver1 = mocker.Mock()
    mock_driver2 = mocker.Mock()
    mock_driver_cls = mocker.Mock(side_effect=[mock_driver1, mock_driver2])
    mock_get_driver.return_value = mock_driver_cls

    EOS("host1", "user1", "pass1")
    EOS("host2", "user2", "pass2")

    assert mock_driver1.open.called
    assert mock_driver2.open.called
    assert mock_driver1 is not mock_driver2
