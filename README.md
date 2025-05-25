# ICE 287(g) Program Archive and Analysis

This project collects, processes, and analyzes historical snapshots of the [ICE 287(g) program webpage](https://www.ice.gov/identify-and-arrest/287g) using data from the Wayback Machine. It extracts structured data, saves Excel files of participating and pending agencies, and filters snapshots based on specific dates (especially before and after February 20, 2025).

---

## 📁 Project Structure
```
287g/
├── archive-url-snapshot.py
├── combine_yearly_urls.py
├── extract_287g_after_feb20_snapshot.py
├── extract_287g_before_feb20_snapshot.py
├── extract_sheets_after_feb20_.py
├── extract_sheets_before_feb20.py
├── filtered_snapshots_every_3_days.xlsx
├── filter_snapshots_every_3_days.py
├── ice_287g_snapshots.xlsx
├── sheets_every_2_days.xlsx
├── Participating Entities before feb 20/
│   └── (Excel files with agencies before February 20)
│
├── participatingAgencies/
│   └── (Excel files with agencies after February 20)
│
└── pendingAgencies/
    └── (Excel files for pending agencies after February 20)
```
## 📌 Key Functionalities

### 1. `archive-url-snapshot.py`
- Fetches all Wayback Machine snapshots of the 287(g) page.
- Saves metadata (timestamp with date and archive URL) to `ice_287g_snapshots.xlsx`.

### 2. `extract_sheets_before_feb20.py`
- Processes multiple early snapshots.
- Extracts tables of participating entities before Feb 20.
- Saves results in `Participating Entities before feb 20/`.

### 3. `extract_sheets_after_feb20.py`
- Downloads Excel files from links in the page.
- Saves output to `participatingAgencies/` and `pendingAgencies/`

### 4. `filter_snapshots_every_3_days.py`
- Filters the snapshot list to optimize scraping intervals of 3 days.
- Outputs to `filtered_snapshots_every_3_days.xlsx`.

### 5. `Participating Entities before feb 20/`
- This folder contains Excel files that have been parsed from snapshots taken before February 20, 2025.
- Each Excel file is named with the snapshot date and contains a table of agencies involved in the program.

### 6. `participatingAgencies/`
- This folder stores Excel files that are based on snapshots taken **after February 20, 2025**.
- Each Excel file corresponds to a snapshot with a timestamp and includes the list of agencies that are currently participating in the program.

### 7. `pendingAgencies/`
- This folder holds Excel files that provide data about agencies that are **pending** or in the process of joining the 287(g) program.
- These files are based on snapshots taken **after February 20, 2025**.

---

