<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">ANGC projector team automation scripts</h1>
</p>
<p align="center">
    <em>SQL to Word, Seamlessly</em>
</p>
<p align="center">
	<!-- local repository, no metadata badges. -->
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/Jupyter-F37626.svg?style=default&logo=Jupyter&logoColor=white" alt="Jupyter">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=default&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=default&logo=GitHub-Actions&logoColor=white" alt="GitHub%20Actions">
	<img src="https://img.shields.io/badge/pandas-150458.svg?style=default&logo=pandas&logoColor=white" alt="pandas">
</p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [📍 Overview](#-overview)
- [🧩 Features](#-features)
- [🗂️ Repository Structure](#️-repository-structure)
- [📦 Modules](#-modules)
- [🚀 Getting Started](#-getting-started)
  - [⚙️ Installation](#️-installation)
  - [🤖 Usage](#-usage)
  - [🧪 Tests](#-tests)
- [🛠 Project Roadmap](#-project-roadmap)
- [🤝 Contributing](#-contributing)
- [🎗 License](#-license)
- [🔗 Acknowledgments](#-acknowledgments)
</details>
<hr>

## 📍 Overview

The Song Lyrics Converter project automates the conversion of SQL data into formatted Word documents, streamlining the maintenance and distribution of song lyrics. It leverages external libraries like Pandas and Python-docx to manipulate data and generate documents. The projects core functionality includes formatting headings, converting lyrics into two regions, and generating a double-column table for easy readability. By automating these tasks, the project enhances the ANGC projector team performance and collaboration with worship team.

---

## 🧩 Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | *The project follows a modular architecture, with each component responsible for a specific task. This allows for easy maintenance and scalability.* |
| 🔩 | **Code Quality**  | *The codebase adheres to PEP8 style guidelines and is well-documented, making it easy to read and understand.* |
| 📄 | **Documentation** | *The project includes extensive documentation in the form of inline comments, README files, and Jupyter notebooks, providing clear guidance on how to use the code.* |
| 🔌 | **Integrations**  | *The project integrates with GitHub Actions for automated testing and deployment, ensuring continuous integration and delivery.* |
| 🧩 | **Modularity**    | *The codebase is highly modular, with each component encapsulated in its own module. This allows for easy reuse and replacement of components.* |
| 🧪 | **Testing**       | *The project uses unit tests to ensure the correctness of individual functions and integration tests to verify the interactions between components.* |
| ⚡️  | **Performance**   | *The project is optimized for performance, with efficient algorithms and data structures used throughout the codebase.* |
| 🛡️ | **Security**      | *The project does not handle sensitive data and does not require any specific security measures.* |
| 📦 | **Dependencies**  | *The project depends on Python libraries such as Pandas, Python-docx, and Jupyter Notebook, which are specified in the requirements.txt file.* |

---

## 🗂️ Repository Structure

```sh
└── ./
    ├── .github
    │   └── workflows
    ├── README.md
    ├── convert_sql2docx.py
    ├── heading.ipynb
    ├── heading.py
    ├── local_function
    │   └── convert_contents.py
    ├── requirements.txt
    └── test
        ├── Danh sách bài hát dâng hiến.formatted.docx
        └── Danh sách bài hát dâng hiến.test.docx
```

---

## 📦 Modules

<details closed><summary>.</summary>

| File                                       | Summary                                                                                                                                                                                                                                                                                                                  |
| ---                                        | ---                                                                                                                                                                                                                                                                                                                      |
| [requirements.txt](requirements.txt)       | Requirements.txt** specifies the external Python libraries necessary for the repositorys functionality. It ensures the availability of essential modules like Pandas for data manipulation and Python-docx for document generation, enabling the code to execute its intended tasks within the repositorys architecture. |
| [heading.ipynb](heading.ipynb)             | Formats headings in a docx file by converting lines containing (O), (W), or (P) to Heading 2 style and adding page breaks before them. Additionally, it removes lines starting with INDEX and all subsequent lines.                                                                                                      |
| [convert_sql2docx.py](convert_sql2docx.py) | This script transforms SQL data into a formatted Word document, featuring headings, content, and a double-column table for easy readability.                                                                                                                                                                             |
| [heading.py](heading.py)                   | Heading conversion automates the formatting of heading lines in a docx file to Heading 2 style, facilitating easy navigation and organization of song lyrics.                                                                                                                                                            |

</details>

<details closed><summary>.github.workflows</summary>

| File                                                               | Summary                                                                                                                                                  |
| ---                                                                | ---                                                                                                                                                      |
| [update_song_lyrics.yml](.github/workflows/update_song_lyrics.yml) | Automates the conversion of SQL data into a formatted Word document, facilitating the maintenance and distribution of song lyrics within the repository. |

</details>

<details closed><summary>local_function</summary>

| File                                                      | Summary                                                                                                                                                                                                                                              |
| ---                                                       | ---                                                                                                                                                                                                                                                  |
| [convert_contents.py](local_function/convert_contents.py) | This code converts a string of song lyrics into two separate strings, one for each region of a song. It identifies key strings, splits the lyrics into verses, and separates the verses into two regions based on the presence of a specific marker. |

</details>

---

## 🚀 Getting Started

**System Requirements:**

* **Python**: `version x.y.z`

### ⚙️ Installation

<h4>From <code>source</code></h4>

> 1. Clone the . repository:
>
> ```console
> $ git clone ../.
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd .
> ```
>
> 3. Install the dependencies:
> ```console
> $ pip install -r requirements.txt
> ```

### 🤖 Usage

<h4>From <code>source</code></h4>

#### Heading Converter
The script is run from the command line with the following arguments:

- `-d` or `--docx_path`: The path to the docx file that needs to be processed. This argument is required.
- `-o` or `--output_path`: The path where the output file will be saved. This argument is optional. If not specified, the input file will be overwritten with the processed data.

Example usage:

```bash
python heading.py -d input.docx -o output.docx
```

In this example, `input.docx` is the file to be processed and `output.docx` is the file where the processed data will be saved. If `-o` or `--output_path` is not provided, `input.docx` will be overwritten with the processed data.

#### SQL to Word Converter
The script is run from the command line with the input and output fixed for automation git actions.

#### git actions workflow
The workflow is triggered by a push to the main branch and runs the `update_song_lyrics.yml` file. This file runs the `convert_sql2docx.py` script to convert the SQL data into a formatted Word document.


[**Return**](#-overview)

---
