import pytest
from network_cicd.devices.eos import EOS
from network_cicd.devices.napalm_base import NapalmDevice


def test_eos_initialization_success(mocker):
    """Test successful EOS device initialization"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_instance = mocker.Mock()
    mock_get_driver.return_value = mock_driver_cls
    mock_driver_cls.return_value = mock_driver_instance

    device = EOS(
        hostname="test-device",
        username="admin",
        password="admin123"
    )

    assert isinstance(device, NapalmDevice)
    mock_get_driver.assert_called_once_with("eos")


def test_eos_initialization_whitespace_stripping(mocker):
    """Test that EOS strips whitespace from credentials"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_instance = mocker.Mock()
    mock_get_driver.return_value = mock_driver_cls
    mock_driver_cls.return_value = mock_driver_instance

    EOS(
        hostname="  test-device  ",
        username="  admin  ",
        password="  admin123  "
    )

    mock_driver_cls.assert_called_once_with(
        hostname="test-device",
        username="admin",
        password="admin123"
    )


def test_eos_driver_open_called(mocker):
    """Test that driver.open() is called during initialization"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_instance = mocker.Mock()
    mock_get_driver.return_value = mock_driver_cls
    mock_driver_cls.return_value = mock_driver_instance

    EOS(hostname="192.168.1.1", username="user", password="pass")

    mock_driver_instance.open.assert_called_once()


def test_eos_constructor_call_order(mocker):
    """Test that driver is opened before super().__init__() is called"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_instance = mocker.Mock()
    mock_get_driver.return_value = mock_driver_cls
    mock_driver_cls.return_value = mock_driver_instance

    device = EOS(hostname="test", username="admin", password="pass")

    # Verify open was called
    mock_driver_instance.open.assert_called_once()
    # Verify device has the driver
    assert device._device == mock_driver_instance


def test_eos_all_credentials_passed_to_driver(mocker):
    """Test that all credentials are passed to driver constructor"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_instance = mocker.Mock()
    mock_get_driver.return_value = mock_driver_cls
    mock_driver_cls.return_value = mock_driver_instance

    hostname = "spine01.example.com"
    username = "netadmin"
    password = "P@ssw0rd!"

    EOS(hostname=hostname, username=username, password=password)

    mock_driver_cls.assert_called_once_with(
        hostname=hostname,
        username=username,
        password=password
    )


def test_eos_inheritance_from_napalm_device(mocker):
    """Test that EOS properly inherits from NapalmDevice"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_instance = mocker.Mock()
    mock_get_driver.return_value = mock_driver_cls
    mock_driver_cls.return_value = mock_driver_instance

    device = EOS(hostname="10.0.0.1", username="admin", password="secret")

    assert isinstance(device, NapalmDevice)
    assert hasattr(device, "_device")
    assert device._device == mock_driver_instance


def test_eos_empty_hostname_raises_value_error():
    """Test that empty hostname raises ValueError"""
    with pytest.raises(ValueError, match="Hostname cannot be empty"):
        EOS(hostname="", username="admin", password="pass")


def test_eos_whitespace_only_hostname_raises_value_error():
    """Test that whitespace-only hostname raises ValueError"""
    with pytest.raises(ValueError, match="Hostname cannot be empty"):
        EOS(hostname="   ", username="admin", password="pass")


def test_eos_empty_username_raises_value_error():
    """Test that empty username raises ValueError"""
    with pytest.raises(ValueError, match="Username cannot be empty"):
        EOS(hostname="test", username="", password="pass")


def test_eos_whitespace_only_username_raises_value_error():
    """Test that whitespace-only username raises ValueError"""
    with pytest.raises(ValueError, match="Username cannot be empty"):
        EOS(hostname="test", username="   ", password="pass")


def test_eos_empty_password_raises_value_error():
    """Test that empty password raises ValueError"""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        EOS(hostname="test", username="admin", password="")


def test_eos_whitespace_only_password_raises_value_error():
    """Test that whitespace-only password raises ValueError"""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        EOS(hostname="test", username="admin", password="   ")


def test_eos_get_network_driver_called_with_eos(mocker):
    """Test that get_network_driver is called with 'eos'"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_instance = mocker.Mock()
    mock_get_driver.return_value = mock_driver_cls
    mock_driver_cls.return_value = mock_driver_instance

    EOS(hostname="test", username="admin", password="pass")

    mock_get_driver.assert_called_once_with("eos")


def test_eos_driver_open_exception_propagates(mocker):
    """Test that driver.open() exceptions are propagated"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_instance = mocker.Mock()
    mock_driver_instance.open.side_effect = ConnectionError("Connection failed")
    mock_get_driver.return_value = mock_driver_cls
    mock_driver_cls.return_value = mock_driver_instance

    with pytest.raises(ConnectionError, match="Connection failed"):
        EOS(hostname="unreachable-host", username="admin", password="admin")


def test_eos_driver_instantiation_exception_propagates(mocker):
    """Test that driver instantiation exceptions are propagated"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_cls.side_effect = Exception("Invalid credentials")
    mock_get_driver.return_value = mock_driver_cls

    with pytest.raises(Exception, match="Invalid credentials"):
        EOS(hostname="test", username="admin", password="admin")


def test_eos_get_network_driver_exception_propagates(mocker):
    """Test that get_network_driver exceptions are propagated"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_get_driver.side_effect = Exception("Driver not found")

    with pytest.raises(Exception, match="Driver not found"):
        EOS(hostname="test", username="admin", password="admin")


def test_eos_with_special_characters_in_password(mocker):
    """Test EOS initialization with special characters in password"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_instance = mocker.Mock()
    mock_get_driver.return_value = mock_driver_cls
    mock_driver_cls.return_value = mock_driver_instance

    special_password = "P@$$w0rd!#%&*()[]{}±"
    EOS(hostname="test", username="admin", password=special_password)

    mock_driver_cls.assert_called_once_with(
        hostname="test",
        username="admin",
        password=special_password
    )


def test_eos_with_hostname_containing_dots(mocker):
    """Test EOS initialization with FQDN hostname"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_instance = mocker.Mock()
    mock_get_driver.return_value = mock_driver_cls
    mock_driver_cls.return_value = mock_driver_instance

    fqdn = "spine01.dc1.example.com"
    EOS(hostname=fqdn, username="admin", password="pass")

    mock_driver_cls.assert_called_once_with(
        hostname=fqdn,
        username="admin",
        password="pass"
    )


def test_eos_with_ip_address_hostname(mocker):
    """Test EOS initialization with IP address as hostname"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_instance = mocker.Mock()
    mock_get_driver.return_value = mock_driver_cls
    mock_driver_cls.return_value = mock_driver_instance

    ip_address = "192.168.1.100"
    EOS(hostname=ip_address, username="admin", password="pass")

    mock_driver_cls.assert_called_once_with(
        hostname=ip_address,
        username="admin",
        password="pass"
    )


def test_eos_validation_order_hostname_first(mocker):
    """Test that hostname is validated before calling get_network_driver"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    with pytest.raises(ValueError, match="Hostname cannot be empty"):
        EOS(hostname="", username="admin", password="pass")

    # get_network_driver should not have been called
    mock_get_driver.assert_not_called()


def test_eos_validation_order_username_second(mocker):
    """Test that username is validated before calling get_network_driver"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    with pytest.raises(ValueError, match="Username cannot be empty"):
        EOS(hostname="test", username="", password="pass")

    # get_network_driver should not have been called
    mock_get_driver.assert_not_called()


def test_eos_validation_order_password_third(mocker):
    """Test that password is validated before calling get_network_driver"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    with pytest.raises(ValueError, match="Password cannot be empty"):
        EOS(hostname="test", username="admin", password="")

    # get_network_driver should not have been called
    mock_get_driver.assert_not_called()


def test_eos_multiple_instances_independent(mocker):
    """Test that multiple EOS instances are independent"""
    mock_get_driver = mocker.patch("network_cicd.devices.eos.get_network_driver")
    mock_driver_cls = mocker.Mock()
    mock_driver_instance1 = mocker.Mock()
    mock_driver_instance2 = mocker.Mock()
    mock_get_driver.return_value = mock_driver_cls
    mock_driver_cls.side_effect = [mock_driver_instance1, mock_driver_instance2]

    device1 = EOS(hostname="device1", username="user1", password="pass1")
    device2 = EOS(hostname="device2", username="user2", password="pass2")

    assert device1._device == mock_driver_instance1
    assert device2._device == mock_driver_instance2
    assert device1._device is not device2._device
