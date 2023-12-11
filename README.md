# ANGC PROJECTOR ASSISTANT SCRIPTS
## Heading Converter

This Python script is designed to convert the heading lines of a Microsoft Word document (docx file) to a Heading 2 format. It uses the `docx` and `argparse` libraries.

### Dependencies

- `docx`
- `argparse`

### Usage

The script is run from the command line with the following arguments:

- `-d` or `--docx_path`: The path to the docx file that needs to be processed. This argument is required.
- `-o` or `--output_path`: The path where the output file will be saved. This argument is optional. If not specified, the input file will be overwritten with the processed data.

Example usage:

```bash
python heading.py -d input.docx -o output.docx
```

In this example, `input.docx` is the file to be processed and `output.docx` is the file where the processed data will be saved. If `-o` or `--output_path` is not provided, `input.docx` will be overwritten with the processed data.