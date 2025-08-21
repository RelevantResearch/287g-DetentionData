# # import pandas as pd
# # import matplotlib.pyplot as plt

# # # Read Excel file (only the relevant columns)
# # df = pd.read_excel(
# #     "support_type_summary.xlsx",
# #     usecols=["date", "Task Force Model", "Warrant Service Officer", "Jail Enforcement Model"]
# # )

# # # Convert date to datetime
# # df["date"] = pd.to_datetime(df["date"])
# # df = df.sort_values("date")

# # x_positions = range(len(df))

# # plt.figure(figsize=(14, 7))

# # # Plot stacked bars
# # bars_wso = plt.bar(x_positions, df["Warrant Service Officer"], label="Warrant Service Officer", color="#3498DB")
# # bars_jem = plt.bar(x_positions, df["Jail Enforcement Model"], bottom=df["Warrant Service Officer"], label="Jail Enforcement Model", color="#E74C3C")
# # bars_tfm = plt.bar(x_positions, df["Task Force Model"], bottom=df["Warrant Service Officer"] + df["Jail Enforcement Model"], label="Task Force Model", color="#2ECC71")

# # plt.title("Agreements Over Time (Stacked by Type)", fontsize=16)
# # plt.xlabel("Date", fontsize=12)
# # plt.ylabel("Number of Agreements", fontsize=12)
# # plt.grid(axis="y", alpha=0.3)
# # plt.xticks(x_positions, df["date"].dt.strftime("%m/%d/%y"), rotation=45)
# # plt.legend()

# # # Add value labels
# # for i in x_positions:
# #     # Warrant Service Officer
# #     wso_val = df["Warrant Service Officer"][i]
# #     if wso_val < 15:  # small values
# #         plt.text(i, wso_val + 2, f"{wso_val}", ha="center", va="bottom", color="red", fontsize=9)
# #     else:
# #         plt.text(i, wso_val/2, f"{wso_val}", ha="center", va="center", color="white", fontsize=9)

# #     # Jail Enforcement Model
# #     jem_val = df["Jail Enforcement Model"][i]
# #     bottom_jem = df["Warrant Service Officer"][i]
# #     if jem_val < 15:
# #         plt.text(i, bottom_jem + jem_val + 2, f"{jem_val}", ha="center", va="bottom", color="red", fontsize=9)
# #     else:
# #         plt.text(i, bottom_jem + jem_val/2, f"{jem_val}", ha="center", va="center", color="white", fontsize=9)

# #     # Task Force Model
# #     tfm_val = df["Task Force Model"][i]
# #     bottom_tfm = df["Warrant Service Officer"][i] + df["Jail Enforcement Model"][i]
# #     if tfm_val < 15:
# #         plt.text(i, bottom_tfm + tfm_val + 2, f"{tfm_val}", ha="center", va="bottom", color="red", fontsize=9)
# #     else:
# #         plt.text(i, bottom_tfm + tfm_val/2, f"{tfm_val}", ha="center", va="center", color="white", fontsize=9)

# # plt.tight_layout()
# # plt.savefig("agreements_stacked_bar_adjusted.png", dpi=300, bbox_inches="tight")
# # print("✅ Saved as agreements_stacked_bar_adjusted.png")


# # # import pandas as pd
# # # import matplotlib.pyplot as plt

# # # # Read Excel file (only date and Jail Enforcement Model columns)
# # # df = pd.read_excel("support_type_summary.xlsx", usecols=["date", "Jail Enforcement Model"])

# # # # Convert date to datetime
# # # df["date"] = pd.to_datetime(df["date"])
# # # df = df.sort_values("date")

# # # # Equal spacing for x-axis positions
# # # x_positions = range(len(df))

# # # # Create the plot
# # # plt.figure(figsize=(12, 6))
# # # plt.plot(
# # #     x_positions,
# # #     df["Jail Enforcement Model"],
# # #     marker="o",
# # #     linewidth=2,
# # #     markersize=6,
# # #     color="#3498DB",         # Line color
# # #     markerfacecolor="#E74C3C",  # Marker fill color
# # #     markeredgecolor="#3498DB"   # Marker border color
# # # )

# # # # Titles and labels
# # # plt.title("Jail Enforcement Model Over Time", fontsize=16)
# # # plt.xlabel("Date", fontsize=12)
# # # plt.ylabel("Jail Enforcement Model", fontsize=12)
# # # plt.grid(True, alpha=0.3)

# # # # X-axis date labels with equal spacing
# # # plt.xticks(x_positions, df["date"].dt.strftime("%m/%d/%y"), rotation=45)

# # # # Add value labels above each point
# # # for i, value in enumerate(df["Jail Enforcement Model"]):
# # #     plt.annotate(
# # #         f"{value}",
# # #         (i, value),
# # #         textcoords="offset points",
# # #         xytext=(0, 10),
# # #         ha="center",
# # #         fontsize=9
# # #     )

# # # # Adjust layout to prevent label cutoff
# # # plt.tight_layout()

# # # # Save the figure
# # # plt.savefig("Jail_Enforcement_Model_line.png", dpi=300, bbox_inches="tight")
# # # print("✅ Saved as task_force_line_graph.png")

# # import pandas as pd
# # import matplotlib.pyplot as plt

# # # Read Excel file (only the relevant columns)
# # df = pd.read_excel(
# #     "support_type_summary.xlsx",
# #     usecols=["date", "Task Force Model", "Warrant Service Officer", "Jail Enforcement Model"]
# # )

# # # Convert date to datetime
# # df["date"] = pd.to_datetime(df["date"])
# # df = df.sort_values("date")

# # # Equal spacing for x-axis positions
# # x_positions = range(len(df))

# # # Create stacked bar chart
# # plt.figure(figsize=(14, 7))

# # # Plot each category stacked
# # plt.bar(
# #     x_positions,
# #     df["Warrant Service Officer"],
# #     label="Warrant Service Officer",
# #     color="#3498DB"
# # )
# # plt.bar(
# #     x_positions,
# #     df["Jail Enforcement Model"],
# #     bottom=df["Warrant Service Officer"],  # stack on top of previous
# #     label="Jail Enforcement Model",
# #     color="#E74C3C"
# # )
# # plt.bar(
# #     x_positions,
# #     df["Task Force Model"],
# #     bottom=df["Warrant Service Officer"] + df["Jail Enforcement Model"],  # stack on top
# #     label="Task Force Model",
# #     color="#2ECC71"
# # )

# # # Titles and labels
# # plt.title("Agreements Over Time (Stacked by Type)", fontsize=16)
# # plt.xlabel("Date", fontsize=12)
# # plt.ylabel("Number of Agreements", fontsize=12)
# # plt.grid(axis="y", alpha=0.3)

# # # X-axis labels with equal spacing
# # plt.xticks(x_positions, df["date"].dt.strftime("%m/%d/%y"), rotation=45)

# # # Add legend
# # plt.legend()

# # # Add value labels for each segment
# # for i in x_positions:
# #     plt.text(
# #         i, df["Warrant Service Officer"][i]/2,
# #         f"{df['Warrant Service Officer'][i]}",
# #         ha="center", va="center", color="white", fontsize=9
# #     )
# #     plt.text(
# #         i, df["Warrant Service Officer"][i] + df["Jail Enforcement Model"][i]/2,
# #         f"{df['Jail Enforcement Model'][i]}",
# #         ha="center", va="center", color="white", fontsize=9
# #     )
# #     plt.text(
# #         i, df["Warrant Service Officer"][i] + df["Jail Enforcement Model"][i] + df["Task Force Model"][i]/2,
# #         f"{df['Task Force Model'][i]}",
# #         ha="center", va="center", color="white", fontsize=9
# #     )

# # # Adjust layout and save figure
# # plt.tight_layout()
# # plt.savefig("agreements_stacked_bar.png", dpi=300, bbox_inches="tight")
# # print("✅ Saved as agreements_stacked_bar.png")

# # import pandas as pd

# # # Read Excel
# # df = pd.read_excel('TOTAL-participatingAgencies08132025am.xlsx')

# # # Keep only the STATE and SUPPORT TYPE columns
# # df_subset = df[['STATE', 'SUPPORT TYPE']]

# # # Save to a new Excel file
# # df_subset.to_excel('state_support_type.xlsx', index=False)
# # print("Columns 'STATE' and 'SUPPORT TYPE' saved as 'state_support_type.xlsx'")

# import pandas as pd

# # Read Excel
# df = pd.read_excel('state_support_type.xlsx')

# df['SUPPORT TYPE']=df['SUPPORT TYPE'].str.strip()

# # Create pivot table counting agreements per state and support type
# summary = df.pivot_table(index='STATE', 
#                          columns='SUPPORT TYPE', 
#                          aggfunc='size', 
#                          fill_value=0)

# # Add row totals per state
# summary['Total'] = summary.sum(axis=1)

# # Add column totals per support type
# summary.loc['Total'] = summary.sum()

# # Reset index to make STATE a column
# summary = summary.reset_index()

# # Save to Excel
# summary.to_excel('graph/agreements_summary_with_totals.xlsx', index=False)
# print("Summary with totals saved as 'agreements_summary_with_totals.xlsx'")

# # Display the table

# import pandas as pd
# import matplotlib.pyplot as plt

# # Read your summary Excel
# df = pd.read_excel('graph/agreements_summary_with_totals.xlsx')

# # Remove trailing spaces in STATE
# df['STATE'] = df['STATE'].str.strip()

# # Drop the 'Total' row if it exists
# df = df[df['STATE'] != 'Total']

# # Drop the 'Total' column if it exists
# if 'Total' in df.columns:
#     df = df.drop(columns=['Total'])

# # Set STATE as index
# df.set_index('STATE', inplace=True)

# # Create stacked bar chart
# ax = df.plot(kind='bar', stacked=True, figsize=(14,7), colormap='tab20')

# # Customize plot
# plt.title('Agreements by State and Model Type', fontsize=16)
# plt.xlabel('State', fontsize=12)
# plt.ylabel('Number of Agreements', fontsize=12)
# plt.xticks(rotation=45, ha='right')
# plt.legend(title='Support Type')
# plt.tight_layout()

# # Save as PNG
# plt.savefig('graph/agreements_by_state_stack.png', dpi=300, bbox_inches='tight')
# print("Plot saved as 'graph/agreements_by_state_stack.png'")


# import pandas as pd
# import matplotlib.pyplot as plt

# # Read the summary
# df = pd.read_excel('graph/agreements_summary_with_totals.xlsx')

# # Clean STATE column
# df['STATE'] = df['STATE'].str.strip()

# # Drop Total row/column
# df = df[df['STATE'] != 'Total']
# if 'Total' in df.columns:
#     df = df.drop(columns=['Total'])

# # Convert numeric columns to integers
# numeric_cols = df.columns.drop('STATE')
# df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

# # Calculate total agreements per state
# df['Total_Agreements'] = df[numeric_cols].sum(axis=1)

# # Sort and pick top 9 states
# df_sorted = df.sort_values('Total_Agreements', ascending=False)
# top9 = df_sorted.head(9)
# others = pd.DataFrame(df_sorted.iloc[9:][numeric_cols].sum()).T
# others['STATE'] = 'Other States'

# # Combine top 9 + others
# plot_df = pd.concat([top9, others], ignore_index=True)
# plot_df.set_index('STATE', inplace=True)
# plot_df = plot_df.drop(columns=['Total_Agreements'])

# # Define shades of blue (dark → medium → light)
# blue_shades = ['#0D47A1', '#1976D2', '#42A5F5']  # dark, medium, light blue

# # Plot stacked bar chart with custom colors
# # ax = plot_df.plot(kind='bar', stacked=True, figsize=(12,7), color=blue_shades)

# # plt.title('Top 9 States + Others: Agreements by Model Type', fontsize=16)
# # plt.xlabel('State', fontsize=12)
# # plt.ylabel('Number of Agreements', fontsize=12)
# # plt.xticks(rotation=45, ha='right')
# # plt.legend(title='Support Type')
# # plt.tight_layout()


# df.plot(kind='bar', stacked=False, figsize=(14,7), colormap='Set2')
# plt.title('Agreements by State and Model Type', fontsize=16)
# plt.xlabel('State', fontsize=12)
# plt.ylabel('Number of Agreements', fontsize=12)
# plt.xticks(rotation=45, ha='right')
# plt.legend(title='Support Type')
# plt.tight_layout()


# # Save as PNG
# plt.savefig('graph/states_agreements_blue.png', dpi=300, bbox_inches='tight')
# print("Plot saved as 'graph/top9_states_agreements_blue.png'")

# import pandas as pd
# import plotly.express as px

# # Read the summary Excel
# df = pd.read_excel('graph/agreements_summary_with_totals.xlsx')

# # Clean STATE column
# df['STATE'] = df['STATE'].str.strip()

# # Drop Total row and column if exists
# df = df[df['STATE'] != 'Total']
# if 'Total' in df.columns:
#     df = df.drop(columns=['Total'])

# # Convert numeric columns to integers
# numeric_cols = df.columns.drop('STATE')
# df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

# # Calculate total agreements per state
# df['Total_Agreements'] = df[numeric_cols].sum(axis=1)

# # Map state names to postal codes (required by Plotly)
# state_codes = {
#     'ALABAMA':'AL','ALASKA':'AK','ARIZONA':'AZ','ARKANSAS':'AR','CALIFORNIA':'CA',
#     'COLORADO':'CO','CONNECTICUT':'CT','DELAWARE':'DE','FLORIDA':'FL','GEORGIA':'GA',
#     'HAWAII':'HI','IDAHO':'ID','ILLINOIS':'IL','INDIANA':'IN','IOWA':'IA','KANSAS':'KS',
#     'KENTUCKY':'KY','LOUISIANA':'LA','MAINE':'ME','MARYLAND':'MD','MASSACHUSETTS':'MA',
#     'MICHIGAN':'MI','MINNESOTA':'MN','MISSISSIPPI':'MS','MISSOURI':'MO','MONTANA':'MT',
#     'NEBRASKA':'NE','NEVADA':'NV','NEW HAMPSHIRE':'NH','NEW JERSEY':'NJ','NEW MEXICO':'NM',
#     'NEW YORK':'NY','NORTH CAROLINA':'NC','NORTH DAKOTA':'ND','OHIO':'OH','OKLAHOMA':'OK',
#     'OREGON':'OR','PENNSYLVANIA':'PA','RHODE ISLAND':'RI','SOUTH CAROLINA':'SC','SOUTH DAKOTA':'SD',
#     'TENNESSEE':'TN','TEXAS':'TX','UTAH':'UT','VERMONT':'VT','VIRGINIA':'VA','WASHINGTON':'WA',
#     'WEST VIRGINIA':'WV','WISCONSIN':'WI','WYOMING':'WY'
# }

# df['State_Code'] = df['STATE'].map(state_codes)

# # Create choropleth map
# fig = px.choropleth(df,
#                     locations='State_Code',
#                     locationmode="USA-states",
#                     color='Total_Agreements',
#                     scope="usa",
#                     color_continuous_scale="Blues",
#                     labels={'Total_Agreements':'Agreements'},
#                     title='Total Agreements per State')

# # Save map as HTML (interactive)
# fig.write_html('graph/agreements_us_map.html')
# print("Interactive U.S. map saved as 'graph/agreements_us_map.html'")

# # If you want a static PNG image:
# fig.write_image('graph/agreements_us_map.png', scale=2)
# print("Static U.S. map saved as 'graph/agreements_us_map.png'")


# import pandas as pd
# import plotly.express as px
# import numpy as np

# # Read your summary Excel
# df = pd.read_excel('graph/agreements_summary_with_totals.xlsx')

# # Clean STATE column and drop totals
# df['STATE'] = df['STATE'].str.strip()
# df = df[df['STATE'] != 'Total']
# if 'Total' in df.columns:
#     df = df.drop(columns=['Total'])

# # Convert numeric columns to int
# numeric_cols = df.columns.drop('STATE')
# df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

# # Calculate total agreements
# df['Total_Agreements'] = df[numeric_cols].sum(axis=1)

# # Map state names to postal codes
# state_codes = { 'ALABAMA':'AL','ALASKA':'AK','ARIZONA':'AZ','ARKANSAS':'AR','CALIFORNIA':'CA',
#                 'COLORADO':'CO','CONNECTICUT':'CT','DELAWARE':'DE','FLORIDA':'FL','GEORGIA':'GA',
#                 'HAWAII':'HI','IDAHO':'ID','ILLINOIS':'IL','INDIANA':'IN','IOWA':'IA','KANSAS':'KS',
#                 'KENTUCKY':'KY','LOUISIANA':'LA','MAINE':'ME','MARYLAND':'MD','MASSACHUSETTS':'MA',
#                 'MICHIGAN':'MI','MINNESOTA':'MN','MISSISSIPPI':'MS','MISSOURI':'MO','MONTANA':'MT',
#                 'NEBRASKA':'NE','NEVADA':'NV','NEW HAMPSHIRE':'NH','NEW JERSEY':'NJ','NEW MEXICO':'NM',
#                 'NEW YORK':'NY','NORTH CAROLINA':'NC','NORTH DAKOTA':'ND','OHIO':'OH','OKLAHOMA':'OK',
#                 'OREGON':'OR','PENNSYLVANIA':'PA','RHODE ISLAND':'RI','SOUTH CAROLINA':'SC','SOUTH DAKOTA':'SD',
#                 'TENNESSEE':'TN','TEXAS':'TX','UTAH':'UT','VERMONT':'VT','VIRGINIA':'VA','WASHINGTON':'WA',
#                 'WEST VIRGINIA':'WV','WISCONSIN':'WI','WYOMING':'WY' }

# df['State_Code'] = df['STATE'].map(state_codes)

# # Create quartile bins
# df['Category'] = pd.qcut(df['Total_Agreements'], 4, labels=['Low','Medium','High','Very High'])

# # Assign custom discrete colors
# color_map = {'Low':'#deebf7', 'Medium':'#9ecae1', 'High':'#3182bd', 'Very High':'#08519c'}

# # Create choropleth with discrete categories
# fig = px.choropleth(df,
#                     locations='State_Code',
#                     locationmode='USA-states',
#                     color='Category',
#                     color_discrete_map=color_map,
#                     scope='usa',
#                     labels={'Category':'Agreements'},
#                     title='Agreements per State (Quartiles)')

# # Save interactive HTML
# fig.write_html('graph/agreements_us_map_quartiles.html')

# # Save static PNG
# fig.write_image('graph/agreements_us_map_quartiles.png', scale=2)

# print("Map saved with quartile-based coloring.")


# import pandas as pd
# import plotly.express as px

# # Read your summary Excel
# df = pd.read_excel('graph/agreements_summary_with_totals.xlsx')

# # Clean STATE column and drop Total row/column
# df['STATE'] = df['STATE'].str.strip()
# df = df[df['STATE'] != 'Total']
# if 'Total' in df.columns:
#     df = df.drop(columns=['Total'])

# # Convert numeric columns to int
# numeric_cols = df.columns.drop('STATE')
# df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

# # Calculate total agreements
# df['Total_Agreements'] = df[numeric_cols].sum(axis=1)

# # Map state names to postal codes
# state_codes = { 'ALABAMA':'AL','ALASKA':'AK','ARIZONA':'AZ','ARKANSAS':'AR','CALIFORNIA':'CA',
#                 'COLORADO':'CO','CONNECTICUT':'CT','DELAWARE':'DE','FLORIDA':'FL','GEORGIA':'GA',
#                 'HAWAII':'HI','IDAHO':'ID','ILLINOIS':'IL','INDIANA':'IN','IOWA':'IA','KANSAS':'KS',
#                 'KENTUCKY':'KY','LOUISIANA':'LA','MAINE':'ME','MARYLAND':'MD','MASSACHUSETTS':'MA',
#                 'MICHIGAN':'MI','MINNESOTA':'MN','MISSISSIPPI':'MS','MISSOURI':'MO','MONTANA':'MT',
#                 'NEBRASKA':'NE','NEVADA':'NV','NEW HAMPSHIRE':'NH','NEW JERSEY':'NJ','NEW MEXICO':'NM',
#                 'NEW YORK':'NY','NORTH CAROLINA':'NC','NORTH DAKOTA':'ND','OHIO':'OH','OKLAHOMA':'OK',
#                 'OREGON':'OR','PENNSYLVANIA':'PA','RHODE ISLAND':'RI','SOUTH CAROLINA':'SC','SOUTH DAKOTA':'SD',
#                 'TENNESSEE':'TN','TEXAS':'TX','UTAH':'UT','VERMONT':'VT','VIRGINIA':'VA','WASHINGTON':'WA',
#                 'WEST VIRGINIA':'WV','WISCONSIN':'WI','WYOMING':'WY' }

# df['State_Code'] = df['STATE'].map(state_codes)

# # Create manual categories
# def categorize(val):
#     if val == 0:
#         return '0'
#     elif 1 <= val <= 9:
#         return '1-9'
#     elif 10 <= val <= 20:
#         return '10-20'
#     elif 21 <= val <= 40:
#         return '21-40'
#     else:  # over 40
#         return '40+'

# df['Category'] = df['Total_Agreements'].apply(categorize)

# # Define custom colors
# color_map = {
#     '0':'#d3d3d3',       # light grey for zero
#     '1-9':'#c6dbef',     # light blue
#     '10-20':'#6baed6',   # medium blue
#     '21-40':'#2171b5',   # dark blue
#     '40+':'#08306b'      # very dark blue
# }

# # Create choropleth
# fig = px.choropleth(df,
#                     locations='State_Code',
#                     locationmode='USA-states',
#                     color='Category',
#                     color_discrete_map=color_map,
#                     scope='usa',
#                     labels={'Category':'Agreements'},
#                     title='Agreements per State (Manual Categories)')

# # Save interactive HTML
# fig.write_html('graph/agreements_us_map_manual.html')

# # Save static PNG
# fig.write_image('graph/agreements_us_map_manual.png', scale=2)

# print("Manual category U.S. map saved with grey for zero states and blue shades for others.")


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read summary Excel
df = pd.read_excel('graph/agreements_summary_with_totals.xlsx')

# Clean STATE column and drop Total row/column
df['STATE'] = df['STATE'].str.strip()
df = df[df['STATE'] != 'Total']
if 'Total' in df.columns:
    df = df.drop(columns=['Total'])

# Convert numeric columns to int
numeric_cols = df.columns.drop('STATE')
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

# Calculate total agreements
df['Total_Agreements'] = df[numeric_cols].sum(axis=1)

# Map state names to postal codes
state_codes = { 'ALABAMA':'AL','ALASKA':'AK','ARIZONA':'AZ','ARKANSAS':'AR','CALIFORNIA':'CA',
                'COLORADO':'CO','CONNECTICUT':'CT','DELAWARE':'DE','FLORIDA':'FL','GEORGIA':'GA',
                'HAWAII':'HI','IDAHO':'ID','ILLINOIS':'IL','INDIANA':'IN','IOWA':'IA','KANSAS':'KS',
                'KENTUCKY':'KY','LOUISIANA':'LA','MAINE':'ME','MARYLAND':'MD','MASSACHUSETTS':'MA',
                'MICHIGAN':'MI','MINNESOTA':'MN','MISSISSIPPI':'MS','MISSOURI':'MO','MONTANA':'MT',
                'NEBRASKA':'NE','NEVADA':'NV','NEW HAMPSHIRE':'NH','NEW JERSEY':'NJ','NEW MEXICO':'NM',
                'NEW YORK':'NY','NORTH CAROLINA':'NC','NORTH DAKOTA':'ND','OHIO':'OH','OKLAHOMA':'OK',
                'OREGON':'OR','PENNSYLVANIA':'PA','RHODE ISLAND':'RI','SOUTH CAROLINA':'SC','SOUTH DAKOTA':'SD',
                'TENNESSEE':'TN','TEXAS':'TX','UTAH':'UT','VERMONT':'VT','VIRGINIA':'VA','WASHINGTON':'WA',
                'WEST VIRGINIA':'WV','WISCONSIN':'WI','WYOMING':'WY' }

df['State_Code'] = df['STATE'].map(state_codes)

# Manual categories for coloring
def categorize(val):
    if val == 0:
        return '0'
    elif 1 <= val <= 9:
        return '1-9'
    elif 10 <= val <= 20:
        return '10-20'
    elif 21 <= val <= 40:
        return '21-40'
    else:
        return '40+'

df['Category'] = df['Total_Agreements'].apply(categorize)

# Custom colors
color_map = {
    '0':'#d3d3d3',
    '1-9':'#c6dbef',
    '10-20':'#6baed6',
    '21-40':'#2171b5',
    '40+':'#08306b'
}

# --- Interactive HTML with exact value on hover ---
fig = px.choropleth(df,
                    locations='State_Code',
                    locationmode="USA-states",
                    color='Category',
                    color_discrete_map=color_map,
                    scope="usa",
                    hover_data={'Total_Agreements':True, 'State_Code':True},
                    title='Agreements per State')

fig.write_html('graph/agreements_us_map_manual_hover.html')

# --- Static PNG with state code and total annotated ---
import plotly.io as pio
fig2 = go.Figure()

# Add choropleth layer
fig2.add_trace(go.Choropleth(
    locations=df['State_Code'],
    z=df['Total_Agreements'],
    locationmode='USA-states',
    colorscale=['#d3d3d3','#c6dbef','#6baed6','#2171b5','#08306b'],
    zmin=0, zmax=df['Total_Agreements'].max(),
    showscale=False
))

# Add text annotations: state code + total
for i, row in df.iterrows():
    fig2.add_trace(go.Scattergeo(
        locations=[row['State_Code']],
        locationmode='USA-states',
        text=f"{row['State_Code']}: {row['Total_Agreements']}",
        mode='text'
    ))

fig2.update_layout(
    title_text='Agreements per State (Manual Categories with Labels)',
    geo_scope='usa',
)

# Save as PNG
pio.write_image(fig2, 'graph/agreements_us_map_manual_labeled.png', scale=2)
print("Static PNG saved with state codes and total agreements.")
