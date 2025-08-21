
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import glob
import re
import os
from collections import defaultdict

def parse_filename_date(filename):
    """
    Extract date from filename. Handles multiple formats:
    - participatingAgencies-20250409011417.xlsx -> 2025-04-09
    - participatingAgencies03062025am.xlsx -> 2025-03-06
    """
    basename = os.path.basename(filename)
    
    # Pattern 1: YYYYMMDDHHMMSS format
    pattern1 = r'participatingAgencies-(\d{8})\d{6}\.xlsx'
    match1 = re.search(pattern1, basename)
    if match1:
        date_str = match1.group(1)
        return datetime.strptime(date_str, '%Y%m%d').date()
    
    # Pattern 2: MMDDYYYY format
    pattern2 = r'participatingAgencies(\d{8})[ap]m\.xlsx'
    match2 = re.search(pattern2, basename)
    if match2:
        date_str = match2.group(1)
        # Convert MMDDYYYY to YYYYMMDD
        month = date_str[:2]
        day = date_str[2:4]
        year = date_str[4:8]
        return datetime.strptime(f'{year}{month}{day}', '%Y%m%d').date()
    
    return None

def read_and_analyze_file(filepath):
    """
    Read Excel file and count agreements by support type
    """
    try:
        df = pd.read_excel(filepath)
        df.columns = df.columns.str.strip()
        
        support_col = None
        for col in df.columns:
            if 'SUPPORT' in col.upper() and 'TYPE' in col.upper():
                support_col = col
                break
        
        if support_col is None:
            print(f"Warning: Could not find SUPPORT TYPE column in {filepath}")
            return {}
        
        support_counts = df[support_col].value_counts().to_dict()
        
        normalized_counts = {}
        for support_type, count in support_counts.items():
            if pd.isna(support_type):
                continue
            
            support_type_clean = str(support_type).strip()
            
            if 'Task Force Model' in support_type_clean:
                if 'Warrant Service Officer' in support_type_clean:
                    normalized_counts['Warrant Service Officer'] = count
                else:
                    normalized_counts['Task Force Model'] = count
            elif 'Jail' in support_type_clean and 'Model' in support_type_clean:
                normalized_counts['Jail Enforcement Model'] = count
            else:
                normalized_counts[support_type_clean] = count
        
        return normalized_counts
        
    except Exception as e:
        print(f"Error reading {filepath}: {str(e)}")
        return {}

def create_pie_chart(df_plot, main_types, output_folder):
    totals = {t: df_plot[t].sum() for t in main_types}
    filtered_totals = {k: v for k, v in totals.items() if v > 0}
    
    if not filtered_totals:
        print("No data available for pie chart")
        return
    
    plt.figure(figsize=(10, 8))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    wedges, texts, autotexts = plt.pie(
        filtered_totals.values(), 
        labels=filtered_totals.keys(),
        autopct='%1.1f%%',
        startangle=90,
        colors=colors[:len(filtered_totals)],
        explode=[0.05] * len(filtered_totals)
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('bold')
    
    plt.title('Total 287G Agreements Distribution by Support Type\n(January 1, 2025 - Present)', 
              fontsize=16, fontweight='bold', pad=20)
    
    total_agreements = sum(filtered_totals.values())
    plt.text(0, 0, f'Total\n{total_agreements}\nAgreements', 
             ha='center', va='center', fontsize=14, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    plt.axis('equal')
    plt.tight_layout()
    pie_chart_path = os.path.join(output_folder, '287g_agreements_pie_chart.png')
    plt.savefig(pie_chart_path, dpi=300, bbox_inches='tight')
    plt.show()

def create_bar_chart(df_plot, main_types, output_folder):
    totals = {t: df_plot[t].sum() for t in main_types}
    filtered_totals = {k: v for k, v in totals.items() if v > 0}
    
    if not filtered_totals:
        print("No data available for bar chart")
        return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    bars1 = ax1.bar(filtered_totals.keys(), filtered_totals.values(), 
                    color=colors[:len(filtered_totals)], alpha=0.8, edgecolor='black', linewidth=1)
    
    ax1.set_title('Total 287G Agreements by Support Type\n(January 1, 2025 - Present)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylabel('Total Number of Agreements', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    ax1.tick_params(axis='x', rotation=15)
    
    dates = df_plot['Date']
    bottoms = [0] * len(dates)
    
    for i, support_type in enumerate(main_types):
        if support_type in filtered_totals:
            ax2.bar(dates, df_plot[support_type], bottom=bottoms, 
                    label=support_type, color=colors[i], alpha=0.8, edgecolor='black', linewidth=0.5)
            for j in range(len(bottoms)):
                bottoms[j] += df_plot[support_type].iloc[j]
    
    ax2.set_title('287G Agreements Over Time (Stacked by Support Type)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Number of Agreements', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    bar_chart_path = os.path.join(output_folder, '287g_agreements_bar_chart.png')
    plt.savefig(bar_chart_path, dpi=300, bbox_inches='tight')
    plt.show()

def main():
    folder_path = "participatingAgencies after feb 20"
    output_folder = "output_charts"
    os.makedirs(output_folder, exist_ok=True)

    file_pattern = os.path.join(folder_path, "*.xlsx")
    files = glob.glob(file_pattern)
    
    if not files:
        print(f"No Excel files found in {folder_path}")
        return
    
    cutoff_date = datetime(2025, 1, 1).date()
    data_by_date = defaultdict(lambda: defaultdict(int))
    processed_files = []
    
    for file in files:
        file_date = parse_filename_date(file)
        if file_date is None:
            print(f"Could not parse date from filename: {file}")
            continue
        if file_date < cutoff_date:
            continue
        print(f"Processing {file} (Date: {file_date})")
        support_counts = read_and_analyze_file(file)
        if support_counts:
            for support_type, count in support_counts.items():
                data_by_date[file_date][support_type] += count
            processed_files.append((file, file_date))
    
    if not data_by_date:
        print("No data found for the specified date range")
        return
    
    dates = sorted(data_by_date.keys())
    main_types = ['Task Force Model', 'Jail Enforcement Model', 'Warrant Service Officer']
    
    plot_data = {
        'Date': [],
        'Task Force Model': [],
        'Jail Enforcement Model': [],
        'Warrant Service Officer': []
    }
    
    for date in dates:
        plot_data['Date'].append(date)
        for support_type in main_types:
            plot_data[support_type].append(data_by_date[date][support_type])
    
    df_plot = pd.DataFrame(plot_data)
    
    print(f"\nProcessed {len(processed_files)} files")
    print(f"Date range: {min(dates)} to {max(dates)}")
    print("\nSummary by support type:")
    for support_type in main_types:
        print(f"  {support_type}: {df_plot[support_type].sum()}")
    
    plt.figure(figsize=(14, 8))
    sns.set_style("whitegrid")
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for i, support_type in enumerate(main_types):
        plt.plot(df_plot['Date'], df_plot[support_type], 
                 marker='o', linewidth=2.5, markersize=6,
                 label=support_type, color=colors[i])
    
    plt.title('287G Agreements Over Time by Support Type\n(January 1, 2025 - Present)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Date', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Agreements', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    timeline_path = os.path.join(output_folder, '287g_agreements_timeline.png')
    csv_path = os.path.join(output_folder, '287g_agreements_data.csv')

    plt.savefig(timeline_path, dpi=300, bbox_inches='tight')
    plt.show()

    df_plot.to_csv(csv_path, index=False)

    print(f"\nPlot saved as '{timeline_path}'")
    print(f"Data saved as '{csv_path}'")
    
    create_pie_chart(df_plot, main_types, output_folder)
    create_bar_chart(df_plot, main_types, output_folder)


if __name__ == "__main__":
    main()
