import fitz  # PyMuPDF
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CIDHighlighter:

    @staticmethod
    def highlight_cid_in_pdf(input_path, output_path, cid_json):
        """
        Highlights all CID entities in PDF by searching for exact text matches
        Param:
            input_path: Path to input PDF
            output_path: Path to save highlighted PDF
            cid_json: JSON string with CID entities (from LLM response)
        """

        doc = fitz.open(input_path)
        logger.info(f"Doc: {doc}")

        cid_data = json.loads(cid_json)
        logger.info(f"Cid_json: {cid_json}")

        for page in doc:
            for entity in cid_data["cid_entities"]:
                text_to_highlight = entity["text"]
                # logger.info(f"Inside For-loop")

                # Skip empty text fields
                if not text_to_highlight.strip():
                    logger.info(f"Skipping empty {entity['entity_type']}")
                    continue

                # Search for exact text (case-sensitive)
                text_instances = page.search_for(text_to_highlight)

                # Highlight all found instances
                for inst in text_instances:
                    highlight = page.add_highlight_annot(inst)
                    highlight.update()

        logger.info(output_path)
        doc.save(output_path)
        logger.info(f"Highlighted PDF saved to: {output_path}")
