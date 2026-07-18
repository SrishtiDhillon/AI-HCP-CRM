# from langgraph.prebuilt import create_react_agent

# from app.llm.groq_client import llm
# from app.agent.tools import (
#     get_all_hcp,
#     get_hcp_by_location,
#     get_interactions
# )

# graph = create_react_agent(
#     llm,
#     tools=[
#         get_all_hcp,
#         get_hcp_by_location,
#         get_interactions
#     ]
# )
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage

from app.llm.groq_client import llm
from app.agent.tools import (
    get_all_hcp,
    search_hcp,
    get_interactions,
    log_interaction,
    edit_interaction,
    suggest_next_action
)


tools = [
    get_all_hcp,
    search_hcp,
    get_interactions,
    log_interaction,
    edit_interaction,
    suggest_next_action
]


system_prompt = """
You are an AI-first CRM assistant for life sciences field representatives.

You can use these CRM tools:
1. get_all_hcp
2. search_hcp
3. get_interactions
4. log_interaction
5. edit_interaction
6. suggest_next_action

Important rules:
- Use the correct tool only once when the user asks for a specific CRM action.
- If the user asks to edit an interaction, call edit_interaction once, then stop and return the success message.
- If the user asks to log an interaction, call log_interaction once, then stop and return the success message.
- If the user asks for interaction history, call get_interactions once, then stop.
- If the user asks for next action, call suggest_next_action once, then stop.
- Do not repeatedly call the same tool.
- Keep the final response concise and professional.
"""


graph = create_react_agent(
    llm,
    tools
)


def run_agent(message: str) -> str:
    response = graph.invoke(
        {
            "messages": [
                SystemMessage(content=system_prompt),
                HumanMessage(content=message)
            ]
        },
        config={
            "recursion_limit": 50
        }
    )

    return response["messages"][-1].content