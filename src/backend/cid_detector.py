from typing import List, Dict, Any
import logging
import ollama
import json
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()


class CIDDetector:

    @staticmethod
    def detect_cid(text: str) -> List[Dict[str, Any]]:
        """
        Detect Client Identifying Data in text.
        Returns a list of detected entities with their positions and scores.
        """
        # System prompt explaining CID and requiring JSON output
        SYSTEM_PROMPT = """
        You are an expert at extracting Client Identifying Data (CID) from invoices.
        Extract ALL CID from the following text and return ONLY JSON in this format:
        {
        "cid_entities": [
            {"entity_type": "TYPE", "text": "EXACT_MATCH_FROM_TEXT"}
        ]
        }
        
        Entity types to extract:
        - NAME (personal or company names)
        - ADDRESS (full addresses)
        - IBAN (bank account numbers)
        - BIC (bank codes)
        - VAT_ID (tax IDs)
        - INVOICE_NUMBER
        - PHONE (phone numbers)
        - EMAIL (email addresses)
        
        Rules:
        1. Only return the JSON object, no other text
        2. Find ALL instances, not just the first one
        3. Use exact matches from the text
        """

        result = ""
        env_mode = os.getenv("ENV_MODE")
        logger.info(f"ENV: {env_mode}")

        try:
            clean_text = " ".join(text.split())

            client = (
                ollama.Client(host=os.getenv("OLLAMA_HOST_DOCKER"))
                if env_mode == "docker"
                else ollama
            )
            logger.info(f"Client: {client}")
            response = client.chat(  
                model=os.getenv("OLLAMA_MODEL"),
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Extract ALL CID from this invoice text:\n{clean_text}",
                    },
                ],
                options={"temperature": 0.0, "format": "json"},
            )
            result = response["message"]["content"].strip()
            logger.info(f"Raw LLM Response result: {result}")

            if result.startswith("```"):
                result = result[result.find("{") : result.rfind("}") + 1]
                logger.info(f"result: {result}")

            cid_data = json.loads(result)
            logger.info(f"result: {cid_data}")

            assert isinstance(cid_data.get("cid_entities", None), list)
            return cid_data

        except Exception as e:
            logger.error(f"CID detection failed: {str(e)}\nResponse: {result}")
            return {"cid_entities": []}
