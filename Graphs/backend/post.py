# import pandas as pd
# import psycopg2
# from datetime import datetime

# # --- Database connection ---
# conn = psycopg2.connect(
#     host="localhost",
#     database="287g_data",
#     user="postgres"
# )
# cur = conn.cursor()

# # --- Load Excel ---
# df = pd.read_excel("extracted_sheet.xlsx")

# # --- Helper functions ---
# def safe_val(val):
#     return None if pd.isna(val) else val

# def parse_date(val):
#     if val is None:
#         return None
#     if isinstance(val, str):
#         return datetime.strptime(val, "%Y-%m-%d").date() if "-" in val else datetime.strptime(val, "%Y/%m/%d").date()
#     return val.date() if hasattr(val, "date") else val

# # --- Clear tables and reset sequences ---
# cur.execute("DELETE FROM agencies;")
# cur.execute("DELETE FROM counties;")
# cur.execute("DELETE FROM states;")
# cur.execute("DELETE FROM status;")

# cur.execute("ALTER SEQUENCE states_state_id_seq RESTART WITH 1;")
# cur.execute("ALTER SEQUENCE counties_county_id_seq RESTART WITH 1;")
# cur.execute("ALTER SEQUENCE status_status_id_seq RESTART WITH 1;")
# cur.execute("ALTER SEQUENCE agencies_agency_id_seq RESTART WITH 1;")

# # --- Caches to avoid duplicate inserts ---
# state_cache = {}
# status_cache = {}

# for _, row in df.iterrows():
#     # --- Insert state (avoid duplicates) ---
#     state_name = safe_val(row['STATE'])
#     state_id = None
#     if state_name:
#         if state_name in state_cache:
#             state_id = state_cache[state_name]
#         else:
#             cur.execute("SELECT state_id FROM states WHERE state_name=%s;", (state_name,))
#             existing_state = cur.fetchone()
#             if existing_state:
#                 state_id = existing_state[0]
#             else:
#                 cur.execute("INSERT INTO states (state_name) VALUES (%s) RETURNING state_id;", (state_name,))
#                 state_id = cur.fetchone()[0]
#             state_cache[state_name] = state_id

#     # --- Insert county ---
#     county_name = safe_val(row.get('COUNTY'))
#     county_id = None
#     if county_name:
#         cur.execute("INSERT INTO counties (county_name, state_id) VALUES (%s, %s) RETURNING county_id;", (county_name, state_id))
#         county_id = cur.fetchone()[0]

#     # --- Insert status (avoid duplicates) ---
#     status_name = safe_val(row.get('Status'))
#     status_id = None
#     if status_name:
#         if status_name in status_cache:
#             status_id = status_cache[status_name]
#         else:
#             cur.execute("SELECT status_id FROM status WHERE status_name=%s;", (status_name,))
#             existing_status = cur.fetchone()
#             if existing_status:
#                 status_id = existing_status[0]
#             else:
#                 cur.execute("INSERT INTO status (status_name) VALUES (%s) RETURNING status_id;", (status_name,))
#                 status_id = cur.fetchone()[0]
#             status_cache[status_name] = status_id

#     # --- Insert agency ---
#     cur.execute("""
#         INSERT INTO agencies
#         (agency_name, type, support_type, county_id, signed, last_seen, status_id, extracted_link)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
#     """, (
#         safe_val(row['Agency Validation']),
#         safe_val(row.get('TYPE')),
#         safe_val(row.get('SUPPORT TYPE')),
#         county_id,
#         parse_date(row.get('SIGNED')),
#         parse_date(row.get('LAST SEEN')),
#         status_id,
#         safe_val(row.get('EXTRACTED LINK'))
#     ))

# # --- Commit and close ---
# conn.commit()
# cur.close()
# conn.close()

# print(f"All {len(df)} rows inserted successfully!")


import pandas as pd
import psycopg2
from datetime import datetime

# --- Database connection ---
conn = psycopg2.connect(
    host="localhost",
    database="287g_data",
    user="postgres"
)
cur = conn.cursor()

# --- Load Excel ---
df = pd.read_excel("extracted_sheet.xlsx")

# --- Helper functions ---
def safe_val(val):
    return None if pd.isna(val) else val

def parse_date(val):
    if val is None:
        return None
    if isinstance(val, str):
        return datetime.strptime(val, "%Y-%m-%d").date() if "-" in val else datetime.strptime(val, "%Y/%m/%d").date()
    return val.date() if hasattr(val, "date") else val

# --- Clear tables and reset sequences ---
cur.execute("DELETE FROM agencies;")
cur.execute("DELETE FROM counties;")
cur.execute("DELETE FROM states;")
cur.execute("DELETE FROM status;")

cur.execute("ALTER SEQUENCE states_state_id_seq RESTART WITH 1;")
cur.execute("ALTER SEQUENCE counties_county_id_seq RESTART WITH 1;")
cur.execute("ALTER SEQUENCE status_status_id_seq RESTART WITH 1;")
cur.execute("ALTER SEQUENCE agencies_agency_id_seq RESTART WITH 1;")

# --- Caches to avoid duplicate inserts ---
state_cache = {}
status_cache = {}
county_cache = {}  # key = (county_name, state_id)

for _, row in df.iterrows():
    # --- Insert state (avoid duplicates) ---
    state_name = safe_val(row['STATE'])
    state_id = None
    if state_name:
        if state_name in state_cache:
            state_id = state_cache[state_name]
        else:
            cur.execute("SELECT state_id FROM states WHERE state_name=%s;", (state_name,))
            existing_state = cur.fetchone()
            if existing_state:
                state_id = existing_state[0]
            else:
                cur.execute("INSERT INTO states (state_name) VALUES (%s) RETURNING state_id;", (state_name,))
                state_id = cur.fetchone()[0]
            state_cache[state_name] = state_id

    # --- Insert county (avoid duplicates) ---
    county_name = safe_val(row.get('COUNTY'))
    county_id = None
    if county_name:
        key = (county_name, state_id)
        if key in county_cache:
            county_id = county_cache[key]
        else:
            cur.execute("SELECT county_id FROM counties WHERE county_name=%s AND state_id=%s;", (county_name, state_id))
            existing_county = cur.fetchone()
            if existing_county:
                county_id = existing_county[0]
            else:
                cur.execute("INSERT INTO counties (county_name, state_id) VALUES (%s, %s) RETURNING county_id;", (county_name, state_id))
                county_id = cur.fetchone()[0]
            county_cache[key] = county_id

    # --- Insert status (avoid duplicates) ---
    status_name = safe_val(row.get('Status'))
    status_id = None
    if status_name:
        if status_name in status_cache:
            status_id = status_cache[status_name]
        else:
            cur.execute("SELECT status_id FROM status WHERE status_name=%s;", (status_name,))
            existing_status = cur.fetchone()
            if existing_status:
                status_id = existing_status[0]
            else:
                cur.execute("INSERT INTO status (status_name) VALUES (%s) RETURNING status_id;", (status_name,))
                status_id = cur.fetchone()[0]
            status_cache[status_name] = status_id

    # --- Insert agency ---
    cur.execute("""
        INSERT INTO agencies
        (agency_name, type, support_type, county_id, signed, last_seen, status_id, extracted_link)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        safe_val(row['Agency Validation']),
        safe_val(row.get('TYPE')),
        safe_val(row.get('SUPPORT TYPE')),
        county_id,
        parse_date(row.get('SIGNED')),
        parse_date(row.get('LAST SEEN')),
        status_id,
        safe_val(row.get('EXTRACTED LINK'))
    ))

# --- Commit and close ---
conn.commit()
cur.close()
conn.close()

print(f"All {len(df)} rows inserted successfully!")

