import pytest

from network_cicd.devices.factory import create_device
from network_cicd.devices.protocol import NetworkDevice


def test_create_device_eos_success(mocker):
    """Test successful device creation with EOS OS type"""
    mock_eos = mocker.patch("network_cicd.devices.factory.EOS")
    mock_instance = mocker.Mock(spec=NetworkDevice)
    mock_eos.return_value = mock_instance

    result = create_device("eos", "hostname", "user", "pass")

    assert result == mock_instance
    mock_eos.assert_called_once_with("hostname", "user", "pass")


def test_create_device_eos_uppercase(mocker):
    """Test that OS type is case-insensitive (uppercase)"""
    mock_eos = mocker.patch("network_cicd.devices.factory.EOS")
    mock_instance = mocker.Mock(spec=NetworkDevice)
    mock_eos.return_value = mock_instance

    create_device("EOS", "hostname", "user", "pass")

    mock_eos.assert_called_once_with("hostname", "user", "pass")


def test_create_device_eos_mixed_case(mocker):
    """Test that OS type is case-insensitive (mixed case)"""
    mock_eos = mocker.patch("network_cicd.devices.factory.EOS")
    mock_instance = mocker.Mock(spec=NetworkDevice)
    mock_eos.return_value = mock_instance

    create_device("EoS", "hostname", "user", "pass")

    mock_eos.assert_called_once_with("hostname", "user", "pass")


def test_create_device_os_type_whitespace_stripping(mocker):
    """Test that OS type whitespace is stripped"""
    mock_eos = mocker.patch("network_cicd.devices.factory.EOS")
    mock_instance = mocker.Mock(spec=NetworkDevice)
    mock_eos.return_value = mock_instance

    create_device("  eos  ", "hostname", "user", "pass")

    mock_eos.assert_called_once_with("hostname", "user", "pass")


def test_create_device_hostname_whitespace_stripping(mocker):
    """Test that hostname whitespace is stripped"""
    mock_eos = mocker.patch("network_cicd.devices.factory.EOS")
    mock_instance = mocker.Mock(spec=NetworkDevice)
    mock_eos.return_value = mock_instance

    create_device("eos", "  hostname  ", "user", "pass")

    mock_eos.assert_called_once_with("hostname", "user", "pass")


def test_create_device_username_whitespace_stripping(mocker):
    """Test that username whitespace is stripped"""
    mock_eos = mocker.patch("network_cicd.devices.factory.EOS")
    mock_instance = mocker.Mock(spec=NetworkDevice)
    mock_eos.return_value = mock_instance

    create_device("eos", "hostname", "  user  ", "pass")

    mock_eos.assert_called_once_with("hostname", "user", "pass")


def test_create_device_password_whitespace_stripping(mocker):
    """Test that password whitespace is stripped"""
    mock_eos = mocker.patch("network_cicd.devices.factory.EOS")
    mock_instance = mocker.Mock(spec=NetworkDevice)
    mock_eos.return_value = mock_instance

    create_device("eos", "hostname", "user", "  pass  ")

    mock_eos.assert_called_once_with("hostname", "user", "pass")


def test_create_device_empty_os_type_raises_value_error():
    """Test that empty OS type raises ValueError"""
    with pytest.raises(ValueError, match="OS type cannot be empty"):
        create_device("", "hostname", "user", "pass")


def test_create_device_empty_hostname_raises_value_error():
    """Test that empty hostname raises ValueError"""
    with pytest.raises(ValueError, match="Hostname cannot be empty"):
        create_device("eos", "", "user", "pass")


def test_create_device_empty_username_raises_value_error():
    """Test that empty username raises ValueError"""
    with pytest.raises(ValueError, match="Username cannot be empty"):
        create_device("eos", "hostname", "", "pass")


def test_create_device_empty_password_raises_value_error():
    """Test that empty password raises ValueError"""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        create_device("eos", "hostname", "user", "")


def test_create_device_whitespace_only_os_type_raises_value_error():
    """Test that whitespace-only OS type raises ValueError"""
    with pytest.raises(ValueError, match="OS type cannot be empty"):
        create_device("   ", "hostname", "user", "pass")


def test_create_device_whitespace_only_hostname_raises_value_error():
    """Test that whitespace-only hostname raises ValueError"""
    with pytest.raises(ValueError, match="Hostname cannot be empty"):
        create_device("eos", "   ", "user", "pass")


def test_create_device_whitespace_only_username_raises_value_error():
    """Test that whitespace-only username raises ValueError"""
    with pytest.raises(ValueError, match="Username cannot be empty"):
        create_device("eos", "hostname", "   ", "pass")


def test_create_device_whitespace_only_password_raises_value_error():
    """Test that whitespace-only password raises ValueError"""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        create_device("eos", "hostname", "user", "   ")


def test_create_device_unsupported_os_type_raises_value_error():
    """Test that unsupported OS type raises ValueError"""
    with pytest.raises(ValueError, match="Unsupported OS: xxx"):
        create_device("xxx", "hostname", "user", "pass")


def test_create_device_validation_order_os_type_first():
    """Test that OS type is validated first"""
    with pytest.raises(ValueError, match="OS type cannot be empty"):
        create_device("", "", "", "")


def test_create_device_validation_order_hostname_second():
    """Test that hostname is validated after OS type"""
    with pytest.raises(ValueError, match="Hostname cannot be empty"):
        create_device("eos", "", "user", "pass")


def test_create_device_validation_order_username_third():
    """Test that username is validated after hostname"""
    with pytest.raises(ValueError, match="Username cannot be empty"):
        create_device("eos", "hostname", "", "pass")


def test_create_device_validation_order_password_fourth():
    """Test that password is validated after username"""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        create_device("eos", "hostname", "user", "")


def test_create_device_eos_exception_propagates(mocker):
    """Test that exceptions from EOS constructor propagate"""
    mock_eos = mocker.patch("network_cicd.devices.factory.EOS")
    mock_eos.side_effect = Exception("Connection error")

    with pytest.raises(Exception, match="Connection error"):
        create_device("eos", "hostname", "user", "pass")


def test_create_device_with_special_characters_in_credentials(mocker):
    """Test device creation with special characters in credentials"""
    mock_eos = mocker.patch("network_cicd.devices.factory.EOS")
    mock_instance = mocker.Mock(spec=NetworkDevice)
    mock_eos.return_value = mock_instance

    special_pass = "p@ss!w0rd#$%^&*()"
    create_device("eos", "host-01", "admin@domain", special_pass)

    mock_eos.assert_called_once_with("host-01", "admin@domain", special_pass)


def test_create_device_with_fqdn_hostname(mocker):
    """Test device creation with FQDN hostname"""
    mock_eos = mocker.patch("network_cicd.devices.factory.EOS")
    mock_instance = mocker.Mock(spec=NetworkDevice)
    mock_eos.return_value = mock_instance

    create_device("eos", "spine01.example.com", "user", "pass")

    mock_eos.assert_called_once_with("spine01.example.com", "user", "pass")


def test_create_device_with_ip_address_hostname(mocker):
    """Test device creation with IP address as hostname"""
    mock_eos = mocker.patch("network_cicd.devices.factory.EOS")
    mock_instance = mocker.Mock(spec=NetworkDevice)
    mock_eos.return_value = mock_instance

    create_device("eos", "192.168.1.1", "user", "pass")

    mock_eos.assert_called_once_with("192.168.1.1", "user", "pass")


def test_create_device_unsupported_os_type_lowercase():
    """Test unsupported OS type in lowercase"""
    with pytest.raises(ValueError, match="Unsupported OS: yyy"):
        create_device("yyy", "hostname", "user", "pass")


def test_create_device_unsupported_os_type_uppercase():
    """Test unsupported OS type in uppercase"""
    with pytest.raises(ValueError, match="Unsupported OS: yyy"):
        create_device("YYY", "hostname", "user", "pass")


def test_create_device_unsupported_os_type_with_whitespace():
    """Test unsupported OS type with leading/trailing whitespace"""
    with pytest.raises(ValueError, match="Unsupported OS: zzz"):
        create_device("  zzz  ", "hostname", "user", "pass")
