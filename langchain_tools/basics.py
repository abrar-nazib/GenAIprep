from langchain.tools import tool

@tool
def search_database(query:str, limit:int=10) -> str:
    """
    Search the customera database for records matching the query.
    
    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
        
    return f"Found {limit} results for {query}"

@tool("web_search")  # Custom name
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

print(search.name)  # web_search

@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))

