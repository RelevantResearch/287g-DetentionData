# # import pandas as pd
# # import matplotlib.pyplot as plt
# # from datetime import datetime

# # # Read the Excel file
# # df = pd.read_excel('support_type_summary.xlsx')

# # # Convert the date column to datetime format
# # df['Date'] = pd.to_datetime(df['Date'])

# # # Sort by date to ensure proper line connection
# # df = df.sort_values('Date')

# # # Create the line graph with fixed spacing
# # plt.figure(figsize=(12, 7))

# # # Use range/index for x-axis to create equal spacing
# # x_positions = range(len(df))

# # # Plot each column as a separate line (excluding 'Total')
# # plt.plot(x_positions, df['Task Force Model'], marker='o', linewidth=2, markersize=6, 
# #          label='Task Force Model', color='#E74C3C')
# # plt.plot(x_positions, df['Warrant Service Officer'], marker='s', linewidth=2, markersize=6, 
# #          label='Warrant Service Officer', color='#3498DB')
# # plt.plot(x_positions, df['Jail Enforcement Model'], marker='^', linewidth=2, markersize=6, 
# #          label='Jail Enforcement Model', color='#2ECC71')

# # # Customize the plot
# # plt.title('Law Enforcement Models Over Time', fontsize=16)
# # plt.xlabel('Date', fontsize=12)
# # plt.ylabel('Number of Agreements', fontsize=12)
# # plt.grid(True, alpha=0.3)

# # # Set y-axis to start from 0
# # plt.ylim(bottom=0)

# # # Set x-axis labels to show actual dates with equal spacing
# # plt.xticks(range(len(df)), df['Date'].dt.strftime('%m/%d/%y'), rotation=45)

# # # Add legend
# # plt.legend(loc='upper left', frameon=True, shadow=True)

# # # Adjust layout to prevent label cutoff
# # plt.tight_layout()

# # # Save the plot
# # plt.savefig('graph/support_summary_line_graph.png', dpi=300, bbox_inches='tight')
# # print("Graph saved as 'support_summary_line_graph.png'")

# # # For interactive display:
# # # plt.show()

# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # # from datetime import datetime

# # # # Read the Excel file
# # # df = pd.read_excel('support_type_summary.xlsx')

# # # # Convert the date column to datetime format
# # # df['Date'] = pd.to_datetime(df['Date'])

# # # # Sort by date to ensure proper line connection
# # # df = df.sort_values('Date')

# # # # Create the line graph
# # # plt.figure(figsize=(12, 7))

# # # # Use range/index for x-axis to create equal spacing
# # # x_positions = range(len(df))

# # # # Plot only Task Force Model
# # # plt.plot(x_positions, df['Task Force Model'], marker='o', linewidth=2, markersize=6, 
# # #          label='Task Force Model', color='#E74C3C')

# # # # Customize the plot
# # # plt.title('Task Force Model Over Time', fontsize=16)
# # # plt.xlabel('Date', fontsize=12)
# # # plt.ylabel('Number of Officers/Cases', fontsize=12)
# # # plt.grid(True, alpha=0.3)

# # # # Set y-axis to start from 0
# # # plt.ylim(bottom=0)

# # # # Set x-axis labels to show actual dates with equal spacing
# # # plt.xticks(range(len(df)), df['Date'].dt.strftime('%m/%d/%y'), rotation=45)

# # # # Add legend
# # # plt.legend(loc='upper left', frameon=True, shadow=True)

# # # # Add value labels on data points
# # # for i, value in enumerate(df['Task Force Model']):
# # #     plt.annotate(f'{value}', (i, value), textcoords="offset points", 
# # #                  xytext=(0,10), ha='center', fontsize=9)

# # # # Adjust layout to prevent label cutoff
# # # plt.tight_layout()

# # # # Save the plot
# # # plt.savefig('graph/task_force_model_graph.png', dpi=300, bbox_inches='tight')
# # # print("Graph saved as 'task_force_model_graph.png'")

# # # # For interactive display:
# # # # plt.show()

# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime

# # Read the Excel file
# df = pd.read_excel('summary.xlsx')

# # Convert the date column to datetime format
# df['Date'] = pd.to_datetime(df['Date'])

# # Sort by date to ensure proper line connection
# df = df.sort_values('Date')

# # Create the line graph with fixed spacing
# plt.figure(figsize=(12, 7))

# # Use range/index for x-axis to create equal spacing
# x_positions = range(len(df))

# # Define blue shades from dark to medium
# colors = ['#0D3B66', '#1E6091', '#4B9CD3']  # Dark blue, medium-dark blue, medium blue

# # Plot each column as a separate line with blue shades
# plt.plot(x_positions, df['Task Force Model'], marker='o', linewidth=2, markersize=6, 
#          label='Task Force Model', color=colors[0])
# plt.plot(x_positions, df['Warrant Service Officer'], marker='s', linewidth=2, markersize=6, 
#          label='Warrant Service Officer', color=colors[1])
# plt.plot(x_positions, df['Jail Enforcement Model'], marker='^', linewidth=2, markersize=6, 
#          label='Jail Enforcement Model', color=colors[2])

# # Customize the plot
# plt.title('Law Enforcement Models Over Time', fontsize=16)
# plt.xlabel('Date', fontsize=12)
# plt.ylabel('Number of Agreements', fontsize=12)
# plt.grid(True, alpha=0.3)

# # Set y-axis to start from 0
# plt.ylim(bottom=0)

# # Set x-axis labels to show actual dates with equal spacing
# plt.xticks(range(len(df)), df['Date'].dt.strftime('%m/%d/%y'), rotation=45)

# # Add legend
# plt.legend(loc='upper left', frameon=True, shadow=True)

# # Adjust layout to prevent label cutoff
# plt.tight_layout()

# # Save the plot
# plt.savefig('final/support_summary_line_graph.png', dpi=300, bbox_inches='tight')
# print("Graph saved as 'support_summary_line_graph.png'")

# # For interactive display:
# # plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read the Excel file
df = pd.read_excel('summary.xlsx')

# Convert the date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Sort by date
df = df.sort_values('Date')

# Create the plot
fig, ax = plt.subplots(figsize=(12, 7))

# Use range/index for x-axis to create equal spacing
x_positions = range(len(df))

# Define blue shades from dark to medium
colors = ['#0D3B66', '#1E6091', '#4B9CD3']

# Plot lines
ax.plot(x_positions, df['Task Force Model'], marker='o', linewidth=2, markersize=6,
        label='Task Force Model', color=colors[0])
ax.plot(x_positions, df['Warrant Service Officer'], marker='s', linewidth=2, markersize=6,
        label='Warrant Service Officer', color=colors[1])
ax.plot(x_positions, df['Jail Enforcement Model'], marker='^', linewidth=2, markersize=6,
        label='Jail Enforcement Model', color=colors[2])

# Force y-axis to start at 0
ax.set_ylim(bottom=0)

# Remove left and right padding on x-axis
ax.set_xlim(left=min(x_positions), right=max(x_positions))

# Optional: remove automatic margins entirely
ax.margins(x=0)

# Customize x-axis labels
ax.set_xticks(x_positions)
ax.set_xticklabels(df['Date'].dt.strftime('%m/%d/%y'), rotation=45)

# Customize plot
ax.set_title('Law Enforcement Models Over Time', fontsize=16)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Number of Agreements', fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left', frameon=True, shadow=True)

plt.tight_layout()

# Save the plot
plt.savefig('final/support_summary_line_graph.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'support_summary_line_graph.png'")
