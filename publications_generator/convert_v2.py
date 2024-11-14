import pandas as pd
from jinja2 import Template

def combine_csv_files(csv_files, output_file="./all_articles.csv"):
    # Read and concatenate all CSV files into a single DataFrame
    dataframes = [pd.read_csv(f) for f in csv_files]
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Sort by the number of non-null values in each row (descending)
    combined_df['non_null_count'] = combined_df.notna().sum(axis=1)

    # Sort by 'Title' and keep the row with the most non-null values
    combined_df.sort_values(['Title', 'non_null_count'], ascending=[True, False], inplace=True)

    # Drop duplicates based on 'Title', keeping the row with the most non-null values
    combined_df = combined_df.drop_duplicates(subset='Title', keep='first')

    # Remove the helper column used for counting non-null values
    combined_df.drop(columns=['non_null_count'], inplace=True)

    # Sort by year in descending order
    combined_df = combined_df.sort_values(by='Year', ascending=False)

    # Write the cleaned DataFrame to the output CSV file
    combined_df.to_csv(output_file, index=False)

    print(f"Combined file saved as {output_file}")

    return combined_df


def generate_html_from_csv_files(csv_files):

    combined_df = combine_csv_files(csv_files)

    combined_df['Year'] = pd.to_numeric(combined_df['Year'], errors='coerce')  # Coerce invalid values to NaN

    combined_df = combined_df.dropna(how='all')
    print(combined_df.tail(5))

    combined_df['Year'] = combined_df['Year'].fillna(-1).astype(int)  # Replace NaN with -1 (or any value you prefer) and cast to int

    # Replace NaN in 'Pages' column with an empty string for easy checking in the template
    combined_df['Publication'] = combined_df['Publication'].fillna('')
    combined_df['Pages'] = combined_df['Pages'].fillna('')
    combined_df['Publisher'] = combined_df['Publisher'].fillna('')
    combined_df['Link'] = combined_df['Link'].fillna('')
    combined_df['Highlight'] = combined_df['Highlight'].fillna('')  # Ensure 'Highlight' column is properly handled

    # Remove duplicates based on the 'Title' column
    combined_df = combined_df.drop_duplicates(subset='Title', keep='first')

    # Separate highlighted publications from the rest
    highlighted_df = combined_df[combined_df['Highlight'] != '']
    print(highlighted_df)
    other_df = combined_df[combined_df['Highlight'] == '']

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
            .highlighted-publication {
                background-color: #fef7e3;
                border-left: 5px solid #ffb300;
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
            .simpler-publication {
                margin-bottom: 10px;
                padding-left: 15px;
            }
        </style>
    </head>
    <body>
        <h1>Publications</h1>

        <!-- Highlighted Publications -->
        <section>
            <h2>Highlighted Publications</h2>
            {% for index, row in highlighted_df.iterrows() %}
            <div class="highlighted-publication">
                <div class="title">
                    {% if row['Link'] %}
                        <a href="{{ row['Link'] }}" target="_blank">{{ row['Title'] }}</a>
                    {% else %}
                        {{ row['Title'] }}
                    {% endif %}
                </div>
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
        </section>

        <!-- Other Publications -->
        <section>
            <h2>Other Publications</h2>
            {% for index, row in other_df.iterrows() %}
            <div class="simpler-publication">
                <div class="title">
                    {% if row['Link'] %}
                        <a href="{{ row['Link'] }}" target="_blank">{{ row['Title'] }}</a>
                    {% else %}
                        {{ row['Title'] }}
                    {% endif %}
                </div>
                <div class="authors">Authors: {{ row['Authors'] }}</div>
                <div class="details">
                    <span>Year: {{ row['Year'] }}</span>
                    {% if row['Pages'] %}
                        <span>Pages:{{ row['Pages'] }}</span>
                    {% endif %}
                    {% if row['Publisher'] %}
                        <span>Publisher: {{ row['Publisher'] }}</span>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </section>

    </body>
    </html>
    """

    # Create a Jinja2 Template object
    template = Template(html_template)

    # Render the HTML with the combined data
    html_output = template.render(highlighted_df=highlighted_df, other_df=combined_df)

    # Save the combined HTML to a single file
    output_file_path = "combined_publications.html"
    with open(output_file_path, "w", encoding='utf-8') as file:
        file.write(html_output)

    print(f"Combined HTML file created: {output_file_path}")



csv_files = [
    "As. drd. ing. Eugen-Richard Ardelean.csv",
    "As. Drd. Ing. Raluca-Laura Portase.csv",
    "As. Drd. Ing. Vlad Andrei Negru.csv",
    "Conf.dr.ing.Camelia Lemnaru.csv",
    "Prof.dr.ing. Mihaela Dinsoreanu.csv",
    "Prof.dr.ing. Rodica Potolea.csv",
]

# Process each CSV file and generate a single combined HTML file
generate_html_from_csv_files(csv_files)