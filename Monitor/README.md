# Script Overview

This script automates the monitoring, processing, and emailing of files related to participating and pending agencies. The workflow involves monitoring a webpage for new files, processing them, sending them via email, and pushing updates to GitHub. Below are the steps performed by the script:

## Steps in the Script:

### 1. **Monitor and Download Latest Files**
   - Monitors the specified URL (`https://www.ice.gov/identify-and-arrest/287g`) for any new files (Excel files).
   - If a new file is detected, the script downloads it for further processing.

### 2. **Process Participating Agencies**
   - **Extract Hyperlinks**: Extracts hyperlinks from the latest downloaded Excel file and saves them in a designated folder.
   - **Combine Files**: Combines the extracted hyperlinks with the total participating agencies data.
   - **Remove Processed Files**: Deletes the processed hyperlink file after it has been handled.

### 3. **Process Pending Agencies**
   - **Combine Pending Agencies**: Combines data from pending agencies.
   - **Deduplicate**: Removes duplicate entries from the combined data.
   - **Clean-up**: Deletes any leftover duplicated files after processing.

### 4. **Broadcast Email**
   - Sends an email with the latest participating and pending agencies files as attachments.
   - The email is sent using SendGrid with the API key, from email, and recipient list retrieved from environment variables.

### 5. **Push Files to GitHub**
   - Pushes the latest files to a GitHub repository for backup and sharing.

### 6. **Logging**
   - Logs all steps of the script for easy tracking of the operations performed. This includes both successful and failed steps.
   - Logs are saved in a file called `log.txt` and displayed on the console for real-time monitoring.


# Script Descriptions

- **getFilename.py** -> Finds the most recent date participating and pending agencies file in a specified folder.

- **getHyperlink.py** -> Extracts all hyperlinks (URLs) from a sheet and keep in 'EXTRACTED LINK' column.

- **combineFiles.py** -> Combines both hyperlinked participating file and get the latest date file from folder into one.

- **monitorSheets.py** -> Monitors and downloads sheet if updateed from a source.

- **pushGithub.py** -> Automates the process of pushing files to a GitHub repository.

- **send_email.py** -> Broadcasts automated emails with necessary files or updates.

- **combinePendingAgencies.py** -> Combines currently downlaoded sheet and get the latest date file pending agencies file.

- **deduplicate_pending_combined.py** -> Removes duplicate records from a combined dataset of pending agencies.