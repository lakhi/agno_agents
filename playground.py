from agno.agent import Agent
from agno.models.groq import Groq
from agno.playground import Playground, serve_playground_app
from agno.knowledge.pdf import PDFKnowledgeBase
import os
from agno.vectordb.chroma import ChromaDb
from agno.embedder.sentence_transformer import SentenceTransformerEmbedder
from dotenv import load_dotenv
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage

"""
TODO: 
<commit each step of the agent as and when any of this is achieved>
1. add memory to the agent
2. if it does not know the answer to a medical question, it suggests to ask a doctor
3. style the agent to be warm and friendly
4. customizable between only using the knowledge base or using the internet
5. chatbot should be PROACTIVE: it should ask follow up questions

THINK ABOUT:
1. Data Security / Privacy: you must have answers to the question of WHERE THE DATA IS STORED?
2. Data Access: researchers should be able to access the stored conversations
"""

load_dotenv(dotenv_path="/Users/lakhi/Developer/uni-studAsst-projects/ai_agents_ws/.env")

pdf_path = os.path.join(os.path.dirname(__file__), "faq_marhinovirus_en.pdf")
knowledge_base = PDFKnowledgeBase(
    path=pdf_path,
    vector_db=ChromaDb(collection="virus", embedder=SentenceTransformerEmbedder()),
)

# memory = Memory(
#     model=Groq(id="llama-3.3-70b-versatile"),
# )

marhinovirus_agent = Agent(
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    description="You are a friendly and helpful chatbot that answers queries in the best way possible",
    instructions=[
        "Always search the knowledge base",
        "After each response, ask the user if they have any other questions",
        "In case you do not find the answer to a medical question, please suggest the user to consult a medical health professional."
    ],
    markdown=True,
    monitoring=True,
    knowledge=knowledge_base,
    add_references=True,
    storage=SqliteStorage(table_name="agent_sessions", db_file="tmp/data.db"),
    add_history_to_messages=True,
    num_history_runs=3,
    # memory=memory,
    # enable_agentic_memory=True,
    # enable_user_memories=True,
)

marhinovirus_agent.knowledge.load(recreate=False)

app = Playground(agents=[marhinovirus_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)
