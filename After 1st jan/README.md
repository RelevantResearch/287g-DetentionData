roject Directory Overview

This directory contains scripts and Excel files related to processing and combining data from participating agencies, categorized based on the dates of collection.

## Root Files
- **Python Scripts**:
  - `combine.py`: Combines multiple Excel files into a single workbook.
  - `combine hyperlink.py`: Similar to `combine.py` but extract hyperlinks from the column MOA and then place it in the new column i.e. Extracted Link.
- **Excel Files**:
  - `combined_result.xlsx`: Final combined Excel file.
  - `combined_result_with_links.xlsx`: Combined Excel file with hyperlinks.
  - `participatingAgencies-*.xlsx`: Multiple Excel files generated at different timestamps, representing different snapshots of participating agency data.
  - `participatingAgencies_with_links.xlsx`: Combined data with hyperlinks for easy navigation.

## Subdirectories

### after feb 20
- **Description**:  
  Contains Excel files and scripts related to participating agencies data collected after February 20, 2025.
- **Contents**:
  - `after.py`, `after after.py`: Scripts for handling post-February datasets.
  - `combine_with_links.xlsx`, `combine_without_duplicates.xlsx`: Processed datasets.
  - A series of timestamped Excel files similar to the root folder but processed for post-February data.

### before feb 20
- **Description**:  
  Contains Excel files and scripts related to participating agencies data collected before February 20, 2025.
- **Contents**:
  - `combine both final files.py`: Combines "before" datasets into one.
  - `filter.py`, `filter with link.py`: Scripts to filter records, possibly removing duplicates or adding hyperlinks.
  - `deduplicated_output.xlsx`, `after_deduplicated_links.xlsx`, `after_deduplicated_removal.xlsx`: Cleaned and deduplicated Excel datasets.
  - Multiple timestamped Excel files representing the earlier data collection