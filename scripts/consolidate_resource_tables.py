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
headers = ["Title", "Summary", "Categories","Link"]

def parse_markdown_table(file_path):
    """Parse a markdown table from a file and return a DataFrame."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find table using regex
    # Extrahiere alle Zeilen, die mit '|' beginnen (Tabellenzeilen)
    lines = [line for line in content.split('\n') if line.strip().startswith('|')]
    if len(lines) < 2:
        return pd.DataFrame(columns=headers)

    # Header ist die erste Zeile, Trennzeile die zweite
    table_headers = [h.strip() for h in lines[0].split('|')[1:-1]]
    valid_headers = [h for h in table_headers if h in headers]
    if not valid_headers:
        return pd.DataFrame(columns=headers)

    # Datenzeilen ab der dritten Zeile
    data = []
    for row in lines[2:]:
        cols = [c.strip() for c in row.split('|')[1:-1]]
        if len(cols) == len(table_headers):
            # Fülle alle Ziel-Header, fehlende werden mit "" ergänzt
            row_data = {}
            for h in headers:
                if h in table_headers:
                    idx = table_headers.index(h)
                    row_data[h] = cols[idx]
                else:
                    row_data[h] = ""
            data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    return df

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