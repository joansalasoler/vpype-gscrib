import pytest
from unittest.mock import Mock, patch
from serial.serialutil import SerialException
from vpype_mecode.builder.writers import SerialWriter
from vpype_mecode.builder.devices import Printer


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def mock_printer():
    with patch('vpype_mecode.builder.writers.serial_writer.Printer') as mock:
        printer_instance = Mock()
        mock.return_value = printer_instance
        yield printer_instance

@pytest.fixture
def serial_writer():
    return SerialWriter("/dev/ttyUSB0", 115200)


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

# Test initialization

def test_init_default_state():
    writer = SerialWriter("/dev/ttyUSB0", 115200)
    assert writer._port == "/dev/ttyUSB0"
    assert writer._baudrate == 115200
    assert writer._printer is None

# Test connection

def test_connect_success(mock_printer, serial_writer):
    serial_writer.connect()
    mock_printer.connect.assert_called_once()
    mock_printer.start.assert_called_once()
    assert serial_writer._printer is not None

def test_connect_already_connected(mock_printer, serial_writer):
    serial_writer.connect()
    serial_writer.connect() # Should not create new printer
    mock_printer.connect.assert_called_once()
    mock_printer.start.assert_called_once()

# Test auto-connection

def test_auto_connect_on_write(mock_printer, serial_writer):
    test_command = b"G1 X10 Y10\n"
    serial_writer.write(test_command)
    mock_printer.connect.assert_called_once()
    mock_printer.start.assert_called_once()
    mock_printer.sendline.assert_called_once_with("G1 X10 Y10\n")
    serial_writer.disconnect()

# Test disconnection

def test_disconnect_when_connected(mock_printer, serial_writer):
    serial_writer.connect()
    serial_writer.disconnect()
    mock_printer.disconnect.assert_called_once_with(True)
    assert serial_writer._printer is None

def test_disconnect_when_not_connected(serial_writer):
    serial_writer.disconnect()
    assert serial_writer._printer is None

def test_disconnect_with_wait_false(mock_printer, serial_writer):
    serial_writer.connect()
    serial_writer.disconnect(wait=False)
    mock_printer.disconnect.assert_called_once_with(False)
    assert serial_writer._printer is None

# Test writing

def test_write_without_response(mock_printer, serial_writer):
    test_command = b"G1 X10 Y10\n"
    serial_writer.write(test_command)
    mock_printer.sendline.assert_called_once_with("G1 X10 Y10\n")
    mock_printer.get_response.assert_not_called()

def test_write_with_response(mock_printer, serial_writer):
    test_command = b"M114\n"
    mock_printer.get_response.return_value = "ok X:10 Y:20 Z:0"
    response = serial_writer.write(test_command, requires_response=True)
    mock_printer.get_response.assert_called_once_with("M114\n")
    assert response == "ok X:10 Y:20 Z:0"

def test_write_multiple_statements(mock_printer, serial_writer):
    statements = [
        b"G1 X10 Y10\n",
        b"G1 X20 Y20\n",
        b"G1 X30 Y30\n"
    ]

    for statement in statements:
        serial_writer.write(statement)

    assert mock_printer.sendline.call_count == 3
    mock_printer.sendline.assert_any_call("G1 X10 Y10\n")
    mock_printer.sendline.assert_any_call("G1 X20 Y20\n")
    mock_printer.sendline.assert_any_call("G1 X30 Y30\n")

def test_mixed_response_writes(mock_printer, serial_writer):
    mock_printer.get_response.return_value = "ok"
    serial_writer.write(b"G1 X10 Y10\n")
    serial_writer.write(b"M114\n", requires_response=True)
    serial_writer.write(b"G1 X20 Y20\n")
    assert mock_printer.sendline.call_count == 2
    assert mock_printer.get_response.call_count == 1

# Test error handling

def test_write_connection_error(mock_printer, serial_writer):
    mock_printer.connect.side_effect = SerialException()

    with pytest.raises(SerialException):
        serial_writer.write(b"G1 X10 Y10\n")

def test_write_send_error(mock_printer, serial_writer):
    mock_printer.sendline.side_effect = SerialException()

    with pytest.raises(SerialException):
        serial_writer.write(b"G1 X10 Y10\n")

def test_write_response_error(mock_printer, serial_writer):
    mock_printer.get_response.side_effect = SerialException()

    with pytest.raises(SerialException):
        serial_writer.write(b"M114\n", requires_response=True)
