from langchain.tools import ToolRuntime, tool

@tool
def get_weather(city: str, runtime: ToolRuntime) -> str:
    """Get weather for a given city"""
    writer = runtime.stream_writer
    
    # Stream custom updates as the tool executes
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    
    # Accessing execution info as well
    info = runtime.execution_info
    print(f"Thread: {info.thread_id}, Run: {info.run_id}")
    print(f"Attepmt: {info.node_attempt}")
    
    return f"It's always synny in {city}"