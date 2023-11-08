from langchain.agents import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from dotenv import load_dotenv

load_dotenv()

#Declare tools
search = GoogleSearchAPIWrapper()

tool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=search.run,
)

ALL_TOOLS = [tool]