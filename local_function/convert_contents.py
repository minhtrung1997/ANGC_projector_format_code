import re
def remove_fault_brackets(input_string):
    # Search the strings and convert the square brackets contain 'x' in to round brackets
    pattern = r'\[(.*?)\]'
    # Replace the square brackets containing 'x' with round brackets
    output_string = re.sub(pattern, lambda x: f'({x.group(1)})' if 'x' in x.group(1) else x.group(0), input_string)

    return output_string

def extract_key_in_verse(input_string):
     # Regular expression pattern to find strings enclosed in square brackets
    pattern = r'\[(.*?)\]'

    # Find all matches in the content
    matches = re.findall(pattern, input_string)

    # Filter out '[region 2]'
    keys = [match for match in matches if match != 'region 2']

    return keys

def split_content_into_verse(input_string):
    try:
        # Remove the leading and trailing \n
        input_string = input_string.strip()
        parts = re.split(r'\[(?!region 2\])(.*?)\]\n', input_string)
        # Remove any empty strings from the list
        parts = [part for part in parts if part]
        # Add square brackets to the elements in the key list
        parts = [f'[{part}]' if part in extract_key_in_verse(input_string) else part for part in parts]
        # Group the parts into verses
        verses = [parts[i] +"\n"+ parts[i + 1] if i + 1 < len(parts) else parts[i] for i in range(0, len(parts), 2)]
        # print(verses)
        return verses
    except Exception as e:
        print(f"An error occured: {e}, check the input string or database")

def split_verse_into_region(verse,content1_df,content2_df):
    try:
        # Check if the verse has the region 2 marker
        if '[region 2]' not in verse:
            content1_df.append(verse)
            # Content2 append a number of new lines equal to the number of lines in content1
            content2_df.append('\n' * verse.count('\n'))
            return content1_df,content2_df
        # Split the verse at the region 2 marker
        parts = re.split(r'(\[region 2\])', verse)
        # print(parts)
        # Remove any empty strings leading and trailing element in part[0] and part[2]
        parts[0] = parts[0].strip()
        parts[2] = parts[2].strip()

        # if start of part[0] iis \n then remove it
        if parts[0][0] == '\n':
            parts[0] = parts[0][1:]
        # Append the first part to the content1 list
        if parts[0][-1] != '\n':
            parts[0] = parts[0] + '\n'
        content1_df.append(parts[0])

        if parts[2][0] == '\n':
            parts[2] = parts[2][1:]
        # Append the key string of the verse to part[2] if extract_key_in_verse(parts[0]) is not empty
        if extract_key_in_verse(parts[0]):
            parts[2] = f"[{extract_key_in_verse(parts[0])[0]}]\n" + parts[2]
        # If end of part[2] is not \n then add it
        if parts[2][-1] != '\n':
            parts[2] = parts[2] + '\n'
        # Append the second part to the content2 list
        content2_df.append(parts[2])
        return content1_df,content2_df
    except Exception as e:
        print(f"An error occured: {e}, check the input string or database")

def cat_list_to_string(input_list):
    # Concatenate the list to a string
    output_string = ''.join(input_list)
    # Remove empty spaces trailing the \n in the string
    output_string = re.sub(r'\n\s+', '\n', output_string)
    return output_string

def main(raw_input_string):
    # Remove the fault brackets
    input_string = remove_fault_brackets(raw_input_string)
    # Extract the key string
    key = extract_key_in_verse(input_string)
    # Split the string into verses
    verses = split_content_into_verse(input_string)
    # Initialize the content1 and content2 list
    content1 = []
    content2 = []
    # Split the verse into content1 and content2
    for verse in verses:
        content1,content2 = split_verse_into_region(verse,content1,content2)
    # Concatenate the content1 and content2 list to string
    content1 = cat_list_to_string(content1)
    content2 = cat_list_to_string(content2)
    return content1,content2

# Test the function
if __name__ == '__main__':
    input_string = """
    [1]
    This is content1
    verse 1
    [region 2]
    This is content2
    verse 1
    [chorus]
    This is content1
    chorus
    [region 2]
    This is content2
    chorus
    """
    print(main(input_string))