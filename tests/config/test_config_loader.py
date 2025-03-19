import pytest

from click import BadParameter, Command
from unittest.mock import MagicMock, patch
from vpype import Document

from vpype_mecode.config import ConfigOption, ConfigLoader
from vpype_mecode.builder.enums import LengthUnits, TimeUnits


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def mock_document():
    document = MagicMock(spec=Document)
    document.layers = {0: MagicMock(), 1: MagicMock()}
    return document

@pytest.fixture
def config_loader(sample_command):
    return ConfigLoader(sample_command)

@pytest.fixture
def sample_command():
    command = Command(name='sample_command')

    param1 = ConfigOption('work_speed', type=int, default=0)
    param2 = ConfigOption('length_units', type=LengthUnits, default=LengthUnits.MILLIMETERS)
    param3 = ConfigOption('time_units', type=TimeUnits, default=TimeUnits.MILLISECONDS)
    command.params = [param1, param2, param3]

    return command


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

def test_config_loader_initialization(sample_command):
    loader = ConfigLoader(sample_command)
    assert loader._command == sample_command

def test_validate_config_empty(config_loader):
    result = config_loader.validate_config({})
    assert result == {}

def test_validate_config_with_parameters(config_loader):
    result = config_loader.validate_config({
        'work_speed': 100,
        'length_units': 'mm',
        'unknown_param': 'value'  # Should be ignored
    })

    assert 'work_speed' in result
    assert 'length_units' in result
    assert 'unknown_param' not in result
    assert result['work_speed'] == 100
    assert result['length_units'] == 'mm'

@patch('vpype_mecode.config.config_loader.ConfigManager')
def test_read_config_file(mock_config_manager, config_loader, mock_document):
    manager_instance = mock_config_manager.return_value
    manager_instance.config = {}

    document_config = MagicMock()
    config_loader._to_config_model = MagicMock()
    config_loader._to_config_model.return_value = document_config
    result = config_loader.read_config_file('config.toml', mock_document)

    assert len(result) == 3  # Document + 2 layers
    assert result[0] == document_config
    assert result[1] == document_config
    assert result[2] == document_config

@patch('vpype_mecode.config.config_loader.ConfigManager')
def test_read_config_file_with_layers(mock_config_manager, config_loader, mock_document):
    manager_instance = mock_config_manager.return_value

    manager_instance.config = {
        'document': {
            'work_speed': 100,
            'length_units': 'in',
            'time_units': 'ms'
        },
        'layer-0': {
            'work_speed': 200,
            'length_units': 'mm',
            'time_units': 's'
        },
        'layer-1': {
            'work_speed': 300
        }
    }

    result = config_loader.read_config_file('config.toml', mock_document)

    assert len(result) == 3  # Document + 2 layers
    assert result[0].work_speed == 100
    assert result[0].length_units == 'in'
    assert result[0].time_units == 'ms'
    assert result[1].work_speed == 300 # Layers in reversed order
    assert result[2].work_speed == 200 # Layers in reversed order
    assert result[1].length_units == 'in' # Inherit from document
    assert result[2].length_units == 'in' # Inherit from document
    assert result[1].time_units == 'ms' # Inherit from document
    assert result[2].time_units == 'ms' # Inherit from document

@patch('vpype_mecode.config.config_loader.ConfigManager')
def test_read_config_file_invalid(mock_config_manager, config_loader, mock_document):
    manager_instance = mock_config_manager.return_value

    manager_instance.config = {
        'document': {
            'length_units': 'invalid_unit',
        }
    }

    with pytest.raises(BadParameter):
        config_loader.read_config_file('config.toml', mock_document)
