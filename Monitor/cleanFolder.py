import os
import glob

def cleanFolder(folder_path: str):
    """
    Delete all Excel files (*.xlsx, *.xls) inside the given folder.
    """
    # Ensure folder exists
    if not os.path.isdir(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return
    
    # Match Excel files
    files = glob.glob(os.path.join(folder_path, "*.xls*"))
    
    if not files:
        print(f"No Excel files found in: {folder_path}")
        return

    # Delete each file
    for f in files:
        os.remove(f)
        print(f"Deleted: {os.path.basename(f)}")

    print(f"Cleaned folder: {folder_path}")

