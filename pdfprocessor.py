import os
from dotenv import load_dotenv
import pdfplumber
import google.generativeai as genai
import typing_extensions as typing
import json
import pandas
import typing

# internal imports:
from prompts import *

load_dotenv()

class PDFProcessor:

    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def process(self, pdf_file_path: str):
        # Process flow of the processing the PDF file

        # Generate the text of the file
        text = self._extract_text_from_pdf(pdf_file_path)
        print('extracted text')

        # Preprocess the table data
        processed_data = self._jsonifyText(text)
        print('processed data')

        # Return the table data
        return self._processTables(processed_data)

    def _extract_text_from_pdf(self, pdf_file_path: str) -> str:
        """
        Extracts text from a PDF file using the pdfplumber library.

        Args:
            pdf_file_path (str): The path to the PDF file.
        Returns:
            str: The extracted text from the PDF file.
        """
        with pdfplumber.open(pdf_file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text

    def _jsonifyText(self, pdf_text_data):
        """
        Converts the tabularized text data into a JSON format.

        Args:
            pdf_text_data (str): The tabularized text data.
        Returns:
            dict: The tabularized text data in JSON format.
        """
        prompt = getTabulizationPrompt(pdf_text_data)
        result = self.model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json"
                    )
                )
        return json.loads(result.candidates[0].content.parts[0].text)

    def _processTables(self, pdf_dict):
        # Preprocess the table data

        # Extract tables:
        tables = pdf_dict.get("tables", [])

        if not tables:
            print("No tables found in the PDF.")
            return None
        
        # Convert tables to CSV format
        csvs = {}
        for table in tables:
            df = pandas.DataFrame(table["rows"], columns=table["header"])
            csvs[table["title"]] = df.to_csv(index=False)
    
        return csvs