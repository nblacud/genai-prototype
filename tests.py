import os

def get_dataset_path():
    
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    #csv_path = os.path.join(current_dir, "..", "data", "customer_reviews.csv")
    return current_dir

print(get_dataset_path())