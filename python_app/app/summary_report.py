import pandas as pd
from .data_cleaning import clean_data
from . import db
import logging

def generate_summary_report():
    """
    Generate a summary report of products by category.

    This function queries the 'products' table from the database,
    cleans the data, groups it by category, and calculates the total revenue,
    top product, and top product quantity sold for each category.
    The summary is then saved to a CSV file 'summary_report.csv'.

    Raises:
        Exception: If there is an error in querying the database or writing to the CSV file.
    """
    try:
        # Query the 'products' table from the database
        df = pd.read_sql('products', db.engine)
        
        if df.empty:
            raise Exception("No data found")

        # Clean the data (assuming 'clean_data' is a predefined function)
        df = clean_data(df)
        
        # Group by category and calculate summary statistics
        total_revenue = df.groupby('category').apply(lambda x: (x['price'] * x['quantity_sold']).sum().round(2)).reset_index(name='total_revenue')
        top_products = df.loc[df.groupby('category')['quantity_sold'].idxmax()].reset_index()
        top_products = top_products[['category', 'product_name', 'quantity_sold']]
        top_products.columns = ['category', 'top_product', 'top_product_quantity_sold']
        summary = total_revenue.merge(top_products, on="category")

        # summary = df.groupby('category').agg(
        #     total_revenue=pd.NamedAgg(column='price', aggfunc='sum'),
        #     top_product=pd.NamedAgg(column='product_name', aggfunc=lambda x: x.iloc[0]),
        #     top_product_quantity_sold=pd.NamedAgg(column='quantity_sold', aggfunc='sum')
        # ).reset_index()
        
        # Save the summary to a CSV file
        summary.to_csv('summary_report.csv', index=False)
        logging.info("Summary report generated successfully.")
    except Exception as e:
        logging.error(e)
        raise Exception(e)

# Example usage of the function
# generate_summary_report()