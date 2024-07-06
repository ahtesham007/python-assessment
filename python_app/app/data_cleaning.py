import pandas as pd
import logging

def clean_data(df):
    """
    Cleans the product data by handling missing values and ensuring numerical integrity.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame containing product data with columns 
                           ['price', 'quantity_sold', 'rating', 'category'].
    
    Returns:
    pandas.DataFrame: The cleaned DataFrame with missing values handled and 
                      numerical values coerced.
    
    Raises:
    ValueError: If the DataFrame does not contain the required columns.
    """
    required_columns = ['price', 'quantity_sold', 'rating', 'category']
    
    # Check if required columns are present
    if not all(column in df.columns for column in required_columns):
        raise ValueError(f"The DataFrame must contain the following columns: {required_columns}")
    
    try:
        # Handle missing values for 'price' and 'quantity_sold' by filling with the median
        df['price'] = df['price'].fillna(df['price'].median())
        df['quantity_sold'] = df['quantity_sold'].fillna(round(df['quantity_sold'].median()))

        # Handle missing values for 'rating' by filling with the average rating per category
        df['rating'] = df.groupby('category')['rating'].transform(lambda x: x.fillna(x.mean()))
        
        # Ensure 'price', 'quantity_sold', and 'rating' are numeric values
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    
    except Exception as e:
        logging.error(f"An error occurred while cleaning the data: {e}")
        raise RuntimeError(f"An error occurred while cleaning the data: {e}")
    
    return df