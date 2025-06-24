# AI Research Agent with Google Gemini

- A powerful AI research assistant built with Google Gemini and LangChain.
- This agent processes user queries, searches the web using DuckDuckGo, retrieves information from Wikipedia, and saves structured results to a text file.
- Ideal for research, interview preparation, or quick information gathering.
Features

## Features
- Query Processing: Accepts user queries and generates detailed responses using Google Gemini.

- Web Search: Integrates DuckDuckGo for real-time web searches.

- Wikipedia Lookup: Fetches concise data from Wikipedia for reliable references.

- Result Saving: Saves query, timestamp, and response to research_output.txt in a clean, structured format.

- Extensible Tools: Built with LangChain, allowing easy addition of new tools.

- Environment Management: Uses .env for secure API key storage.

## Prerequisites

Python 3.8+ (tested with Python 3.13)

Google Gemini API Key: Obtain from Google AI Studio

Internet Connection: Required for Gemini API, DuckDuckGo search, and Wikipedia access

## Installation

### Clone the Repository:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

### Set Up a Virtual Environment:

python -m venv venv

.\venv\Scripts\activate  # Windows

or

source venv/bin/activate  # macOS/Linux

### Install Dependencies:

pip install -r requirements.txt

### Usage
Run the Script:
python main.py

