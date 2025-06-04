import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.vectordb.chroma import ChromaDb
from agno.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from agno.playground import Playground, serve_playground_app

load_dotenv(dotenv_path="/Users/lakhi/Developer/uni-studAsst-projects/ai_agents_ws/.env")

db_path = os.path.join(os.path.dirname(__file__), "tmp", "data.db")
if os.path.exists(db_path):
    os.remove(db_path)

knowledge_base = WebsiteKnowledgeBase(
    urls=["https://health.univie.ac.at/en/media-reports/"],
    max_links=1, # this is the default value -> change it later if needed
    vector_db=ChromaDb(collection="health_research_network_db", embedder=SentenceTransformerEmbedder()),
)

health_research_network_agent = Agent(
    model=Gemini(id="gemini-2.0-flash"),
    description="You are a friendly and helpful AI Agent that helps the users find out more information about the Health Research Network of the University of Vienna. You can answer questions about the network, its members, and their research areas.",
    instructions=[
        "Always search the knowledge base if the user's question includes any of these words ['health', 'research', 'network', 'members'], or any similar contextual information about the health reserach network.",
        "After each response, prod the user to ask more questions about the health research network's members and their reserach areas.",
    ],
    knowledge=knowledge_base,
    add_references=True,
    storage=SqliteStorage(table_name="agent_sessions", db_file="tmp/data.db"),
    add_history_to_messages=True,
    num_history_runs=3,
)
# health_research_network_agent.knowledge.load(recreate=False)

app = Playground(agents=[health_research_network_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)