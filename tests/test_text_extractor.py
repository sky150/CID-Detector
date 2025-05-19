import pytest
from src.backend.text_extractor import TextExtractor
import os

# Path to your existing test file
TEST_PDF_PATH = "../data/CID-1.pdf"


def test_extracts_text_from_pdf():
    """Test extracts text from existing PDF"""
    if not os.path.exists(TEST_PDF_PATH):
        pytest.skip(f"Test file {TEST_PDF_PATH} not found")

    result = TextExtractor.extract_text(TEST_PDF_PATH)

    # Verify key content is extracted
    assert "Dr. Alice Smith" in result
    assert "221B Baker Street" in result
    assert "alice.smith@example.com" in result
    assert "+41 44 123 45 67" in result


def test_returns_string_type():
    """Test returns string type"""
    if not os.path.exists(TEST_PDF_PATH):
        pytest.skip(f"Test file {TEST_PDF_PATH} not found")

    result = TextExtractor.extract_text(TEST_PDF_PATH)
    assert isinstance(result, str)


def test_handles_missing_file():
    """Test raises error for missing files"""
    with pytest.raises(FileNotFoundError):
        TextExtractor.extract_text("non_existent_file.pdf")
