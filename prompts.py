"""
This prompt file contains all the prompts that are used in the application.

CLASSIFICATION_PROMPT: prompt used to classify if a pdf is a valid bank statement or not.
"""

CLASSIFICATION_PROMPT = ""


"""
TABULIZATION_PROMPT: prompt used to tabularize the text from the pdf.
"""

TABULIZATION_PROMPT = """The following text is a bank statement containing structured tables of transaction data along with other text. Extract all the tables from the text. For each table:
1. Assign a descriptive title based on the content of the table (e.g., "Account Summary", "Checks", "Deposits and Credits").
2. Format the table as JSON with the following structure:
   {
       "title": "Table Title",
       "header": ["Column1", "Column2", "Column3"],
       "rows": [
           ["Row1Value1", "Row1Value2", "Row1Value3"],
           ["Row2Value1", "Row2Value2", "Row2Value3"]
       ]
   }
3. If multiple tables exist, return them as a list of JSON objects under the key `"tables"`. Ensure each table has a unique title.
   
Text data from the bank statement:"""

def getClassificationPrompt():
    return CLASSIFICATION_PROMPT

def getTabulizationPrompt(text: str) -> str:
    return f"{TABULIZATION_PROMPT} {text}"