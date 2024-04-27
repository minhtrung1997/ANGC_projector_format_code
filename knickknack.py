def set_updatefields_true(docx_path: str):
    """ Opens the docx and adds <w:updateFields w:val="true"/> to
       (docx_path)/word/settings.xml to enforce update of TOC (and
       other fields marked as dirty) on first open.
       Saves the file afterwards.

    Arguments:
        docx_path {str} -- Absolute path to docx
    Returns:
        Nothing
    """
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    doc = Document(docx_path)
    # add child to doc.settings element
    element_updatefields = lxml.etree.SubElement(
        doc.settings.element, f"{namespace}updateFields"
    )
    element_updatefields.set(f"{namespace}val", "true")
    doc.save(docx_path)
    print(f"Added <w:updateFields w:val='true'/> to {docx_path}")

def update_toc_from_docx_file(file_path):
        subprocess.call(
            [
                "libreoffice",
                "--headless",
                f"macro:///Standard.Module1.UpdateTOC({file_path})",
            ]
        )
        print(f"Updated TOC in {file_path}")