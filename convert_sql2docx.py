# This script will parse an SQL file and convert it into a pandas dataframe
# It then reformat the dataframe and save it as a docx files

import pandas as pd
import argparse, docx, sqlite3, re
import json
import os
from difflib import SequenceMatcher
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

def load_snapshot(snapshot_path):
    if not os.path.exists(snapshot_path):
        return {}
    with open(snapshot_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_snapshot(snapshot_path, snapshot_data):
    with open(snapshot_path, 'w', encoding='utf-8') as f:
        json.dump(snapshot_data, f, ensure_ascii=False, indent=2)

def generate_song_change_report(previous_snapshot, current_snapshot):
    previous_titles = set(previous_snapshot.keys())
    current_titles = set(current_snapshot.keys())

    new_titles = sorted(current_titles - previous_titles)
    removed_titles = sorted(previous_titles - current_titles)
    common_titles = sorted(current_titles & previous_titles)

    print("=== Song Change Report ===")
    print(f"Total songs (current): {len(current_titles)}")
    print(f"New songs added: {len(new_titles)}")
    for title in new_titles:
        print(f"  + {title}")

    changed_count = 0
    for title in common_titles:
        old_song = previous_snapshot[title]
        new_song = current_snapshot[title]
        if old_song != new_song:
            old_text = f"{old_song.get('title2', '')}\n{old_song.get('content1', '')}\n{old_song.get('content2', '')}"
            new_text = f"{new_song.get('title2', '')}\n{new_song.get('content1', '')}\n{new_song.get('content2', '')}"
            similarity_ratio = SequenceMatcher(None, old_text, new_text).ratio()
            change_percent = (1 - similarity_ratio) * 100
            print(f"  * {title}: changed {change_percent:.2f}%")
            changed_count += 1

    print(f"Changed songs: {changed_count}")
    if removed_titles:
        print(f"Removed songs: {len(removed_titles)}")
        for title in removed_titles:
            print(f"  - {title}")
    print("=== End Song Change Report ===")

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
# The function will split the contents into content1 and content2 and return them as a string
# Create the new columns
df['content1'] = ''
df['content2'] = ''
for i in range(len(df)):
    # check if contents has [region 2] marker if not then content1 equals contents and content2 equals ''
    if '[region 2]' not in df.loc[i, 'contents']:
        # df['content1'][i] = df['contents'][i]
        # df['content2'][i] = ''
        df.loc[i, 'content1'] = df.loc[i, 'contents']
        df.loc[i, 'content2'] = ''
    else:
        # df['content1'][i], df['content2'][i] = convert_contents.main(df['contents'][i])
        df.loc[i, 'content1'], df.loc[i, 'content2'] = convert_contents.main(df.loc[i, 'contents'])

# drop the contents column
df = df.drop(columns = ['contents'])
# Sort df by title1 alphabetically
df = df.sort_values(by=['title1'])
df = df.reset_index(drop=True)

# make sure the output folder exists
if not os.path.exists('output'):
    os.makedirs('output')

snapshot_path = 'output/song_snapshot.json'
previous_snapshot = load_snapshot(snapshot_path)
current_snapshot = {
    row['title1']: {
        'title2': row['title2'],
        'content1': row['content1'],
        'content2': row['content2'],
    }
    for _, row in df.iterrows()
}
if previous_snapshot:
    generate_song_change_report(previous_snapshot, current_snapshot)
else:
    print("=== Song Change Report ===")
    print("No previous snapshot found. This run will create the baseline snapshot.")
    print(f"Total songs (current): {len(current_snapshot)}")
    print("=== End Song Change Report ===")

save_snapshot(snapshot_path, current_snapshot)

# Now we need to reformat the dataframe and write it to a docx file
# The title1 will be the heading
# below is the title2 (not a heading) and content1 and content2
# Contents will be placed in a double column table format
# Content1 will be in the left column and content2 will be in the right column

doc = docx.Document()

from docx.shared import RGBColor

def add_text_with_color(cell, text):
    parts = text.split('[')
    for part in parts:
        if ']' in part:
            before_bracket, after_bracket = part.split(']', 1)
            run = cell.paragraphs[0].add_run('[' + before_bracket + ']')
            run.font.color.rgb = RGBColor(255, 0, 0)  # Red color
            run.font.bold = True
            run = cell.paragraphs[0].add_run(after_bracket)
            run.font.color.rgb = RGBColor(0, 0, 0)  # Reset to black color
            run.font.bold = False
        else:
            run = cell.paragraphs[0].add_run(part)
            run.font.color.rgb = RGBColor(0, 0, 0)  # Ensure black color for non-bracket text
            run.font.bold = False

for i in range(len(df)):
    doc.add_heading(f"Song {i+1}: {df['title1'][i]}", level=1)
    doc.add_paragraph(df['title2'][i])
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    table.autofit = True
    hdr_cells = table.rows[0].cells
    # hdr_cells[0].text = df['content1'][i]
    # hdr_cells[1].text = df['content2'][i]
    add_text_with_color(hdr_cells[0], df['content1'][i])
    add_text_with_color(hdr_cells[1], df['content2'][i])

    doc.add_paragraph()

doc.save('output/Danh sách bài hát ANGC.docx')

from docx import Document
from docx.oxml.shared import OxmlElement, qn
import lxml.etree
from docx.oxml import parse_xml
import subprocess

def add_table_of_contents(document):
    """Inserts a basic table of contents field into the given Word document."""
    doc = document

    # Add "Mục Lục" heading
    heading = doc.add_heading('Mục Lục', level=1)._element
    doc.element.body.insert(0, heading)

    # Insert TOC field with instructions (Modified section)
    toc = doc.add_paragraph()
    run = toc.add_run()

    # Add namespace declarations to each element where 'w' is used
    fldChar = OxmlElement('w:fldChar')  # creates a new element
    fldChar.set(qn('w:fldCharType'), 'begin')  # sets attribute on element
    fldChar.set(qn('w:dirty'), 'true')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')  # sets attribute on element
    instrText.text = r'TOC \o "1-3" \h \z \u'   # change 1-3 depending on heading levels you need

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:t')
    fldChar3.text = "Right-click to update field."
    fldChar2.append(fldChar3)

    fldChar4 = OxmlElement('w:fldChar')
    fldChar4.set(qn('w:fldCharType'), 'end')

    r_element = run._r
    r_element.append(fldChar)
    r_element.append(instrText)
    r_element.append(fldChar2)
    r_element.append(fldChar4)

    # Insert TOC at the first position
    toc = toc._element
    doc.element.body.insert(1, toc)

    # Add a page break after the TOC
    page_break = doc.add_page_break()._element
    doc.element.body.insert(2, page_break)

# Create or open an existing document
doc = Document('output/Danh sách bài hát ANGC.docx')
add_table_of_contents(doc)
doc.save('output/Danh sách bài hát ANGC.docx')
print("Finished creating the document")
