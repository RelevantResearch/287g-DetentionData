# import pandas as pd
# import numpy as np
# from datetime import datetime

# def create_interactive_svg(excel_file='support_type_summary.xlsx'):
#     # Read the Excel file
#     df = pd.read_excel(excel_file)
    
#     # Convert the date column to datetime format
#     df['date'] = pd.to_datetime(df['date'])
    
#     # Sort by date to ensure proper line connection
#     df = df.sort_values('date')
    
#     # SVG dimensions and margins
#     width = 1000
#     height = 600
#     margin = {'top': 50, 'right': 100, 'bottom': 80, 'left': 80}
#     chart_width = width - margin['left'] - margin['right']
#     chart_height = height - margin['top'] - margin['bottom']
    
#     # Data preparation
#     columns = ['Task Force Model', 'Warrant Service Officer', 'Jail Enforcement Model', 'Total']
#     colors = ['#E74C3C', '#3498DB', '#2ECC71', '#9B59B6']
#     markers = ['circle', 'rect', 'polygon', 'circle']
    
#     # Calculate scales
#     max_value = df[columns].max().max()
#     min_value = df[columns].min().min()
#     value_range = max_value - min_value
    
#     # Add some padding to the scale
#     scale_max = max_value + (value_range * 0.1)
#     scale_min = max(0, min_value - (value_range * 0.1))
    
#     # Helper functions
#     def x_scale(index):
#         return margin['left'] + (index / (len(df) - 1)) * chart_width
    
#     def y_scale(value):
#         return margin['top'] + chart_height - ((value - scale_min) / (scale_max - scale_min)) * chart_height
    
#     # Start building SVG
#     svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
# <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
# <defs>
#     <style>
#         .tooltip {{
#             position: absolute;
#             background: rgba(0, 0, 0, 0.8);
#             color: white;
#             padding: 8px 12px;
#             border-radius: 4px;
#             font-family: Arial, sans-serif;
#             font-size: 12px;
#             pointer-events: none;
#             opacity: 0;
#             transition: opacity 0.2s;
#             z-index: 1000;
#         }}
        
#         .line {{
#             fill: none;
#             stroke-width: 2.5;
#         }}
        
#         .marker {{
#             cursor: pointer;
#             transition: r 0.2s, width 0.2s, height 0.2s;
#         }}
        
#         .marker:hover {{
#             stroke-width: 2;
#         }}
        
#         .marker.circle:hover {{
#             r: 6;
#         }}
        
#         .marker.rect:hover {{
#             width: 12;
#             height: 12;
#         }}
        
#         .grid-line {{
#             stroke: #E0E0E0;
#             stroke-width: 0.5;
#         }}
        
#         .axis-line {{
#             stroke: #333;
#             stroke-width: 1;
#         }}
        
#         .axis-text {{
#             font-family: Arial, sans-serif;
#             font-size: 11px;
#             fill: #666;
#         }}
        
#         .title {{
#             font-family: Arial, sans-serif;
#             font-size: 18px;
#             font-weight: bold;
#             fill: #333;
#             text-anchor: middle;
#         }}
        
#         .legend {{
#             font-family: Arial, sans-serif;
#             font-size: 12px;
#             fill: #333;
#         }}
#     </style>
# </defs>

# <!-- Background -->
# <rect width="{width}" height="{height}" fill="white"/>

# <!-- Grid lines -->'''
    
#     # Add horizontal grid lines
#     for i in range(6):
#         y_pos = margin['top'] + (i * chart_height / 5)
#         grid_value = scale_max - (i * (scale_max - scale_min) / 5)
#         svg_content += f'''
# <line x1="{margin['left']}" y1="{y_pos}" x2="{margin['left'] + chart_width}" y2="{y_pos}" class="grid-line"/>
# <text x="{margin['left'] - 10}" y="{y_pos + 4}" class="axis-text" text-anchor="end">{grid_value:.0f}</text>'''
    
#     # Add vertical grid lines and x-axis labels
#     for i, (_, row) in enumerate(df.iterrows()):
#         x_pos = x_scale(i)
#         date_str = row['date'].strftime('%m/%d/%y')
#         svg_content += f'''
# <line x1="{x_pos}" y1="{margin['top']}" x2="{x_pos}" y2="{margin['top'] + chart_height}" class="grid-line"/>
# <text x="{x_pos}" y="{margin['top'] + chart_height + 20}" class="axis-text" text-anchor="middle" transform="rotate(45, {x_pos}, {margin['top'] + chart_height + 20})">{date_str}</text>'''
    
#     # Add axes
#     svg_content += f'''
# <!-- Axes -->
# <line x1="{margin['left']}" y1="{margin['top']}" x2="{margin['left']}" y2="{margin['top'] + chart_height}" class="axis-line"/>
# <line x1="{margin['left']}" y1="{margin['top'] + chart_height}" x2="{margin['left'] + chart_width}" y2="{margin['top'] + chart_height}" class="axis-line"/>

# <!-- Title -->
# <text x="{width/2}" y="30" class="title">Law Enforcement Models Over Time</text>

# <!-- Y-axis label -->
# <text x="20" y="{height/2}" class="axis-text" text-anchor="middle" transform="rotate(-90, 20, {height/2})">Number of Officers/Cases</text>

# <!-- X-axis label -->
# <text x="{width/2}" y="{height - 20}" class="axis-text" text-anchor="middle">Date</text>'''
    
#     # Plot lines and markers for each column
#     for col_idx, column in enumerate(columns):
#         color = colors[col_idx]
        
#         # Create path for line
#         path_data = "M"
#         for i, (_, row) in enumerate(df.iterrows()):
#             x_pos = x_scale(i)
#             y_pos = y_scale(row[column])
#             if i == 0:
#                 path_data += f" {x_pos},{y_pos}"
#             else:
#                 path_data += f" L {x_pos},{y_pos}"
        
#         svg_content += f'''
# <!-- Line for {column} -->
# <path d="{path_data}" class="line" stroke="{color}"/>'''
        
#         # Add markers
#         for i, (_, row) in enumerate(df.iterrows()):
#             x_pos = x_scale(i)
#             y_pos = y_scale(row[column])
#             date_str = row['date'].strftime('%B %d, %Y')
#             value = row[column]
            
#             if markers[col_idx] == 'circle':
#                 svg_content += f'''
# <circle cx="{x_pos}" cy="{y_pos}" r="4" fill="{color}" stroke="white" stroke-width="1" 
#         class="marker circle" 
#         onmousemove="showTooltip(evt, '{column}', '{date_str}', '{value}')"
#         onmouseout="hideTooltip()"/>'''
#             elif markers[col_idx] == 'rect':
#                 svg_content += f'''
# <rect x="{x_pos-4}" y="{y_pos-4}" width="8" height="8" fill="{color}" stroke="white" stroke-width="1" 
#       class="marker rect"
#       onmousemove="showTooltip(evt, '{column}', '{date_str}', '{value}')"
#       onmouseout="hideTooltip()"/>'''
#             elif markers[col_idx] == 'polygon':
#                 # Triangle
#                 points = f"{x_pos},{y_pos-5} {x_pos-4},{y_pos+3} {x_pos+4},{y_pos+3}"
#                 svg_content += f'''
# <polygon points="{points}" fill="{color}" stroke="white" stroke-width="1" 
#          class="marker polygon"
#          onmousemove="showTooltip(evt, '{column}', '{date_str}', '{value}')"
#          onmouseout="hideTooltip()"/>'''
    
#     # Add legend
#     legend_x = width - margin['right'] + 10
#     legend_y = margin['top'] + 20
    
#     svg_content += f'''
# <!-- Legend -->
# <text x="{legend_x}" y="{legend_y - 10}" class="legend" font-weight="bold">Legend</text>'''
    
#     for i, (column, color) in enumerate(zip(columns, colors)):
#         y_pos = legend_y + (i * 25)
#         svg_content += f'''
# <circle cx="{legend_x + 8}" cy="{y_pos}" r="4" fill="{color}" stroke="white" stroke-width="1"/>
# <text x="{legend_x + 20}" y="{y_pos + 4}" class="legend">{column}</text>'''
    
#     # Add JavaScript for tooltips
#     svg_content += '''
# <!-- Tooltip -->
# <g id="tooltip" style="opacity: 0; pointer-events: none;">
#     <rect id="tooltip-bg" x="0" y="0" width="0" height="0" 
#           fill="rgba(0,0,0,0.8)" rx="4" ry="4"/>
#     <text id="tooltip-text" x="0" y="0" 
#           font-family="Arial, sans-serif" font-size="12" fill="white"/>
# </g>

# <script><![CDATA[
# function showTooltip(evt, series, date, value) {
#     var tooltip = document.getElementById('tooltip');
#     var tooltipBg = document.getElementById('tooltip-bg');
#     var tooltipText = document.getElementById('tooltip-text');
    
#     // Set tooltip text
#     var text = series + '\\n' + date + '\\n' + 'Value: ' + value;
    
#     // Clear previous text
#     while (tooltipText.firstChild) {
#         tooltipText.removeChild(tooltipText.firstChild);
#     }
    
#     // Add text lines
#     var lines = text.split('\\n');
#     for (var i = 0; i < lines.length; i++) {
#         var tspan = document.createElementNS('http://www.w3.org/2000/svg', 'tspan');
#         tspan.textContent = lines[i];
#         tspan.setAttribute('x', '8');
#         tspan.setAttribute('dy', i === 0 ? '15' : '15');
#         if (i === 0) tspan.setAttribute('font-weight', 'bold');
#         tooltipText.appendChild(tspan);
#     }
    
#     // Get text dimensions and position tooltip
#     var bbox = tooltipText.getBBox();
#     var padding = 8;
#     var bgWidth = bbox.width + (padding * 2);
#     var bgHeight = bbox.height + (padding * 2);
    
#     // Position tooltip near mouse
#     var pt = evt.target.ownerSVGElement.createSVGPoint();
#     pt.x = evt.clientX;
#     pt.y = evt.clientY;
#     var svgP = pt.matrixTransform(evt.target.ownerSVGElement.getScreenCTM().inverse());
    
#     var x = svgP.x + 10;
#     var y = svgP.y - bgHeight - 10;
    
#     // Keep tooltip in bounds
#     if (x + bgWidth > ''' + str(width) + ''') x = svgP.x - bgWidth - 10;
#     if (y < 0) y = svgP.y + 10;
    
#     tooltipBg.setAttribute('x', x);
#     tooltipBg.setAttribute('y', y);
#     tooltipBg.setAttribute('width', bgWidth);
#     tooltipBg.setAttribute('height', bgHeight);
    
#     tooltipText.setAttribute('x', x);
#     tooltipText.setAttribute('y', y);
    
#     tooltip.setAttribute('style', 'opacity: 1; transition: opacity 0.2s;');
# }

# function hideTooltip() {
#     var tooltip = document.getElementById('tooltip');
#     tooltip.setAttribute('style', 'opacity: 0; transition: opacity 0.2s;');
# }
# ]]></script>

# </svg>'''
    
#     return svg_content

# # Generate the SVG
# svg_content = create_interactive_svg('support_type_summary.xlsx')

# # Save to file
# with open('interactive_chart.svg', 'w', encoding='utf-8') as f:
#     f.write(svg_content)

# print("Interactive SVG created as 'interactive_chart.svg'")
# print("Open this file in a web browser to see the interactive tooltips!")

# # Optional: Also save a simple HTML wrapper for easier viewing
# html_wrapper = f'''<!DOCTYPE html>
# <html>
# <head>
#     <title>Interactive Law Enforcement Chart</title>
#     <style>
#         body {{
#             font-family: Arial, sans-serif;
#             margin: 20px;
#             background-color: #f5f5f5;
#         }}
#         .container {{
#             background: white;
#             padding: 20px;
#             border-radius: 8px;
#             box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#             display: inline-block;
#         }}
#     </style>
# </head>
# <body>
#     <div class="container">
#         {svg_content}
#     </div>
# </body>
# </html>'''

# with open('interactive_chart.html', 'w', encoding='utf-8') as f:
#     f.write(html_wrapper)

# print("HTML version created as 'interactive_chart.html' for easier viewing!")

import pandas as pd
import numpy as np
from datetime import datetime

def create_interactive_svg(excel_file='support_type_summary.xlsx'):
    # Read the Excel file
    df = pd.read_excel(excel_file)
    
    # Convert the date column to datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date to ensure proper line connection
    df = df.sort_values('date')
    
    # SVG dimensions and margins
    width = 1000
    height = 600
    margin = {'top': 50, 'right': 100, 'bottom': 80, 'left': 80}
    chart_width = width - margin['left'] - margin['right']
    chart_height = height - margin['top'] - margin['bottom']
    
    # Data preparation
    columns = ['Task Force Model', 'Warrant Service Officer', 'Jail Enforcement Model', 'Total']
    colors = ['#E74C3C', '#3498DB', '#2ECC71', '#9B59B6']
    markers = ['circle', 'rect', 'polygon', 'circle']
    
    # Calculate scales
    max_value = df[columns].max().max()
    min_value = df[columns].min().min()
    value_range = max_value - min_value
    
    # Add some padding to the scale
    scale_max = max_value + (value_range * 0.1)
    scale_min = max(0, min_value - (value_range * 0.1))
    
    # Helper functions
    def x_scale(index):
        return margin['left'] + (index / (len(df) - 1)) * chart_width
    
    def y_scale(value):
        return margin['top'] + chart_height - ((value - scale_min) / (scale_max - scale_min)) * chart_height
    
    # Start building SVG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<defs>
    <style>
        .tooltip {{
            position: absolute;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-family: Arial, sans-serif;
            font-size: 12px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            z-index: 1000;
        }}
        
        .line {{
            fill: none;
            stroke-width: 2.5;
        }}
        
        .marker {{
            cursor: pointer;
            transition: r 0.2s, width 0.2s, height 0.2s;
        }}
        
        .marker:hover {{
            stroke-width: 2;
        }}
        
        .marker.circle:hover {{
            r: 6;
        }}
        
        .marker.rect:hover {{
            width: 12;
            height: 12;
        }}
        
        .grid-line {{
            stroke: #E0E0E0;
            stroke-width: 0.5;
        }}
        
        .axis-line {{
            stroke: #333;
            stroke-width: 1;
        }}
        
        .axis-text {{
            font-family: Arial, sans-serif;
            font-size: 11px;
            fill: #666;
        }}
        
        .title {{
            font-family: Arial, sans-serif;
            font-size: 18px;
            font-weight: bold;
            fill: #333;
            text-anchor: middle;
        }}
        
        .legend {{
            font-family: Arial, sans-serif;
            font-size: 12px;
            fill: #333;
        }}
    </style>
</defs>

<!-- Background -->
<rect width="{width}" height="{height}" fill="white"/>

<!-- Grid lines -->'''
    
    # Add horizontal grid lines
    for i in range(6):
        y_pos = margin['top'] + (i * chart_height / 5)
        grid_value = scale_max - (i * (scale_max - scale_min) / 5)
        svg_content += f'''
<line x1="{margin['left']}" y1="{y_pos}" x2="{margin['left'] + chart_width}" y2="{y_pos}" class="grid-line"/>
<text x="{margin['left'] - 10}" y="{y_pos + 4}" class="axis-text" text-anchor="end">{grid_value:.0f}</text>'''
    
    # Add vertical grid lines and x-axis labels
    for i, (_, row) in enumerate(df.iterrows()):
        x_pos = x_scale(i)
        date_str = row['date'].strftime('%m/%d/%y')
        svg_content += f'''
<line x1="{x_pos}" y1="{margin['top']}" x2="{x_pos}" y2="{margin['top'] + chart_height}" class="grid-line"/>
<text x="{x_pos}" y="{margin['top'] + chart_height + 20}" class="axis-text" text-anchor="middle" transform="rotate(45, {x_pos}, {margin['top'] + chart_height + 20})">{date_str}</text>'''
    
    # Add axes
    svg_content += f'''
<!-- Axes -->
<line x1="{margin['left']}" y1="{margin['top']}" x2="{margin['left']}" y2="{margin['top'] + chart_height}" class="axis-line"/>
<line x1="{margin['left']}" y1="{margin['top'] + chart_height}" x2="{margin['left'] + chart_width}" y2="{margin['top'] + chart_height}" class="axis-line"/>

<!-- Title -->
<text x="{width/2}" y="30" class="title">Law Enforcement Models Over Time</text>

<!-- Y-axis label -->
<text x="20" y="{height/2}" class="axis-text" text-anchor="middle" transform="rotate(-90, 20, {height/2})">Number of Officers/Cases</text>

<!-- X-axis label -->
<text x="{width/2}" y="{height - 20}" class="axis-text" text-anchor="middle">Date</text>'''
    
    # Plot lines and markers for each column
    for col_idx, column in enumerate(columns):
        color = colors[col_idx]
        
        # Create path for line
        path_data = "M"
        for i, (_, row) in enumerate(df.iterrows()):
            x_pos = x_scale(i)
            y_pos = y_scale(row[column])
            if i == 0:
                path_data += f" {x_pos},{y_pos}"
            else:
                path_data += f" L {x_pos},{y_pos}"
        
        svg_content += f'''
<!-- Line for {column} -->
<path d="{path_data}" class="line" stroke="{color}"/>'''
        
        # Add markers
        for i, (_, row) in enumerate(df.iterrows()):
            x_pos = x_scale(i)
            y_pos = y_scale(row[column])
            date_str = row['date'].strftime('%B %d, %Y')
            value = row[column]
            
            # Properly escape data for JavaScript
            column_escaped = str(column).replace("'", "\\'").replace('"', '\\"')
            date_escaped = str(date_str).replace("'", "\\'").replace('"', '\\"')
            value_escaped = str(value).replace("'", "\\'").replace('"', '\\"')
            
            # Create data attributes for more reliable data passing
            data_attrs = f'data-series="{column_escaped}" data-date="{date_escaped}" data-value="{value_escaped}"'
            
            if markers[col_idx] == 'circle':
                svg_content += f'''
<circle cx="{x_pos}" cy="{y_pos}" r="4" fill="{color}" stroke="white" stroke-width="1" 
        class="marker circle" {data_attrs}
        onmousemove="showTooltipFromData(evt)"
        onmouseout="hideTooltip()"/>'''
            elif markers[col_idx] == 'rect':
                svg_content += f'''
<rect x="{x_pos-4}" y="{y_pos-4}" width="8" height="8" fill="{color}" stroke="white" stroke-width="1" 
      class="marker rect" {data_attrs}
      onmousemove="showTooltipFromData(evt)"
      onmouseout="hideTooltip()"/>'''
            elif markers[col_idx] == 'polygon':
                # Triangle
                points = f"{x_pos},{y_pos-5} {x_pos-4},{y_pos+3} {x_pos+4},{y_pos+3}"
                svg_content += f'''
<polygon points="{points}" fill="{color}" stroke="white" stroke-width="1" 
         class="marker polygon" {data_attrs}
         onmousemove="showTooltipFromData(evt)"
         onmouseout="hideTooltip()"/>'''
    
    # Add legend
    legend_x = width - margin['right'] + 10
    legend_y = margin['top'] + 20
    
    svg_content += f'''
<!-- Legend -->
<text x="{legend_x}" y="{legend_y - 10}" class="legend" font-weight="bold">Legend</text>'''
    
    for i, (column, color) in enumerate(zip(columns, colors)):
        y_pos = legend_y + (i * 25)
        svg_content += f'''
<circle cx="{legend_x + 8}" cy="{y_pos}" r="4" fill="{color}" stroke="white" stroke-width="1"/>
<text x="{legend_x + 20}" y="{y_pos + 4}" class="legend">{column}</text>'''
    
    # Add JavaScript for tooltips - FIXED VERSION
    svg_content += '''
<!-- Tooltip -->
<g id="tooltip" style="opacity: 0; pointer-events: none;">
    <rect id="tooltip-bg" x="0" y="0" width="0" height="0" 
          fill="rgba(0,0,0,0.8)" rx="4" ry="4"/>
    <text id="tooltip-text" x="0" y="0" 
          font-family="Arial, sans-serif" font-size="12" fill="white"/>
</g>

<script><![CDATA[
function showTooltipFromData(evt) {
    var element = evt.target;
    var series = element.getAttribute('data-series');
    var date = element.getAttribute('data-date');
    var value = element.getAttribute('data-value');
    
    if (!series || !date || !value) {
        console.log('Missing tooltip data:', {series, date, value});
        return;
    }
    
    showTooltip(evt, series, date, value);
}

function showTooltip(evt, series, date, value) {
    var tooltip = document.getElementById('tooltip');
    var tooltipBg = document.getElementById('tooltip-bg');
    var tooltipText = document.getElementById('tooltip-text');
    
    if (!tooltip || !tooltipBg || !tooltipText) {
        console.log('Tooltip elements not found');
        return;
    }
    
    // Set tooltip text
    var text = series + '\\n' + date + '\\n' + 'Value: ' + value;
    
    // Clear previous text
    while (tooltipText.firstChild) {
        tooltipText.removeChild(tooltipText.firstChild);
    }
    
    // Get mouse position first (before adding text)
    try {
        var rect = evt.target.ownerSVGElement.getBoundingClientRect();
        var x = evt.clientX - rect.left + 10;
        var y = evt.clientY - rect.top - 10;
        
        // Fallback positioning if clientX/clientY not available
        if (!evt.clientX) {
            // Use element position as fallback
            if (evt.target.cx) {
                x = parseFloat(evt.target.cx.baseVal.value) + 10;
                y = parseFloat(evt.target.cy.baseVal.value) - 10;
            } else if (evt.target.x) {
                x = parseFloat(evt.target.x.baseVal.value) + 10;
                y = parseFloat(evt.target.y.baseVal.value) - 10;
            } else {
                x = 100; y = 100; // Default fallback
            }
        }
    } catch(e) {
        console.log('Error getting position:', e);
        x = 100; y = 100; // Fallback position
    }
    
    // Calculate initial position
    var padding = 8;
    
    // Set initial position for text element
    tooltipText.setAttribute('x', x + padding);
    tooltipText.setAttribute('y', y + padding);
    
    // Add text lines with correct positioning
    var lines = text.split('\\n');
    for (var i = 0; i < lines.length; i++) {
        var tspan = document.createElementNS('http://www.w3.org/2000/svg', 'tspan');
        tspan.textContent = lines[i];
        tspan.setAttribute('x', x + padding);  // Position relative to tooltip position
        tspan.setAttribute('dy', i === 0 ? '15' : '15');
        if (i === 0) tspan.setAttribute('font-weight', 'bold');
        tooltipText.appendChild(tspan);
    }
    
    // Get text dimensions and adjust background
    try {
        var bbox = tooltipText.getBBox();
        var bgWidth = bbox.width + (padding * 2);
        var bgHeight = bbox.height + (padding * 2);
        
        // Adjust position to keep tooltip in bounds
        if (x + bgWidth > ''' + str(width) + ''') x = Math.max(0, x - bgWidth - 20);
        if (y - bgHeight < 0) y = y + bgHeight + 20;
        
        // Update positions if they changed
        tooltipText.setAttribute('x', x + padding);
        tooltipText.setAttribute('y', y - bgHeight + padding + 15);
        
        // Update all tspan positions
        var tspans = tooltipText.getElementsByTagName('tspan');
        for (var i = 0; i < tspans.length; i++) {
            tspans[i].setAttribute('x', x + padding);
        }
        
        // Set background position and size
        tooltipBg.setAttribute('x', bbox.x - padding);
        tooltipBg.setAttribute('y', bbox.y - padding);
        tooltipBg.setAttribute('width', bgWidth);
        tooltipBg.setAttribute('height', bgHeight);
        
    } catch(e) {
        console.log('Error setting tooltip dimensions:', e);
        // Fallback dimensions
        tooltipBg.setAttribute('x', x);
        tooltipBg.setAttribute('y', y - 50);
        tooltipBg.setAttribute('width', 150);
        tooltipBg.setAttribute('height', 50);
    }
    
    tooltip.setAttribute('style', 'opacity: 1; transition: opacity 0.2s;');
}

function hideTooltip() {
    var tooltip = document.getElementById('tooltip');
    if (tooltip) {
        tooltip.setAttribute('style', 'opacity: 0; transition: opacity 0.2s;');
    }
}
]]></script>

</svg>'''
    
    return svg_content

# Generate the SVG
svg_content = create_interactive_svg('support_type_summary.xlsx')

# Save to file
with open('interactive_chart.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("Interactive SVG created as 'interactive_chart.svg'")
print("Open this file in a web browser to see the interactive tooltips!")

# Optional: Also save a simple HTML wrapper for easier viewing
html_wrapper = f'''<!DOCTYPE html>
<html>
<head>
    <title>Interactive Law Enforcement Chart</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: inline-block;
        }}
    </style>
</head>
<body>
    <div class="container">
        {svg_content}
    </div>
</body>
</html>'''

with open('interactive_chart.html', 'w', encoding='utf-8') as f:
    f.write(html_wrapper)

print("HTML version created as 'interactive_chart.html' for easier viewing!")