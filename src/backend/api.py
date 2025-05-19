from fastapi import FastAPI, UploadFile, HTTPException
import tempfile
import os
from pathlib import Path
import logging
import json
from .text_extractor import TextExtractor
from .cid_detector import CIDDetector
from .text_highlighter import CIDHighlighter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/detect")
async def detect_cid(file: UploadFile):
    """
    Detect Client Identifying Data (CID) in uploaded document.
    Returns the detected CIDs.
    """
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=Path(file.filename).suffix
        ) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Create output file path
        highlighted_path = temp_file_path + "_highlighted.pdf"
        logger.info(f"Temp file: {highlighted_path}")
        try:
            # Extract text from file
            text = TextExtractor.extract_text(temp_file_path)

            # Detect CID
            cid_results = CIDDetector.detect_cid(text)

            # Ensure response structure
            if not isinstance(cid_results, dict) or "cid_entities" not in cid_results:
                cid_results = {"cid_entities": []}

            # Highlicht CID
            CIDHighlighter.highlight_cid_in_pdf(
                temp_file_path, highlighted_path, json.dumps(cid_results)
            )

            # Read the highlighted PDF
            with open(highlighted_path, "rb") as f:
                pdf_bytes = f.read()

            return {
                "text": text,
                "cid_results": cid_results["cid_entities"],
                "highlighted_pdf": pdf_bytes.hex(),
            }

        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            logger.info(f"The file has been processed!")

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health", summary="Health check")
def api_health():
    return {"status": "ok", "message": "Welcome to the CID Detection API."}
