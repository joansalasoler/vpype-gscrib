import pytest
from vpype_mecode.builder.writers import SerialWriter
from vpype_mecode.builder.writers import PrintrunWriter


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

# Test initialization

def test_init_default_state():
    writer = SerialWriter("/dev/ttyUSB0", 115200)
    assert isinstance(writer._writer_delegate, PrintrunWriter)
