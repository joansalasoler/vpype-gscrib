import pytest
from numpy import array
from vpype import Document, LineCollection
from unittest.mock import Mock, call

from vpype_gscrib.processor import DocumentProcessor
from vpype_gscrib.processor import DocumentRenderer


# --------------------------------------------------------------------
# Fixtures and helper classes
# --------------------------------------------------------------------

@pytest.fixture
def mock_renderer():
    return Mock(spec=DocumentRenderer)

@pytest.fixture
def processor(mock_renderer):
    return DocumentProcessor(renderer=mock_renderer)

@pytest.fixture
def empty_document():
    return Document()

@pytest.fixture
def sample_document():
    document = Document()
    layer = LineCollection()
    path1 = array([1+2j, 3+4j, 5+6j])
    path2 = array([7+8j, 9+10j])
    layer.append(path1)
    layer.append(path2)
    document.add(layer)
    print(document.layers)
    return document


# --------------------------------------------------------------------
# Test cases
# --------------------------------------------------------------------

def test_process_empty_document(processor, empty_document):
    processor.process(empty_document)
    processor.renderer.begin_document.assert_called_once_with(empty_document)
    processor.renderer.end_document.assert_called_once_with(empty_document)
    processor.renderer.begin_layer.assert_not_called()
    processor.renderer.end_layer.assert_not_called()

def test_process_document(processor, sample_document):
    processor.process(sample_document)
    processor.renderer.begin_document.assert_called_once_with(sample_document)
    processor.renderer.end_document.assert_called_once_with(sample_document)
    assert processor.renderer.begin_layer.call_count == 1
    assert processor.renderer.end_layer.call_count == 1
    assert processor.renderer.begin_path.call_count == 2
    assert processor.renderer.end_path.call_count == 2
    assert processor.renderer.trace_segment.call_count == 5

def test_trace_segment(processor, sample_document):
    processor.process(sample_document)
    layer = sample_document.layers[1]
    processor.renderer.trace_segment.assert_has_calls([
        call(layer.lines[0], 1.0, 2.0),
        call(layer.lines[0], 3.0, 4.0),
        call(layer.lines[0], 5.0, 6.0),
        call(layer.lines[1], 7.0, 8.0),
        call(layer.lines[1], 9.0, 10.0),
    ])
