from unittest.mock import MagicMock

import pytest
from numpy import array
from vpype import Document, LineCollection
from vpype_gscrib.config import RenderConfig
from gscrib import GCodeBuilder
from vpype_gscrib.renderer import GRenderer


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def mock_builder():
    return GCodeBuilder()

@pytest.fixture
def mock_config():
    return RenderConfig.model_validate({})

@pytest.fixture
def mock_configs(mock_config):
    return [mock_config, mock_config]

@pytest.fixture
def grenderer(mock_builder, mock_configs):
    renderer = GRenderer(mock_builder, mock_configs)
    renderer._head_type.trace_to = MagicMock()
    renderer._g.teardown = MagicMock()
    return renderer

@pytest.fixture
def mock_document():
    document = MagicMock(spec=Document)
    document.layers = {0: MagicMock()}
    document.page_size = (100, 100)
    return document

@pytest.fixture
def mock_layer():
    path = array([0 + 0j, 1 + 1j, 2 +  2j])
    layer = LineCollection([path])
    layer.set_property('vp_name', 'test_layer')
    return layer


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

def test_grenderer_initialization(grenderer):
    assert grenderer._g is not None
    assert grenderer._context is not None
    assert grenderer._document_context is not None
    assert grenderer._bed_type is not None
    assert grenderer._coolant_type is not None
    assert grenderer._fan_type is not None
    assert grenderer._head_type is not None
    assert grenderer._rack_type is not None
    assert grenderer._tool_type is not None
    assert len(grenderer._ctx_queue) > 1

def test_begin_document(grenderer, mock_document):
    grenderer.begin_document(mock_document)
    assert grenderer._context == grenderer._document_context
    assert grenderer._g.state.distance_mode is not None
    assert grenderer._g.state.feed_mode is not None
    assert grenderer._g.state.length_units is not None
    assert grenderer._g.state.plane is not None

def test_begin_layer(grenderer, mock_layer):
    initial_context = grenderer._context
    grenderer.begin_layer(mock_layer)
    assert grenderer._context is not None
    assert grenderer._context != initial_context

def test_begin_path(grenderer, mock_layer):
    initial_context = grenderer._context
    grenderer.begin_path(mock_layer.lines[0])
    assert grenderer._context is not None
    assert grenderer._context == initial_context

def test_trace_segment(grenderer):
    initial_context = grenderer._context
    x, y = 10.0, 10.0
    path = array([0 + 0j, 10 + 10j])
    grenderer.trace_segment(path, x, y)
    assert grenderer._context is not None
    assert grenderer._context == initial_context
    grenderer._head_type.trace_to.assert_called_once()

def test_end_path(grenderer, mock_layer):
    initial_context = grenderer._context
    grenderer.end_path(mock_layer.lines[0])
    assert grenderer._context is not None
    assert grenderer._context == initial_context

def test_end_layer(grenderer, mock_layer):
    initial_context = grenderer._context
    grenderer.end_layer(mock_layer)
    assert grenderer._context is not None
    assert grenderer._context == initial_context

def test_end_document(grenderer, mock_document):
    grenderer.end_document(mock_document)
    assert grenderer._context == grenderer._document_context
    grenderer._g.teardown.assert_called_once()

def test_process_error(grenderer):
    test_error = Exception("Test error")
    grenderer.process_error(test_error)
    grenderer._g.teardown.assert_called_once()
