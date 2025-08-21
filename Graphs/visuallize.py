# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime
# import matplotlib.dates as mdates

# # Read the Excel file
# df = pd.read_excel('summary.xlsx')

# # Convert the date column to datetime format
# df['Date'] = pd.to_datetime(df['Date'])

# # Sort by date to ensure proper line connection
# df = df.sort_values('Date')

# # Create the line graph with fixed spacing (ignoring actual date gaps)
# plt.figure(figsize=(10, 6))
# # Use range/index for x-axis to create equal spacing with subtle colors
# x_positions = range(len(df))
# plt.plot(x_positions, df['Total'], marker='o', linewidth=2, markersize=6, 
#          color='#3498DB', markerfacecolor='#E74C3C', markeredgecolor='#3498DB')

# # Customize the plot with subtle colors
# plt.title('Total Agreement Over Time', fontsize=16)
# plt.xlabel('Date', fontsize=12)
# plt.ylabel('Total Agreement', fontsize=12)
# plt.grid(True, alpha=0.3)

# # Set x-axis labels to show actual dates with equal spacing
# plt.xticks(range(len(df)), df['Date'].dt.strftime('%m/%d/%y'), rotation=45)

# # Add value labels on data points with simple styling
# for i, value in enumerate(df['Total']):
#     plt.annotate(f'{value}', (i, value), textcoords="offset points", 
#                 xytext=(0,10), ha='center', fontsize=9)

# # Adjust layout to prevent label cutoff
# plt.tight_layout()

# # Save the plot (since plt.show() doesn't work in non-interactive environments)
# plt.savefig('final/summary_line_graph.png', dpi=300, bbox_inches='tight')


import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read the Excel file
df = pd.read_excel('summary.xlsx')

# Convert the date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')
x_positions = range(len(df))

# Define models and corresponding colors
models = {
    'Task Force Model': '#0D3B66',          # Dark blue
    'Warrant Service Officer': '#1E6091',   # Medium blue
    'Jail Enforcement Model': '#4B9CD3'     # Light blue
}

# Loop over each model
for model_name, color in models.items():
    for show_labels in [True, False]:
        plt.figure(figsize=(10, 6))
        plt.plot(x_positions, df[model_name], marker='o', linewidth=2, markersize=6,
                 color=color, markerfacecolor=color, markeredgecolor=color)
        
        # Force y-axis to start at 0
        plt.ylim(bottom=0)
        
        # Remove left/right padding
        plt.xlim(left=min(x_positions), right=max(x_positions))
        plt.margins(x=0)
        
        # Set x-axis labels
        plt.xticks(x_positions, df['Date'].dt.strftime('%m/%d/%y'), rotation=45)
        
        # Add value labels if required
        if show_labels:
            for i in x_positions:
                plt.annotate(f"{df[model_name][i]}", (i, df[model_name][i]),
                             xytext=(0, 8), textcoords="offset points", ha='center', fontsize=9)
        
        # Customize plot
        plt.title(f'{model_name} Over Time', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Number of Agreements', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Save the plot
        label_suffix = 'with_labels' if show_labels else 'without_labels'
        file_name = f'final/{model_name.replace(" ", "_").lower()}_{label_suffix}.png'
        plt.tight_layout()
        plt.savefig(file_name, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Graph saved as '{file_name}'")
