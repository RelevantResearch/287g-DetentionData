import os
import sys
import logging
from dotenv import load_dotenv
from messageToSlack import send_message_to_slack
from getFilename import find_latest_file  # Assuming you have this helper function

# Set up the base directory (monitor folder)
base_dir = os.path.dirname(__file__)

# Configure logging to save logs in the 'monitor' folder
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(base_dir, 'log.txt'), mode='a', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Add current directory to sys.path to import local modules
sys.path.append(os.path.dirname(__file__))

# Function to get the latest file date based on filename format
def get_latest_file_date(directory):
    latest_filename = find_latest_file(directory)
    if not latest_filename:
        logging.warning(f"No matching files found in {directory}.")
        return None
    
    latest_file_path = os.path.join(directory, latest_filename)
    logging.info(f"Found latest file: {latest_filename}")

    # Modify the logic to extract the date from filenames like "Total-participatingAgencies04302025pm.xlsx"
    try:
        # Extract the date from the filename
        file_date = ''.join(filter(str.isdigit, latest_filename))  # Extract digits from the filename
        file_date = file_date[:8]  # Get the first 8 digits (YYYYMMDD format)
        
        if len(file_date) != 8:
            raise ValueError("Date in filename is not in the expected format.")
        
        return file_date
    except Exception as e:
        logging.error(f"Error extracting date from filename: {e}")
        return None

def main():
    logging.info("**********Starting Script************")
    logging.info("Step 0: Monitoring and downloading latest Excel files...")

    # Set directory for 287g files
    base_dir = os.path.dirname(__file__)
    data_directory = os.path.join(base_dir, '..', 'Total participatingAgencies')

    # Check for the latest 287(g) file and get the date
    latest_date = get_latest_file_date(data_directory)

    if latest_date:
        # Send a message to Slack with the latest file date
        message = f"287(g) Alert: The latest 287(g) file has been updated on {latest_date}."
        
        # Send the message to Slack with the date in the alert
        send_message_to_slack(message)

        logging.info(f"Alert sent to Slack: {message}")
    else:
        logging.info("No new files detected. Skipping message.")

    logging.info("**********Script Completed************")

if __name__ == "__main__":
    main()
