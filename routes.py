from flask import Blueprint, request, jsonify, send_file
from flask_cors import CORS
from pdfprocessor import *
from werkzeug.utils import secure_filename
import zipfile
import tempfile
import io

main = Blueprint('main', __name__, static_folder='static', template_folder='templates')
CORS(main)

@main.route('/test', methods=['GET', 'POST'])
def test():
    return jsonify({"message": "Hello, World!"})

@main.route('/process-pdf', methods=['POST', 'GET'])
def process_pdf():
    # Handle GET: Return instructions
    if request.method == 'GET':
        print( "uhh this aint it chief")
        return "Please send a POST request with a PDF file (via form-data field named 'file') to process it."
    
    if request.files:
        print(request.files)
    else:
        print('no files ya bitch')

    # Handle POST: Process the uploaded PDF
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    
    # If no file was selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Secure the filename to avoid directory traversal attacks
    filename = secure_filename(file.filename)
    
    # Check if the file is a PDF (simple check, more robust checks may be needed)
    if not filename.lower().endswith('.pdf'):
        return jsonify({"error": "File provided is not a PDF"}), 400

    # Save the PDF file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        file.save(temp_pdf.name)
        temp_pdf_path = temp_pdf.name

    # Initialize our PDF processor
    processor = PDFProcessor()

    try:
        # Process the PDF to obtain CSV data
        csv_dict = processor.process(temp_pdf_path)

        # If no tables or CSV data returned
        if not csv_dict:
            return jsonify({"error": "No tabulated data found in the PDF."}), 200

        # Create an in-memory ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for table_name, csv_data in csv_dict.items():
                # Make a filename-safe version of the table name
                safe_table_name = secure_filename(table_name)
                # Each CSV is added as a file in the ZIP
                zipf.writestr(f"{safe_table_name}.csv", csv_data)

        # Move to the beginning of the BytesIO buffer
        zip_buffer.seek(0)

        # Send the ZIP file as a download
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='processed_data.zip'
        )

    except Exception as e:
        # In case of any processing errors
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)