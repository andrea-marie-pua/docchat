
# DocChat

I, Eru Iluvatar of Middle-CSCI40, used Python and the Groq API to breathe life into DocChat! This chatbot not only responds like a pirate and has MEMORY of previous messages within the same conversation, but can also explore files, search documents, and perform calculations. It is basically a pirate who knows how to code, or at least I hope it does!

## Features

- Interactive chatbot with pirate-style responses
- Remembers previous messages within the same conversation
- Uses four tools: `ls`, `cat`, `grep`, and `calculate`
- Can automatically call tools to answer questions about files
- Supports manual commands without contacting Groq
- Prevents users from accessing files outside the working directory
- Handles Ctrl+C and end-of-input to exit cleanly
- Includes offline doctests and mocked API tests

## Installation

Install the required dependencies and chatbot:

```bash
python -m pip install -e . -r requirements.txt
```

For live conversations, a valid Groq API key must be provided through the `GROQ_API_KEY` environment variable or a local `.env` file. The `.env` file should not be uploaded to GitHub.

## Usage

Start the chatbot by typing:

```bash
chat
```

Enter a message to receive a response. The chatbot remembers previous messages during the session.

You can also use the following commands:

- `/ls` to list files in the current directory
- `/cat` to read a file
- `/grep` to search for matching text
- `/calculate` to perform arithmetic

These manual commands work without an API request, which is especially useful if the pirate runs out of API credits!

## Testing DocChat with Previous Projects

I tested DocChat on three of my previous projects to see whether it could explore their files and answer questions about them.

### 1. Lab Homepage

Starting from the DocChat repository root:

```text
cd test_projects/lab-homepage
chat
chat> /ls .
README.md butterfly-finished.jpg butterfly-shoe-bow.jpg butterfly-step.jpg gallery.html index.html style.css submission.toml tutorial.html
chat> What HTML pages are in this project, and what is the purpose of each?
Ahoy, matey! 📜 Here be the HTML treasures in yer project:

| File | Purpose |
|------|---------|
| index.html | The home port – the first page ye land on. It welcomes visitors, gives a quick rundown of what the site’s all about, and usually has links to the other goodies. |
| tutorial.html | The how-to galley – a step-by-step guide or tutorial. This page walks users through the process (maybe how to create a butterfly-style shoe or whatever the project is about). |
| gallery.html | The display dock – a showcase of images or examples (in this case the butterfly-related photos). It lets visitors admire the visual results of the project. |

If ye find any other .html files, just drop 'em in the table and let me know! Arrr!
```

This test showed me that DocChat could identify the HTML pages in my webpage project and make guesses about their purposes based on their filenames. It did not actually read the HTML files for this response, so I would still need to check whether its descriptions were accurate.

### 2. Markdown Compiler

Starting from the DocChat repository root:

```text
cd test_projects/markdown-compiler
chat
chat> /ls .
README.md example markdown_compiler pyproject.toml requirements.txt
chat> What does README.md say this project does?
TOOL REQUEST: cat {"path":"README.md"}
Arrr, the README be tellin’ ye that this here code be the starter kit for the Markdown Compiler project in CSCI 40. It also be handy for the optional tasks in Project 4: AI Coding Agent and the Twitter Clone final project. So, in short, it’s a markdown-to-HTML compiler that’s used across a few assignments.
```

This time, DocChat automatically used `cat` to read the README instead of just guessing what the project did. I learned that the chatbot could retrieve information from a file and use it to answer a question without me manually opening the file.

### 3. eBay Scraper

Starting from the DocChat repository root:

```text
cd test_projects/ebay-scraper
chat
chat> /ls .
README.md drill press.csv drill press.json ebay-dl.py garden tools.csv garden tools.json stuffed animal.csv stuffed animal.json submission.toml
chat> What does README.md say this eBay scraper project does?
TOOL REQUEST: cat {"path":"README.md"}
Ahoy, matey! The README be tellin’ ye that this here eBay scraper, called ebay-dl.py, be a Python program that:

- Takes a search term from the command line
- Crawls up to 10 pages of eBay search results
- Uses Requests to fetch the pages and Beautiful Soup to parse them
- Extracts each listing’s name, price, condition, shipping cost, free-returns flag, and number of items sold
- Saves every listing into a JSON file (or CSV if you use the --csv flag)
- Stores missing data as null in the JSON output

So, in short, it be a handy tool to harvest eBay listings and spit 'em out in tidy JSON or CSV format. Arr!
```

This test demonstrated how DocChat could read documentation from my previous eBay scraper and explain what the program does. Instead of manually searching through the repository, I could simply ask the pirate!

## Testing

Run the doctests and integration tests:

```bash
python -m pytest --doctest-modules tools chat.py test_tool_calls.py
```

Check tool coverage:

```bash
python -m coverage run --source=tools -m pytest --doctest-modules tools
python -m coverage report -m
```

Check code style:

```bash
python -m flake8 chat.py tools --ignore=E501
```

The goal is 100% doctest coverage across all four required tools, while making sure the chatbot can execute both manual and automatic tool calls correctly.
