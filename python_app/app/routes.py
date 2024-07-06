from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from . import db
from .data_upload import upload_data
from .summary_report import generate_summary_report
from werkzeug.exceptions import BadRequest

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/upload_data', methods=['POST'])
@jwt_required()
def upload_data_route():
    """
    Flask route to upload data from a CSV file to the 'products' table in the database.

    Requires JWT authentication.

    Returns:
        A JSON response indicating successful data upload.

    Raises:
        BadRequest: If the 'file' key is missing from the request files.
    """
    try:
        # Check if 'file' key is present in request files
        if 'file' not in request.files:
            raise BadRequest("No file part in the request")
        
        csv_file = request.files['file']
        
        # Call the 'upload_data' function to process the CSV file
        upload_data(csv_file)
        
        # Return a success message
        return jsonify(message="Data uploaded successfully"), 201
    except BadRequest as e:
        # Return an error message
        return jsonify(message=str(e)), 400
    except Exception as e:
        # Handle any other exceptions
        return jsonify(message=f"An error occurred: {e}"), 500


@main_bp.route('/summary', methods=['GET'])
@jwt_required()
def summary_report():
    """
    Flask route to generate a summary report of the data in the 'products' table.

    Requires JWT authentication.

    Returns:
        A JSON response indicating successful generation of the summary report.
    """
    try:
        # Call the 'generate_summary_report' function to create the report
        generate_summary_report()
        
        # Return a success message
        return jsonify(message="Summary report generated"), 200
    except Exception as e:
        # Handle any exceptions
        return jsonify(message=f"An error occurred: {e}"), 500