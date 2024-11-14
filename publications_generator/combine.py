import pandas as pd
import glob
import os


def combine_csv_files(csv_files, output_file):
    # Read and concatenate all CSV files into a single DataFrame
    dataframes = [pd.read_csv(f, encoding="utf-8", on_bad_lines="skip") for f in csv_files]
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Sort by the number of non-null values in each row (descending)
    combined_df['non_null_count'] = combined_df.notna().sum(axis=1)
    combined_df.sort_values('non_null_count', ascending=False, inplace=True)

    # Drop duplicates, keeping the row with the most non-null values
    combined_df = combined_df.drop_duplicates(subset=combined_df.columns.difference(['non_null_count']), keep='first')

    # Remove the helper column used for counting non-null values
    combined_df.drop(columns=['non_null_count'], inplace=True)

    # Write the cleaned DataFrame to the output CSV file
    combined_df.to_csv(output_file, index=False)

    print(f"Combined file saved as {output_file}")


csv_files = [
    "As. drd. ing. Eugen-Richard Ardelean.csv",
    "As. Drd. Ing. Raluca-Laura Portase.csv",
    "As. Drd. Ing. Vlad Andrei Negru.csv",
    "Conf.dr.ing.Camelia Lemnaru.csv",
    "Prof.dr.ing. Mihaela Dinsoreanu.csv",
    "Prof.dr.ing. Rodica Potolea.csv",
]


output_file = "all_articles.csv"
combine_csv_files(csv_files, output_file)