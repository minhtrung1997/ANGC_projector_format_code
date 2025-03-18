# This script will parse an SQL file and convert it into a pandas dataframe
# It then reformat the dataframe and save it as a docx files

import pandas as pd
import argparse, sqlite3, re, os
from local_function import convert_contents

def is_hash_like(s):
    # Define a regular expression pattern for a six-digit hexadecimal hash
    pattern = r'^[0-9a-fA-F]{6}$'
    # Use re.match to check if the string matches the pattern
    return bool(re.match(pattern, s))
def check_title_header(df):
    # Drop rows where the first 6 characters of 'title1' are hash-like
    df = df[~df['title1'].apply(lambda x: is_hash_like(x[:6]))]
    # Remove row if the contents column is less than 15 characters
    df = df[df['contents'].str.len() > 15]
    # reset the index
    df = df.reset_index(drop=True)
    return df

conn = sqlite3.connect('download_db/Dedupe_Pooled_Database_2023_curated.db')

sql_query = pd.read_sql_query('''
                               SELECT
                               title1,
                               title2,
                               contents,
                               sequence
                               FROM items
                               ''', conn)

df = pd.DataFrame(sql_query, columns = ['title1', 'title2', 'contents'])
df = check_title_header(df)
# We will use the convert_contents.main function to parse the contents column
# The function will split and altenate the verses in the contents column
# Create the new columns
df['new_contents'] = ''
for i in range(len(df)):
    df.loc[i, 'new_contents'] = convert_contents.main(df.loc[i, 'contents'])

# drop the contents column
df = df.drop(columns = ['contents'])
# Sort df by title1 alphabetically
df = df.sort_values(by=['title1'])
df = df.reset_index(drop=True)

# Output the dataframe, each item to a txt file
for i in range(len(df)):
    # make directory if it does not exist
    if not os.path.exists('output_txt'):
        os.makedirs('output_txt')
    with open(f'output_txt/{df.loc[i, "title1"]}.txt', 'w') as f:
        f.write(df.loc[i, 'new_contents'])

# print finished message
print('Finished converting SQL to txt files')
