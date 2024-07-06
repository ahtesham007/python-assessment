import pandas as pd
from .models import Product
from . import db
from sqlalchemy.exc import SQLAlchemyError
import logging

def upload_data(csv_file):
    """
    Uploads data from a CSV file to the 'products' table in the database.

    Args:
        csv_file (str): The path to the CSV file containing the data to be uploaded.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        SQLAlchemyError: If there is an issue with the database connection or SQL execution.
    """
    try:
        # Read data from CSV file
        df = pd.read_csv(csv_file)
        # Upload data to 'products' table
        df.to_sql('products', db.engine, if_exists='append', index=False)
        logging.info("Data uploaded successfully.")
    except FileNotFoundError as e:
        logging.error(f"Error: {e}")
        raise FileNotFoundError("File not found")
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        raise SQLAlchemyError(f"Upload failed : {e._message}")

# Example usage:
# upload_data('path_to_csv_file.csv')
