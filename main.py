"""Interactive Command Line Chat Agent powered by NVIDIA Nemotron 3 Ultra and LangChain."""

import sys
import uuid

# Ensure UTF-8 output encoding for emojis on Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from langchain_core.messages import HumanMessage, ToolMessage
import config
from agent import create_agent

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    USER_COLOR = Fore.CYAN + Style.BRIGHT
    BOT_COLOR = Fore.GREEN + Style.BRIGHT
    TOOL_COLOR = Fore.YELLOW
    ERR_COLOR = Fore.RED + Style.BRIGHT
    INFO_COLOR = Fore.MAGENTA
    RESET = Style.RESET_ALL
except ImportError:
    USER_COLOR = ""
    BOT_COLOR = ""
    TOOL_COLOR = ""
    ERR_COLOR = ""
    INFO_COLOR = ""
    RESET = ""

def print_banner():
    banner = f"""
===============================================================
       NVIDIA Nemotron 3 Ultra - LangChain Chat Agent          
===============================================================
 Model       : {config.NVIDIA_MODEL}
 Status      : Ready
 Commands    : /help, /clear, /tools, /exit
===============================================================
"""
    print(INFO_COLOR + banner + RESET)

def print_help():
    print(INFO_COLOR + """
Available commands:
  /help   - Show this help message
  /clear  - Reset conversation memory (starts a new thread)
  /tools  - List available agent tools
  /exit   - Exit the chat agent
""" + RESET)

def main():
    print_banner()

    if not config.validate_config():
        sys.exit(1)

    print(INFO_COLOR + "Initializing Nemotron agent and memory..." + RESET)
    try:
        agent = create_agent()
    except Exception as e:
        print(ERR_COLOR + f"Failed to initialize agent: {e}" + RESET)
        sys.exit(1)

    thread_id = str(uuid.uuid4())
    agent_config = {"configurable": {"thread_id": thread_id}}
    print(INFO_COLOR + f"Chat session started (Thread: {thread_id[:8]}). Type your message below.\n" + RESET)

    while True:
        try:
            user_input = input(f"{USER_COLOR}You: {RESET}").strip()
            
            if not user_input:
                continue

            # Command handling
            if user_input.lower() in ("/exit", "/quit", "exit", "quit"):
                print(INFO_COLOR + "\nGoodbye! Have a great day!" + RESET)
                break
            elif user_input.lower() == "/help":
                print_help()
                continue
            elif user_input.lower() == "/clear":
                thread_id = str(uuid.uuid4())
                agent_config = {"configurable": {"thread_id": thread_id}}
                print(INFO_COLOR + f"\n[Session cleared! New thread: {thread_id[:8]}]\n" + RESET)
                continue
            elif user_input.lower() == "/tools":
                from tools import agent_tools
                print(INFO_COLOR + "\nAvailable tools:" + RESET)
                for tool in agent_tools:
                    print(f" - {TOOL_COLOR}{tool.name}{RESET}: {tool.description.splitlines()[0]}")
                print()
                continue

            # Stream response and tool calls
            print(f"{BOT_COLOR}Nemotron: {RESET}", end="", flush=True)

            inputs = {"messages": [HumanMessage(content=user_input)]}
            last_message_content = ""

            for event in agent.stream(inputs, config=agent_config, stream_mode="values"):
                messages = event.get("messages", [])
                if messages:
                    latest = messages[-1]
                    # Check if latest is a ToolMessage to display tool feedback
                    if isinstance(latest, ToolMessage):
                        print(f"\n{TOOL_COLOR}[Tool '{latest.name}' returned]: {latest.content[:150]}...{RESET}")
                        print(f"{BOT_COLOR}Nemotron: {RESET}", end="", flush=True)
                    elif hasattr(latest, "content") and latest.content and latest.type == "ai":
                        # If the AI produced tool calls without text content yet
                        if not latest.tool_calls:
                            last_message_content = latest.content
                        elif latest.tool_calls:
                            for tc in latest.tool_calls:
                                print(f"\n{TOOL_COLOR}[Calling Tool: {tc['name']} with args {tc['args']}]{RESET}")

            if last_message_content:
                print(f"{last_message_content}\n")
            else:
                print()

        except KeyboardInterrupt:
            print(INFO_COLOR + "\n\nSession terminated by user." + RESET)
            break
        except Exception as e:
            print(f"\n{ERR_COLOR}An error occurred: {e}{RESET}\n")

if __name__ == "__main__":
    main()
