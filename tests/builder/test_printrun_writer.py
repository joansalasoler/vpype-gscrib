import pytest
from unittest.mock import Mock, patch
from serial.serialutil import SerialException
from vpype_mecode.builder.enums import DirectWrite
from vpype_mecode.builder.excepts import DeviceConnectionError
from vpype_mecode.builder.writers import PrintrunWriter


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def mock_printcore():
    with patch('vpype_mecode.builder.printrun.printcore') as mock:
        printer_instance = Mock()
        mock.return_value = printer_instance
        yield mock

@pytest.fixture
def serial_writer(mock_printcore):
    return create_writer(
        mock_printcore,
        mode=DirectWrite.SERIAL,
        host="none",
        port="/dev/ttyUSB0",
        baudrate=115200
    )

@pytest.fixture
def scoket_writer(mock_printcore):
    return create_writer(
        mock_printcore,
        mode=DirectWrite.SOCKET,
        host="testhost",
        port="8888",
        baudrate=0
    )

def create_writer(mock_printcore, mode, host, port, baudrate):
    writer = PrintrunWriter(mode, host, port, baudrate)
    writer._create_device = Mock(return_value=mock_printcore)
    writer._wait_for = Mock(return_value=True)
    writer._on_response_received = Mock()
    return writer


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

# Test initialization

def test_init_serial_writer(serial_writer):
    assert serial_writer._mode == DirectWrite.SERIAL
    assert serial_writer._port == "/dev/ttyUSB0"
    assert serial_writer._baudrate == 115200
    assert serial_writer._device is None

def test_init_socket_writer(scoket_writer):
    assert scoket_writer._mode == DirectWrite.SOCKET
    assert scoket_writer._host == "testhost"
    assert scoket_writer._port == "8888"
    assert scoket_writer._device is None

# Test connection

def test_connect_success(serial_writer):
    serial_writer.connect()
    assert serial_writer._device is not None

def test_connect_already_connected(serial_writer):
    serial_writer.connect()
    original_device = serial_writer._device
    serial_writer.connect() # Should not create new device
    assert serial_writer._device == original_device

# Test auto-connection

def test_auto_connect_on_write(serial_writer):
    test_command = b"G1 X10 Y10\n"
    serial_writer.write(test_command)
    assert serial_writer._device is not None
    serial_writer._device.send.assert_called_once_with("G1 X10 Y10")
    serial_writer.disconnect()

# Test disconnection

def test_disconnect_when_connected(serial_writer):
    serial_writer.connect()
    serial_writer.disconnect()
    assert serial_writer._device is None

def test_disconnect_when_not_connected(serial_writer):
    serial_writer.disconnect()
    assert serial_writer._device is None

def test_disconnect_with_wait_false(serial_writer):
    serial_writer.connect()
    serial_writer.disconnect(wait=False)
    assert serial_writer._device is None

# Test writing

def test_write_without_response(serial_writer):
    test_command = b"G1 X10 Y10\n"
    serial_writer.write(test_command)
    serial_writer._device.send.assert_called_once_with("G1 X10 Y10")
    serial_writer._on_response_received.assert_not_called()

def test_write_with_response(serial_writer):
    test_command = b"M114\n"
    test_response = "ok X:10 Y:20 Z:0"
    serial_writer.connect()
    recvcb = lambda c: serial_writer._device.recvcb(test_response)
    serial_writer._device.send = Mock(side_effect=recvcb)
    response = serial_writer.write(test_command, wait=True)
    serial_writer._device.send.assert_called_once_with("M114")
    serial_writer._on_response_received.assert_called_once_with(test_response)
    assert response == "ok X:10 Y:20 Z:0"

def test_write_multiple_statements(serial_writer):
    statements = [
        b"G1 X10 Y10\n",
        b"G1 X20 Y20\n",
        b"G1 X30 Y30\n"
    ]

    for statement in statements:
        serial_writer.write(statement)

    assert serial_writer._device.send.call_count == 3
    serial_writer._device.send.assert_any_call("G1 X10 Y10")
    serial_writer._device.send.assert_any_call("G1 X20 Y20")
    serial_writer._device.send.assert_any_call("G1 X30 Y30")

def test_mixed_response_writes(serial_writer):
    def receive_callback(command):
        if serial_writer._device.recvcb is not None:
            serial_writer._device.recvcb("ok")

    serial_writer.connect()
    serial_writer._device.send = Mock(side_effect=receive_callback)
    serial_writer.write(b"G1 X10 Y10\n")
    serial_writer.write(b"M114\n", wait=True)
    serial_writer.write(b"G1 X20 Y20\n")
    assert serial_writer._device.send.call_count == 3
    assert serial_writer._on_response_received.call_count == 1

# Test error handling

def test_write_connection_error(serial_writer):
    serial_writer.connect()
    serial_writer._device.send.side_effect = DeviceConnectionError()

    with pytest.raises(DeviceConnectionError):
        serial_writer.write(b"G1 X10 Y10\n")

def test_write_send_error(serial_writer):
    serial_writer.connect()
    serial_writer._device.send.side_effect = SerialException()

    with pytest.raises(SerialException):
        serial_writer.write(b"G1 X10 Y10\n")
