import enum
import pytest
import vpype

from click import BadParameter, Context, Command
from click.core import ParameterSource
from vpype_cli import LengthType

from vpype_gscrib.config import ConfigOption


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

class SampleEnum(enum.Enum):
    OPTION1 = 'option1'
    OPTION2 = 'option2'


@pytest.fixture
def sample_context():
    return Context(command=Command(name='mock_command'))

@pytest.fixture
def basic_option():
    return ConfigOption('test_option', default='default_value')

@pytest.fixture
def length_option():
    px_value = vpype.convert_length('10mm')
    return ConfigOption('length_option', type=LengthType(), default=px_value)

@pytest.fixture
def enum_option():
    return ConfigOption('enum_option', type=SampleEnum, default=SampleEnum.OPTION1)


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

def test_basic_option_initialization(basic_option):
    assert basic_option.name == 'test_option'
    assert basic_option.opts == ['--test_option']

def test_enum_option_initialization(enum_option):
    assert 'Choices: option1, option2' in enum_option.help
    assert '[default: option1]' in enum_option.help

def test_length_option_initialization(length_option):
    px_value = vpype.convert_length('10mm')
    assert length_option.default == px_value
    assert '[default: 10.0mm]' in length_option.help

def test_override_default_value(basic_option):
    new_value = 'new_default'
    basic_option.override_default_value(new_value)
    assert basic_option.default == new_value
    assert '[default: new_default]' in basic_option.help

# Should pass if length units are provided
def test_length_type_with_units(sample_context, length_option):
    result = length_option._enforce_units(sample_context, length_option, '10mm')
    assert result == '10mm'

# Should raise BadParameter when length units are missing
def test_length_type_without_units(sample_context, length_option):
    source = ParameterSource.COMMANDLINE
    sample_context.set_parameter_source('length_option', source)

    with pytest.raises(BadParameter):
        length_option._enforce_units(sample_context, length_option, '10')

# Should allow default values without units (defaults to px)
def test_length_type_default_value(sample_context, length_option):
    source = ParameterSource.DEFAULT
    sample_context.set_parameter_source('length_option', source)
    result = length_option._enforce_units(sample_context, length_option, '10')
    assert result == '10'
