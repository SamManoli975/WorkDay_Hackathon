import getpass
import os
import ast
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser

# --- API Key Setup ---
if "GROQ_API_KEY" not in os.environ:
    try:
        print("Groq API key not found in environment variables.")
        os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
    except Exception as e:
        print(f"Error: Could not get API key via getpass: {e}")
        print("Please set the GROQ_API_KEY environment variable.")
        exit(1)

# --- LLM Initialization ---
try:
    from langchain_groq import ChatGroq
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        max_retries=2,
    )
except ImportError:
    print("Please install langchain-groq: pip install langchain-groq")
    exit(1)
except Exception as e:
    print(f"Error initializing LLM: {e}")
    exit(1)

# --- Output Parser ---
string_parser = StrOutputParser()

# --- LLM Logic ---

def is_simple(input_text: str) -> bool:
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""Given the input query: "{text}"
Determine if this query is conceptually simple (asking about one specific thing) or complex (asking multiple things, comparing, or requiring breakdown).
Reply ONLY with the word 'yes' if it is simple, or 'no' if it is complex."""
    )
    chain = prompt | llm | string_parser
    try:
        response = chain.invoke({"text": input_text}).strip().lower()
        return response == "yes"
    except Exception:
        return False

def split_into_simple_queries(input_text: str) -> list[str]:
    prompt = PromptTemplate(
        input_variables=["complex_query"],
        template="""Given the following complex query: "{complex_query}"
Break it down into a list of simple, self-contained search engine queries. Each query should focus on a single aspect.
Format your response ONLY as a Python-style list of strings."""
    )
    chain = prompt | llm | string_parser
    try:
        response_str = chain.invoke({"complex_query": input_text}).strip()
        if response_str.startswith("```"):
            response_str = response_str.strip("```python").strip("```")
        queries = ast.literal_eval(response_str)
        if isinstance(queries, list) and all(isinstance(q, str) for q in queries):
            return queries
        return [input_text]
    except Exception:
        return [input_text]

@tool
def process_query(input_text: str) -> dict:
    if not input_text or not input_text.strip():
        return {"is_simple": True, "queries": []}
    if is_simple(input_text):
        return {"is_simple": True, "queries": [input_text]}
    else:
        simple_queries = split_into_simple_queries(input_text)
        return {"is_simple": False, "queries": simple_queries}

# --- Public Functions for app2.py ---
def run_ai_edit(input_text: str) -> str:
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Improve the following text for clarity and grammar:\n\n{text}\n\nImproved Version:"
    )
    chain = prompt | llm | string_parser
    try:
        return chain.invoke({"text": input_text}).strip()
    except Exception as e:
        return f"[Error improving text: {e}]"


def run_ai_suggestions(input_text: str) -> str:
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Suggest improvements or rewrite alternatives for the following text:\n\n{text}\n\nSuggestions:"
    )
    chain = prompt | llm | string_parser
    try:
        return chain.invoke({"text": input_text}).strip()
    except Exception as e:
        return f"[Error generating suggestions: {e}]"

