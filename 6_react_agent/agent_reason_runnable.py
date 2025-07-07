from langchain_openai import ChatOpenAI
from langchain.agents import tool, create_react_agent
import datetime
from dotenv import load_dotenv
load_dotenv()
from langchain_community.tools import TavilySearchResults
from langchain import hub

llm = ChatOpenAI(openai_api_base="https://apidev.navigatelabsai.com",model="llama3-8b-8192")

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time in the specified format """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

search_tool = TavilySearchResults(search_depth="basic")
react_prompt = hub.pull("hwchase17/react")

@tool
def extract_date_from_text(text: str) -> str:
    """
    Extracts the first valid date found in a block of text (ISO format).
    """
    import re
    from dateutil import parser

    try:
        # Try to find a date-like string using regex
        date_matches = re.findall(r"\b(?:\d{1,2}[\s\-\/])?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\-\/]?\d{2,4}|\d{4}[-/]\d{2}[-/]\d{2}\b", text)
        if date_matches:
            parsed_date = parser.parse(date_matches[0])
            return parsed_date.strftime("%Y-%m-%d")
        return "No date found"
    except Exception as e:
        return f"Error parsing date: {str(e)}"



tools = [get_system_time, search_tool, extract_date_from_text]

react_agent_runnable = create_react_agent(tools=tools, llm=llm, prompt=react_prompt)