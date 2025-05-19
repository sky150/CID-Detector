import os
import argparse
import json
from dotenv import load_dotenv
from src.backend.cid_detector import CIDDetector
from src.backend.text_extractor import TextExtractor

load_dotenv()


def main():
    print(f"Using model: {os.getenv('OLLAMA_MODEL')}")
    print(f"Connecting to: {os.getenv('OLLAMA_HOST_LOCAL')}")
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Detect Client Identifying Data in documents"
    )
    parser.add_argument("file_path", help="Path to the PDF file to analyze")

    args = parser.parse_args()

    # Process the file
    try:
        print(f"Analyzing {args.file_path}...")
        text = TextExtractor().extract_text(args.file_path)
        results = CIDDetector().detect_cid(text)

        # Print pretty JSON results
        print("\nDetection Results:")
        print(json.dumps(results, indent=2))

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
