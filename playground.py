from agno.agent import Agent
from agno.models.groq import Groq
from agno.playground import Playground, serve_playground_app
from agno.knowledge.pdf import PDFKnowledgeBase
import os
from agno.vectordb.chroma import ChromaDb
from agno.embedder.sentence_transformer import SentenceTransformerEmbedder
from dotenv import load_dotenv

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

# Create a knowledge base from the PDF file
pdf_path = os.path.join(os.path.dirname(__file__), "faq_marhinovirus_en.pdf")
knowledge_base = PDFKnowledgeBase(
    path=pdf_path,
    vector_db=ChromaDb(collection="virus", embedder=SentenceTransformerEmbedder()),
)

marhinovirus_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=[
        "start the conversation", 
        "Ask the user how you can help them",
        "Be helpful and friendly",
        "after each response, ask the user if they have any other questions",
    ],
    add_history_to_messages=True,
    markdown=True,
    monitoring=True,
    knowledge=knowledge_base,
    search_knowledge=True,
)


marhinovirus_agent.knowledge.load(recreate=False)

app = Playground(agents=[marhinovirus_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)
