from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv

load_dotenv(dotenv_path="/Users/lakhi/Developer/uni-studAsst-projects/ai_agents_ws/.env")

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    markdown=True
)

agent.print_response("what is your name and who are you?", stream=True)