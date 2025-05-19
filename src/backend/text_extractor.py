import PyPDF2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextExtractor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extracts text from PDF files."""
        if not file_path.endswith(".pdf"):
            logger.error("Only PDFs supported")
            raise ValueError("Only PDFs supported")

        text = []
        reader = PyPDF2.PdfReader(file_path)
        for page in reader.pages:
            text.append(page.extract_text())
        return "\n".join(text)
