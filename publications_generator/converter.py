import pandas as pd
from jinja2 import Template

# Function to generate the HTML file for combined publications from multiple CSVs
def generate_html_from_csv_files(csv_files):
    all_data = []  # List to hold data from all CSV files

    # Loop through each CSV file and read the data
    for csv_file_path in csv_files:
        try:
            # Load the CSV data into a DataFrame
            # Use 'on_bad_lines' to read and retain rows with issues, and then fill NaN where necessary
            df = pd.read_csv(csv_file_path, encoding='utf-8', on_bad_lines='warn')  # We just warn, not skip
            df = df.apply(pd.to_numeric, errors='ignore')  # Convert columns to numeric, keep errors as NaN
            all_data.append(df)  # Add the DataFrame to the list
        except FileNotFoundError:
            print(f"Error: The file '{csv_file_path}' was not found.")
            continue  # Skip this file and move to the next one
        except pd.errors.ParserError as e:
            print(f"Error parsing '{csv_file_path}': {e}")
            continue  # Skip this file and move to the next one

    if not all_data:
        print("No valid data files found.")
        return

    # Concatenate all data frames into one DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)

    # Sort by year in descending order
    combined_df = combined_df.sort_values(by='Year', ascending=False)

    combined_df['Year'] = pd.to_numeric(combined_df['Year'], errors='coerce')  # Coerce invalid values to NaN

    combined_df = combined_df.dropna(how='all')
    print(combined_df.tail(5))

    combined_df['Year'] = combined_df['Year'].fillna(-1).astype(int)  # Replace NaN with -1 (or any value you prefer) and cast to int

    # Replace NaN in 'Pages' column with an empty string for easy checking in the template
    combined_df['Publication'] = combined_df['Publication'].fillna('')
    combined_df['Pages'] = combined_df['Pages'].fillna('')
    combined_df['Publisher'] = combined_df['Publisher'].fillna('')

    # Remove duplicates based on the 'title' column
    combined_df = combined_df.drop_duplicates(subset='Title', keep='first')

    # Create an HTML template with Jinja2 for the publication list
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Publications</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f4f4f4;
            }
            h1 {
                text-align: center;
            }
            .publication {
                background-color: white;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .title {
                font-size: 18px;
                font-weight: bold;
            }
            .authors {
                font-size: 14px;
                color: #555;
            }
            .details {
                font-size: 12px;
                color: #777;
            }
        </style>
    </head>
    <body>
        <h1>Publications</h1>
        {% for index, row in combined_df.iterrows() %}
        <div class="publication">
            <div class="title">{{ row['Title'] }}</div>
            <div class="authors">Authors: {{ row['Authors'] }}</div>
            <div class="details">
                {% if row['Publication'] %}
                    <p><strong>Publication:</strong> {{ row['Publication'] }}</p>
                {% endif %}
                <p><strong>Year:</strong> {{ row['Year'] }}</p>
                {% if row['Pages'] %}
                    <p><strong>Pages:</strong> {{ row['Pages'] }}</p>
                {% endif %}
                {% if row['Publisher'] %}
                    <p><strong>Publisher:</strong> {{ row['Publisher'] }}</p>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </body>
    </html>
    """

    # Create a Jinja2 Template object
    template = Template(html_template)

    # Render the HTML with the combined data
    html_output = template.render(combined_df=combined_df)

    # Save the combined HTML to a single file
    output_file_path = "combined_publications.html"
    with open(output_file_path, "w", encoding='utf-8') as file:
        file.write(html_output)

    print(f"Combined HTML file created: {output_file_path}")


# Main function to process multiple CSV files
def process_multiple_csv_files(csv_files):
    generate_html_from_csv_files(csv_files)


csv_files = [
    "As. drd. ing. Eugen-Richard Ardelean.csv",
    "As. Drd. Ing. Raluca-Laura Portase.csv",
    "Conf.dr.ing.Camelia Lemnaru.csv",
    "Prof.dr.ing. Mihaela Dinsoreanu.csv",
    "Prof.dr.ing. Rodica Potolea.csv",
]

# Process each CSV file and generate a single combined HTML file
process_multiple_csv_files(csv_files)
