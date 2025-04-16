import getpass
import os
import ast # For safely evaluating the string list from the LLM
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser

# --- API Key Setup (Runs only if needed, output hidden by getpass) ---
if "GROQ_API_KEY" not in os.environ:
    try:
        print("Groq API key not found in environment variables.")
        os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
    except Exception as e:
        print(f"Error: Could not get API key via getpass: {e}")
        print("Please set the GROQ_API_KEY environment variable.")
        exit(1) # Exit if key is missing

# --- LLM Initialization ---
try:
    from langchain_groq import ChatGroq
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        # max_tokens=1024, # Optional: set a reasonable limit
        timeout=None,
        max_retries=2,
    )
except ImportError:
    print("Error: langchain-groq is not installed.")
    print("Please install it: pip install langchain-groq")
    exit(1)
except Exception as e:
    print(f"Error initializing ChatGroq LLM: {e}")
    exit(1)


# --- Helper Functions (Internal Logic, No Direct Output) ---

string_parser = StrOutputParser()

def is_simple(input_text: str) -> bool:
    """Determines if the input text represents a simple query using an LLM."""
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""Given the input query: "{text}"
Determine if this query is conceptually simple (asking about one specific thing) or complex (asking multiple things, comparing, or requiring breakdown).
Reply ONLY with the word 'yes' if it is simple, or 'no' if it is complex.

Query: {text}
Is it simple (yes/no)?"""
    )
    chain = prompt | llm | string_parser
    try:
        response = chain.invoke({"text": input_text}).strip().lower()
        # Internal logic check, no print here for final output
        return response == "yes"
    except Exception as e:
        print(f"Warning: Error during simplicity check LLM call: {e}. Assuming complex.")
        return False # Default to complex if error occurs

def split_into_simple_queries(input_text: str) -> list[str]:
    """
    Splits a complex query into multiple simpler queries using an LLM.
    (Internal Logic, No Direct Output)
    """
    prompt = PromptTemplate(
        input_variables=["complex_query"],
        template="""Given the following complex query: "{complex_query}"
Break it down into a list of simple, self-contained search engine queries. Each query should focus on a single aspect.
Format your response ONLY as a Python-style list of strings. Example: ["query 1", "query 2", "query 3"]

Complex Query: {complex_query}
Simple Queries List:"""
    )
    chain = prompt | llm | string_parser
    try:
        response_str = chain.invoke({"complex_query": input_text}).strip()
        # Internal logic to parse, no print here for final output
        try:
             # Basic cleanup: remove potential markdown code fences
            if response_str.startswith("```python"):
                response_str = response_str.removeprefix("```python").removesuffix("```").strip()
            elif response_str.startswith("```"):
                 response_str = response_str.removeprefix("```").removesuffix("```").strip()

            queries = ast.literal_eval(response_str)
            if isinstance(queries, list) and all(isinstance(q, str) for q in queries):
                return queries
            else:
                 # Fallback if LLM response format is wrong
                print(f"Warning: Could not parse LLM split response correctly. Using original query as fallback split.")
                return [input_text]
        except (ValueError, SyntaxError, TypeError) as parse_error:
            print(f"Warning: Could not parse LLM split response ({parse_error}). Using original query as fallback split.")
            # Attempt a very basic split as a fallback
            if "\n" in response_str: # Maybe LLM used newlines
                 potential_queries = [line.strip('- ').strip() for line in response_str.split('\n') if line.strip()]
                 if potential_queries:
                     return potential_queries
            return [input_text] # Ultimate fallback
    except Exception as e:
        print(f"Warning: Error during query splitting LLM call: {e}. Using original query as fallback split.")
        return [input_text] # Fallback to original query if error occurs


# --- Tool Definition (Internal Logic, No Direct Output) ---
@tool
def process_query(input_text: str) -> dict:
    """Decides if the query is simple or complex and prepares query list."""
    if not input_text or not input_text.strip():
      # Handle empty input - return value will be handled by summary logic
      return {"is_simple": True, "queries": []} # Treat empty as simple

    if is_simple(input_text):
        # Classified as simple
        return {"is_simple": True, "queries": [input_text]} # Return original query even if simple
    else:
        # Classified as complex, attempt split
        simple_queries = split_into_simple_queries(input_text)
        return {"is_simple": False, "queries": simple_queries}

# --- Main Execution Block (Generates the Summary Output) ---
if __name__ == "__main__":
    try:
        user_input_text = input("Enter your prompt: ")

        if not user_input_text or not user_input_text.strip():
             print("\nProcessing Summary:")
             print("1. Received an empty query.")
             print("2. No processing needed.")
        else:
            # Call the function to get the processing decision and queries
            processing_result = process_query(user_input_text)

            # --- Generate Step-by-Step Summary ---
            print("\nProcessing Summary:")
            print(f"1. Received Query: \"{user_input_text}\"")

            if processing_result["is_simple"]:
                print("Action: No further processing (like splitting) required: is simple.")
                # You could optionally still mention the query itself here if needed downstream:
                # print(f"   (Query to use: \"{processing_result['queries'][0]}\")")

            else: # Query was complex
                print("2. Determined the query is complex.")
                print("3. Action: Split the query into simpler parts.")
                if processing_result["queries"] and processing_result["queries"] != [user_input_text]:
                    # Only list if splitting actually produced results different from original
                    print("4. Resulting simple queries to process:")
                    for i, query in enumerate(processing_result["queries"]):
                        print(f"   - Query {i+1}: \"{query}\"")
                elif processing_result["queries"] == [user_input_text]:
                    # Handle case where splitting failed and returned the original
                    print("4. Result: Splitting failed or was not possible; using original query.")
                    print(f"   - Query 1: \"{user_input_text}\"")
                else:
                     # Handle case where splitting resulted in empty list (shouldn't happen often)
                    print("4. Warning: Splitting resulted in no queries.")
    

    except Exception as e:
        print(f"\nAn unexpected error occurred during processing: {e}")