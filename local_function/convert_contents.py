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

def split_and_alternate_verse(verse, content_all):
    try:
        # Check if the verse has the region 2 marker
        if '[region 2]' not in verse:
            content_all.append(verse)
            return content_all

        # Split the verse at the region 2 marker
        parts = re.split(r'(\[region 2\])', verse)

        # Remove any empty strings and strip leading/trailing whitespace
        parts[0] = parts[0].strip()
        parts[2] = parts[2].strip()

        # Ensure parts[0] ends with a newline
        if parts[0] and parts[0][-1] != '\n':
            parts[0] += '\n'

        # Ensure parts[2] starts and ends with a newline
        if parts[2] and parts[2][0] != '\n':
            parts[2] = '\n' + parts[2]
        if parts[2] and parts[2][-1] != '\n':
            parts[2] += '\n'

        # Split parts[0] and parts[2] into lines
        part0_lines = parts[0].split('\n')
        part2_lines = parts[2].split('\n')

        # Alternate lines from part0_lines and part2_lines
        for i in range(max(len(part0_lines), len(part2_lines))):
            if i < len(part0_lines) and part0_lines[i].strip():
                content_all.append(part0_lines[i] + '\n')
            if i < len(part2_lines) and part2_lines[i].strip():
                content_all.append(part2_lines[i] + '\n\n')
        return content_all
    except Exception as e:
        print(f"An error occurred: {e}, check the input string or database")

def cat_list_to_string(input_list):
    # Concatenate the list to a string
    output_string = ''.join(input_list)
    # Remove empty spaces trailing the \n in the string
    # output_string = re.sub(r'\n\s+', '\n', output_string)
    return output_string

def harmonize_key_propresent(final_string):
    """
    Harmonize the key from EZ Slide to Propresent by
    [1] to [verse 1]
    [2] to [verse 2]
    ... so on, when the key is number
    """
    # Regular expression pattern to find strings enclosed in square brackets
    pattern = r'\[(.*?)\]'
    # Find all [1], [2], [3]... in the string
    matches = re.findall(pattern, final_string)
    # Harmonize the key from EZ Slide to Propresent
    for match in matches:
        if match.isdigit():
            final_string = re.sub(r'\[' + match + r'\]', f'[verse {match}]', final_string)
    return final_string

def main(raw_input_string):
    # Remove the fault brackets
    input_string = remove_fault_brackets(raw_input_string)
    # Extract the key string
    key = extract_key_in_verse(input_string)
    # Split the string into verses
    verses = split_content_into_verse(input_string)
    # Initialize the content1 and content2 list
    content_all = []
    # Split the verse into content1 and content2
    for verse in verses:
        content_all = split_and_alternate_verse(verse, content_all)
    # Concatenate the content1 and content2 list to string
    output_string = cat_list_to_string(content_all)
    # Harmonize the key from EZ Slide to Propresent
    output_string = harmonize_key_propresent(output_string)
    return output_string

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