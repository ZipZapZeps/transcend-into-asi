import os
import re
import pandas as pd

# Define input and output paths
input_files = [
    "Articles.md",
    "Books.md",
    "Movies.md",
    "Other.md",
    "Papers.md",
    "Videos-podcasts.md"
]
input_dir = "resources"
output_file = os.path.join(input_dir, "Resources.md")

# Headers to extract
headers = ["Title", "Summary", "Links"]

def parse_markdown_table(file_path):
    """Parse a markdown table from a file and return a DataFrame."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find table using regex
    table_pattern = r'\|.*?\|\n\|[-:\s\|]*\|\n(.*?)(?=\n\n|\Z)'  # Match table until double newline or end
    table_match = re.search(table_pattern, content, re.DOTALL)
    
    if not table_match:
        return pd.DataFrame(columns=headers)

    table_content = table_match.group(1).strip().split('\n')
    
    # Get headers from the table
    table_headers = [h.strip() for h in table_content[0].split('|')[1:-1]]
    
    # Filter only relevant headers
    valid_headers = [h for h in table_headers if h in headers]
    if not valid_headers:
        return pd.DataFrame(columns=headers)
    
    # Create DataFrame
    data = []
    for row in table_content[1:]:
        cols = [c.strip() for c in row.split('|')[1:-1]]
        row_data = {table_headers[i]: cols[i] for i in range(len(cols)) if table_headers[i] in headers}
        data.append(row_data)
    
    df = pd.DataFrame(data, columns=valid_headers)
    
    # Ensure all required headers are present
    for header in headers:
        if header not in df.columns:
            df[header] = ""
    
    return df[headers]

def consolidate_tables():
    """Consolidate tables from all input files into one DataFrame."""
    all_data = pd.DataFrame(columns=headers)
    
    for file_name in input_files:
        file_path = os.path.join(input_dir, file_name)
        if os.path.exists(file_path):
            df = parse_markdown_table(file_path)
            all_data = pd.concat([all_data, df], ignore_index=True)
        else:
            print(f"Warning: {file_path} not found.")
    
    return all_data

def write_markdown_table(df, output_path):
    """Write DataFrame to a markdown table in the output file."""
    # Create output directory if it doesn't exist
    os.makedirs(input_dir, exist_ok=True)
    
    # Write markdown table
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write table header
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        
        # Write table rows
        for _, row in df.iterrows():
            f.write("| " + " | ".join([str(row[h]) for h in headers]) + " |\n")

def main():
    # Consolidate tables
    consolidated_df = consolidate_tables()
    
    # Write to output file
    write_markdown_table(consolidated_df, output_file)
    print(f"Consolidated table written to {output_file}")

if __name__ == "__main__":
    main()