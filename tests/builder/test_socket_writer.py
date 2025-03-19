import pytest
import socket
from unittest.mock import Mock, patch
from vpype_mecode.builder.writers import SocketWriter


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def mock_socket():
    with patch('socket.socket') as mock:
        socket_instance = Mock()
        mock.return_value = socket_instance
        yield socket_instance

@pytest.fixture
def socket_writer():
    return SocketWriter("localhost", 8000)


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

# Test initialization

def test_init_default_state():
    writer = SocketWriter("localhost", 8000)
    assert writer._host == "localhost"
    assert writer._port == 8000
    assert writer._wait_for_response is True
    assert writer._socket is None

def test_init_with_different_values():
    writer = SocketWriter("192.168.1.100", 9000, False)
    assert writer._wait_for_response is False
    assert writer._host == "192.168.1.100"
    assert writer._port == 9000

# Test connection

def test_connect_success(socket_writer, mock_socket):
    socket_writer.connect()
    mock_socket.connect.assert_called_once_with(("localhost", 8000))
    assert socket_writer._socket is not None

def test_connect_already_connected(socket_writer, mock_socket):
    socket_writer.connect()
    socket_writer.connect() # should not create new socket
    assert mock_socket.connect.call_count == 1

# Test auto-connection

def test_write_auto_connects(socket_writer, mock_socket):
    test_line = b"G1 X10 Y10\n"
    mock_socket.recv.return_value = b"%ok\n"
    assert socket_writer._socket is None
    socket_writer.write(b"G1 X10 Y10\n")
    mock_socket.connect.assert_called_once_with(("localhost", 8000))
    mock_socket.send.assert_called_once_with(test_line)
    socket_writer.disconnect()

# Test disconnection

def test_disconnect_when_connected(socket_writer, mock_socket):
    mock_socket.recv.return_value = b"%ok\n"
    socket_writer.connect()
    socket_writer.disconnect()
    mock_socket.close.assert_called_once()
    assert socket_writer._socket is None
    socket_writer.write(b"G1 X10 Y10\n") # Should auto-connect
    mock_socket.close.assert_called_once()

def test_disconnect_when_not_connected(socket_writer, mock_socket):
    socket_writer.disconnect()
    assert mock_socket.close.call_count == 0
    assert socket_writer._socket is None

def test_disconnect_with_wait_parameter(socket_writer, mock_socket):
    socket_writer.connect()
    socket_writer.disconnect(wait=False)
    mock_socket.close.assert_called_once()
    assert socket_writer._socket is None

# Test writing

def test_write_without_response(mock_socket):
    test_line = b"G1 X10 Y10\n"
    socket_writer = SocketWriter("localhost", 8000, False)
    socket_writer.connect()
    response = socket_writer.write(test_line)
    mock_socket.send.assert_called_once_with(test_line)
    assert response is None
    socket_writer.disconnect()

def test_write_with_response(mock_socket):
    test_line = b"G1 X10 Y10\n"
    mock_socket.recv.return_value = b"%ok\n"
    socket_writer = SocketWriter("localhost", 8000)
    socket_writer.connect()
    response = socket_writer.write(test_line)
    mock_socket.send.assert_called_once_with(test_line)
    mock_socket.recv.assert_called_once_with(8192)
    assert response == "ok"
    socket_writer.disconnect()

def test_write_multiple_statements(socket_writer, mock_socket):
    statements = [
        b"G1 X10 Y10\n",
        b"G1 X20 Y20\n",
        b"G1 X30 Y30\n"
    ]

    mock_socket.recv.return_value = b"%ok\n"
    socket_writer.connect()

    for statement in statements:
        socket_writer.write(statement)

    socket_writer.disconnect()

    assert mock_socket.send.call_count == 3
    assert mock_socket.recv.call_count == 3

# Test response handling

def test_response_parsing(socket_writer, mock_socket):
    test_cases = [
        (b"%simple\n", "simple"),
        (b"%with spaces\n", "with spaces"),
        (b"%special!@#$\n", "special!@#$"),
        (b"%empty\n", "empty"),
    ]

    for response_bytes, expected in test_cases:
        mock_socket.recv.return_value = response_bytes
        response = socket_writer.write(b"test\n")
        assert response == expected

# Test error handling

def test_connect_failure(socket_writer, mock_socket):
    mock_socket.connect.side_effect = socket.error()

    with pytest.raises(socket.error):
        socket_writer.connect()

def test_write_send_error(socket_writer, mock_socket):
    mock_socket.send.side_effect = socket.error()

    with pytest.raises(socket.error):
        socket_writer.write(b"G1 X10 Y10\n")

def test_write_receive_error(socket_writer, mock_socket):
    mock_socket.recv.side_effect = socket.error()

    with pytest.raises(socket.error):
        socket_writer.write(b"G1 X10 Y10\n")

def test_write_invalid_response(socket_writer, mock_socket):
    test_line = b"G1 X10 Y10\n"
    mock_socket.recv.return_value = b"invalid response\n"

    with pytest.raises(RuntimeError):
        socket_writer.write(test_line)
