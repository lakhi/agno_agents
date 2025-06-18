from agno.agent import Agent
# from agno.models.groq import Groq
from agno.playground import Playground, serve_playground_app
from agno.knowledge.pdf import PDFKnowledgeBase
import os
from agno.vectordb.chroma import ChromaDb
from agno.embedder.sentence_transformer import SentenceTransformerEmbedder
from dotenv import load_dotenv
# from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
# from agno.models.deepseek import DeepSeek
from agno.models.google import Gemini

"""
TODO: 
<commit each step of the agent as and when any of this is achieved>
0. add images support to the agent (through a different embedder - take off from recent Claude answer)
1. work on Sabrina's feedback
1. work on Rian's feedback: 
    a) concise answers (we don't want to overwhelm people with information excess)
    b) simpler language: 
        i. avoid complicated words
        ii. spoken language
        iii. shorter and simpler sentences
2. if it does not know the answer to a medical question, it suggests to ask a doctor
3. style the agent to be warm and friendly
4. customizable between only using the knowledge base or using the internet
5. chatbot should be PROACTIVE: it should ask follow up questions

MAYBE FUTURE:
. add memory to the agent

THINK ABOUT:
1. Data Security / Privacy: you must have answers to the question of WHERE THE DATA IS STORED?
2. Data Access: researchers should be able to access the stored conversations
"""

load_dotenv(dotenv_path="/Users/lakhi/Developer/uni-studAsst-projects/ai_agents_ws/.env")

knowledge_base = PDFKnowledgeBase(
    path="knowledge_base_pdfs",
    vector_db=ChromaDb(collection="virus", embedder=SentenceTransformerEmbedder()),
)

# Delete existing SQLite database file if it exists
db_path = os.path.join(os.path.dirname(__file__), "tmp", "data.db")
if os.path.exists(db_path):
    os.remove(db_path)

# memory = Memory(
#     model=Groq(id="llama-3.3-70b-versatile"),
# )

marhinovirus_agent = Agent(
    # model=DeepSeek(),
    model=Gemini(id="gemini-2.0-flash"),
    # model=Groq(id="deepseek-r1-distill-llama-70b"),
    # model=Groq(id="llama-3.3-70b-versatile"),
    # model=Groq(id="qwen-qwq-32b"),
    # description="You are a friendly and helpful chatbot that answers queries in the best way possible",
    description="You are a friendly and helpful chatbot that answers queries in a concise manner yet encourages the user gain more information about the topic",
    instructions=[
        "Use the following language style: avoid complicated words, use shorter and simpler sentences",
        "Always search the knowledge base if the user's question involves the words 'marhinovirus' or 'marhinitis', or any similar contextual information about infectious diseases, vaccinations, etc.",
        "After each response, suggest relevant followup questions that encourage the user to understand the topic better",
        "The suggested followup questions should have answers in the knowledge base",
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
