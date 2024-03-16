# This script will parse an SQL file and convert it into a pandas dataframe
# It then reformat the dataframe and save it as a docx files

import pandas as pd
import argparse
import docx
import sqlite3
from local_function import convert_contents

conn = sqlite3.connect('Dedupe_Pooled_Database_2023_curated.db')

sql_query = pd.read_sql_query('''
                               SELECT
                               title1,
                               title2,
                               contents,
                               sequence
                               FROM items
                               ''', conn)

df = pd.DataFrame(sql_query, columns = ['title1', 'title2', 'contents'])

# We will use the convert_contents.main function to parse the contents column
# The function will split the contents into content1 and content2 and return them as a string
# Create the new columns
df['content1'] = ''
df['content2'] = ''
for i in range(len(df)):
    # check if contents has [region 2] marker if not then content1 equals contents and content2 equals ''
    if '[region 2]' not in df['contents'][i]:
        df['content1'][i] = df['contents'][i]
        df['content2'][i] = ''
    else:
        df['content1'][i], df['content2'][i] = convert_contents.main(df['contents'][i])

# drop the contents column
df = df.drop(columns = ['contents'])
print(df)


# Now we need to reformat the dataframe and write it to a docx file
# The title1 will be the heading
# below is the title2 (not a heading) and content1 and content2
# Contents will be placed in a double column table format
# Content1 will be in the left column and content2 will be in the right column

doc = docx.Document()
for i in range(len(df)):
    doc.add_heading(f"Song {i+1}: {df['title1'][i]}", level=1)
    doc.add_paragraph(df['title2'][i])
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    table.autofit = True
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = df['content1'][i]
    hdr_cells[1].text = df['content2'][i]
    
    doc.add_paragraph()

doc.save('Danh sách bài hát ANGC.docx')

