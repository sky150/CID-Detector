import streamlit as st
import requests
import tempfile
import os
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv(f"API_HOST_LOCAL")

st.set_page_config(page_title="CID Detector", page_icon="🔍", layout="wide")

st.title("CID Detector")
st.markdown(
    """
This tool helps you detect Client Identifying Data (CID) in your documents.
Upload a PDF file to get started.
"""
)

uploaded_file = st.file_uploader("Choose a file", type=["pdf"])

if uploaded_file is not None:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=Path(uploaded_file.name).suffix
    ) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # Create progress bar and status text
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        # Update progress
        status_text.text("Analyzing document...")
        progress_bar.progress(25)

        # Send file to backend
        files = {"file": (uploaded_file.name, open(tmp_file_path, "rb"))}
        response = requests.post(
            f"{API_URL}/detect", files=files, headers={"Accept": "application/json"}
        )

        # Update progress
        progress_bar.progress(75)

        if response.status_code == 200:
            data = response.json()
            text = data["text"]
            cid_results = data["cid_results"]
            highlighted_pdf = bytes.fromhex(data["highlighted_pdf"])

            # Update progress
            progress_bar.progress(100)
            status_text.text("Analysis complete!")

            # Display detected CIDs
            st.subheader("Detected CIDs")

            if not cid_results or all(not result["text"] for result in cid_results):
                st.info("No CIDs detected in the document.")
            else:
                st.warning("CIDs detected in the document! Please review carefully.")
                st.divider()

                # Prepare data for table - using a dictionary to track unique text per entity type
                table_data = []
                entity_text_counts = defaultdict(lambda: defaultdict(int))

                # Count unique occurrences
                for result in cid_results:
                    text = result["text"].strip()
                    if text:  # Only process non-empty texts
                        entity_text_counts[result["entity_type"]][text] += 1

                # Create table rows (no duplicates)
                for entity_type, texts in entity_text_counts.items():
                    for text, count in texts.items():
                        table_data.append(
                            {
                                "Entity Type": entity_type,
                                "Text": text,
                                "Occurrences": count,
                            }
                        )

                # Sort by entity type for better organization
                table_data.sort(key=lambda x: x["Entity Type"])

                # Display as table
                st.table(table_data)

                # Create download button for the highlighted file
                st.download_button(
                    label="Download Highlighted PDF",
                    data=highlighted_pdf,
                    file_name=f"highlighted_{uploaded_file.name}",
                    mime="application/pdf",
                )

        else:
            error_msg = f"Error: {response.text}"
            if response.status_code == 403:
                error_msg = "Error: Access denied. Please make sure the API server is running and accessible."
            st.error(error_msg)
            progress_bar.progress(0)
            status_text.text("Error occurred during analysis.")

    except requests.exceptions.ConnectionError:
        st.error(
            "Error: Could not connect to the API server. Please make sure it's running at http://localhost:8000"
        )
        progress_bar.progress(0)
        status_text.text("Error occurred during analysis.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        progress_bar.progress(0)
        status_text.text("Error occurred during analysis.")

    finally:
        # Clean up the temporary file
        os.unlink(tmp_file_path)
        if "files" in locals():
            files["file"][1].close()
