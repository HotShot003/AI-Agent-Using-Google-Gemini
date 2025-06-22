from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import StructuredTool
from datetime import datetime
import json

def save_to_txt(data: str, query: str, query_timestamp: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Parse and reformat JSON for clean indentation
    try:
        json_data = json.loads(data)
        formatted_data = json.dumps(json_data, indent=2)
    except json.JSONDecodeError:
        formatted_data = data  # Fallback if data isn’t valid JSON
    formatted_text = f"""--- Research Output ---
Timestamp: {timestamp}
Query: {query}
Query Timestamp: {query_timestamp}
Response:
{formatted_data}

"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    # Return both the success message and the formatted text
    return f"Data successfully saved to {filename}", formatted_text

save_tool = StructuredTool.from_function(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data, query, and query timestamp to a text file.",
    args_schema=dict(
        data=str,
        query=str,
        query_timestamp=str,
        filename=str
    )
)

search = DuckDuckGoSearchRun()
search_tool = StructuredTool.from_function(
    name="search",
    func=search.run,
    description="Search the web for information",
    args_schema=dict(query=str)
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)