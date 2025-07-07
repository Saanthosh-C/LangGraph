from dotenv import load_dotenv

from agent_reason_runnable import react_agent_runnable, tools
from react_state import AgentState

load_dotenv()

def reason_node(state: AgentState):
    print("\n REASON NODE")
    print("Input to reason node:", state["input"])
    agent_outcome = react_agent_runnable.invoke(state)
    print("Agent outcome:", agent_outcome)
    return {"agent_outcome": agent_outcome}

def act_node(state: AgentState):
    print("\n ACT NODE")
    agent_action = state["agent_outcome"]
    print("Agent action:", agent_action)

    tool_name = agent_action.tool
    tool_input = agent_action.tool_input

    tool_function = None
    for tool in tools:
        if tool.name == tool_name:
            tool_function = tool
            break

    if tool_function:
        if isinstance(tool_input, dict):
            output = tool_function.invoke(**tool_input)
        else:
            output = tool_function.invoke(tool_input)
    else:
        output = f"Tool '{tool_name}' not found"

    print("Tool output:", output)
    return {"intermediate_steps": [(agent_action, str(output))]}
