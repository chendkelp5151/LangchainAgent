import datetime
import math
from langchain_core.tools import tool

@tool
def get_current_datetime() -> str:
    """Returns the current date, time, and day of the week in UTC and local time.
    Call this tool whenever the user asks for the current time, date, day, or year."""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_local = datetime.datetime.now()
    return f"Local Time: {now_local.strftime('%Y-%m-%d %H:%M:%S (%A)')}\nUTC Time: {now_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}"

@tool
def calculate(expression: str) -> str:
    """Evaluates a mathematical expression safely.
    Useful for calculating sums, products, percentages, square roots, etc.
    Input should be a valid Python mathematical expression like '2 + 2' or 'sqrt(144) * 5'."""
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names.update({
        "math": math,
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "pow": pow
    })
    
    try:
        # Clean expression
        clean_expr = expression.strip().replace("^", "**")
        result = eval(clean_expr, {"__builtins__": {}}, allowed_names)
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating expression '{expression}': {str(e)}"

@tool
def search_web(query: str, max_results: int = 3) -> str:
    """Searches the web for recent information, facts, news, and documentation using DuckDuckGo.
    Use this tool when you need up-to-date facts or information not in your training data."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return f"No results found for query: '{query}'."
            formatted = []
            for i, r in enumerate(results, 1):
                formatted.append(f"{i}. {r.get('title', 'No Title')}\nURL: {r.get('href', '')}\nSnippet: {r.get('body', '')}\n")
            return "\n".join(formatted)
    except Exception as e:
        return f"Error performing web search: {str(e)}"

@tool
def create_note(content: str, title: str = "General Note") -> str:
    """Creates and saves a note or memo with a timestamp to the user's notes file.
    Use this tool whenever the user asks to save a note, make a note, jot down something, or remember a memo.
    
    Args:
        content: The text content or details of the note to record.
        title: Optional short topic or title for the note (defaults to 'General Note').
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note_entry = f"\n### [{timestamp}] {title}\n{content.strip()}\n"
        
        with open("notes.txt", "a", encoding="utf-8") as f:
            f.write(note_entry)
            
        return f"Successfully saved note '{title}' on {timestamp}."
    except Exception as e:
        return f"Error saving note: {str(e)}"

@tool
def list_notes() -> str:
    """Reads and lists all previously saved notes and memos.
    Use this tool when the user asks to see their notes, check notes, or recall saved memos."""
    try:
        import os
        if not os.path.exists("notes.txt"):
            return "No notes found. You have not saved any notes yet."
        with open("notes.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return "The notes file is empty."
            return f"--- Saved Notes ---\n{content}"
    except Exception as e:
        return f"Error reading notes: {str(e)}"
    
@tool
def tell_joke() -> str:
    """Returns a funny programmer joke."""
    return "Why do programmers prefer dark mode? Because light attracts bugs!"

# Default tools list for the agent
agent_tools = [get_current_datetime, calculate, search_web, create_note, list_notes, tell_joke]
