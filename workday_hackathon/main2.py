import os
import ast
import sys
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# LLM Setup
def init_llm():
    if "GROQ_API_KEY" not in os.environ:
        api_key = "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"
        if not api_key:
            print("API Key is required.")
            sys.exit(1)
        os.environ["GROQ_API_KEY"] = api_key
        print("Groq API Key set.")
    try:
        from langchain_groq import ChatGroq
        return ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            max_retries=2,
            api_key=os.environ["GROQ_API_KEY"]
        )
    except ImportError:
        print("Install langchain-groq: pip install langchain-groq")
        sys.exit(1)
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        sys.exit(1)

llm = init_llm()
parser = StrOutputParser()

# Helpers
def check_if_simple(query: str) -> bool:
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""Given the input query: "{text}"
Is it conceptually simple (one clear question)? Reply only 'yes' or 'no'."""
    )
    chain = prompt | llm | parser
    try:
        return chain.invoke({"text": query}).strip().lower() == "yes"
    except Exception as e:
        print(f"Error: {e}")
        return False

def split_query(query: str) -> list[str]:
    prompt = PromptTemplate(
        input_variables=["complex_query"],
        template="""Break down this complex query into a list of simple ones: "{complex_query}"
Return the list in Python syntax: ["..."] only."""
    )
    chain = prompt | llm | parser
    try:
        response = chain.invoke({"complex_query": query}).strip()
        if response.startswith("```"):
            response = response.strip("`python \n")
        return ast.literal_eval(response)
    except Exception as e:
        print(f"Could not parse split response: {e}")
        return [query]

def process_query(query: str) -> dict:
    if not query.strip():
        return {"is_simple": True, "queries": []}
    if check_if_simple(query):
        return {"is_simple": True, "queries": [query]}
    return {"is_simple": False, "queries": split_query(query)}

def run_ai_edit(text: str) -> str:
    prompt = PromptTemplate(
        input_variables=["text"],
        template="answer here if there are any questions and answer them detailed make it a maximum of 100 words and dont include **:\n\n{text}\n\nImproved:"
    )
    chain = prompt | llm | parser
    try:
        return chain.invoke({"text": text}).strip()
    except Exception as e:
        return f"[Error: {e}]"

def run_ai_suggestions(text: str) -> str:
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Suggest a way to complete this goal. break it down into a max of 5 steps, one line for each step is enough. also do not use ** or stuff like that:\n\n{text}\n\nSuggestions:"
    )
    chain = prompt | llm | parser
    try:
        return chain.invoke({"text": text}).strip()
    except Exception as e:
        return f"[Error: {e}]"

# --- Run basic tests when run directly ---
if __name__ == "__main__":
    print("\nRunning demo...\n")

    # Test queries
    q1 = "What is the capital of France?"
    q2 = "Compare the economic situation in the US and Europe and provide trends for 2024."

    print(f"Simple Query:\n{q1}")
    print(process_query(q1))

    print(f"\nComplex Query:\n{q2}")
    print(process_query(q2))

    print("\nImproving text:")
    print(run_ai_edit("i think its going to rain tommorrow."))

    print("\nSuggesting alternatives:")
    print(run_ai_suggestions("Our current process is inefficient."))
