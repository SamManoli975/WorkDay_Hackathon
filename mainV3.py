import os
import getpass
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.agents import AgentExecutor
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence

load_dotenv()

# Initialize LangChain LLM model
llm = init_chat_model("llama3-8b-8192", model_provider="groq")

# DuckDuckGo Search initialization
ddg = DuckDuckGoSearchRun()

# Define the is_searchable function within LangChain structure
def is_searchable(input_text: str) -> bool:
    """Determine whether the input requires a search engine."""
    print("Checking if the input requires a search engine...")
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
        Determine if the following input requires real-time information from a search engine:
        
        Examples:
        - "What is the capital of France?" -> Not Searchable
        - "Who is the current president of the United States?" -> Searchable
        - "Explain quantum mechanics." -> Not Searchable
        - "What happened yesterday in the stock market of the USA?" -> Searchable
        - "Tell me about the history of the Roman Empire." -> Not Searchable
        - "What are the latest updates on AI regulation?" -> Searchable
        
        Given the input: "{text}", reply with 'yes' if it requires a search engine or 'no' if it does not.
        """
    )  
    chain = prompt | llm
    response = chain.invoke({"text": input_text})
    result = response.content.strip().lower()    
    print(f"Searchable result: {result}")
    return result == "yes"

# Define a LangChain tool for processing the query
@tool
def process_query(input_text: str):
    """Determines if a query requires a search engine and processes accordingly."""
    if is_searchable(input_text):
        return {"requires_search": True, "query": [input_text]}
    else:
        return {"requires_search": False, "query": [input_text]}



# Define the summarize tool that uses ChatGroq to summarize text
@tool
def summarize(text: str) -> str:
    """Summarize the given text using Groq-powered LLM."""
    if "GROQ_API_KEY" not in os.environ:
        os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Example long text to summarize
    messages = [
        ("system", "You are a helpful news summariser. Summarize the user text in a concise manner."),
        ("human", text),
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg.content

# Define the tools that the agent can use
tools = [
    Tool(
        name="Process Query",
        func=process_query,
        description="Determine if the input requires a search engine and process it."
    ),
    Tool(
        name="Summarize",
        func=summarize,
        description="Summarize the final result using Groq-powered LLM."
    )
]

# Initialize the agent with the tools and an LLM
agent = initialize_agent(
    tools=tools,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    llm=llm,
    verbose=True
)

# Function to run the agent
def run_agent(user_input):
    result = agent.run(user_input)
    return result

# Main function to demonstrate the agent
if __name__ == "__main__":
    user_input = "What is the capital of Ireland?"
    agent_result = run_agent(user_input)
    print("Agent Result:", agent_result)