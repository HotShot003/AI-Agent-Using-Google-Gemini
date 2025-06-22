from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
import google.api_core.exceptions
import re
import os
from datetime import datetime
import json

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

try:
    # Instantiate Gemini LLM with gemini-1.5-flash
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

    parser = PydanticOutputParser(pydantic_object=ResearchResponse)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a research assistant that will help generate a research paper.
                Use tools like search or wiki_tool for references when requested.
                If the query includes 'save' or similar terms (e.g., 'save to a file'), you MUST use the save_text_to_file tool to save the results.
                Wrap the output in this format and provide no other text\n{format_instructions}
                """,
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    tools = [search_tool, wiki_tool, save_tool]
    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    print(f"Current working directory: {os.getcwd()}")
    query = input("What can I help you research? ")
    query_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    raw_response = agent_executor.invoke({"query": query})

    try:
        # Get the output string and clean markdown code blocks
        output = raw_response.get("output", "")
        cleaned_output = re.sub(r'^```json\n|\n```$', '', output).strip()
        structured_response = parser.parse(cleaned_output)
        # Format console output to match file
        try:
            formatted_response = json.dumps(json.loads(cleaned_output), indent=2)
        except json.JSONDecodeError:
            formatted_response = cleaned_output
        print(f"""--- Research Output ---
Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Query: {query}
Query Timestamp: {query_timestamp}
Response:
{formatted_response}
""")
        # Automatically save the response if "save" is in the query
        if "save" in query.lower():
            try:
                save_result, formatted_text = save_tool.run({
                    "data": cleaned_output,
                    "query": query,
                    "query_timestamp": query_timestamp
                })
                print(f"Saved to {os.path.abspath('research_output.txt')}")
                print("--- Saved to research_output.txt ---")
                print(formatted_text)  # Show the exact content saved to the file
                # Update tools_used to reflect manual save
                if "save_text_to_file" not in structured_response.tools_used:
                    structured_response.tools_used.append("save_text_to_file")
                    print("Updated response with save tool:", structured_response)
            except Exception as save_error:
                print(f"Error saving to file: {save_error}")
    except Exception as e:
        print("Error parsing response:", e, "Raw Response -", raw_response)

except google.api_core.exceptions.ResourceExhausted as e:
    print(f"Quota exceeded: {e}. Try waiting a minute or switch to a paid tier. See https://ai.google.dev/gemini-api/docs/rate-limits for details.")
except Exception as e:
    print(f"Error initializing or running agent: {e}")