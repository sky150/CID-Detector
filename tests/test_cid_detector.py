from src.backend.cid_detector import CIDDetector
import json


def test_cid_detector():
    detector = CIDDetector()
    test_text = """
    Rechnung
    Kundennr.: 12345
    IBAN: DE89 1000 1000 1000 00
    """
    results = detector.detect_cid(test_text)
    print(json.dumps(results, indent=2))
