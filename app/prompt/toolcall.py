SYSTEM_PROMPT = "You are an agent that can execute tool calls"

NEXT_STEP_PROMPT = (
    "Before executing any tool, you MUST first output your thought process in a <thought> tag. "
    "The thought process should explain your reasoning, plan, and the next tool call. "
    "If you want to stop interaction, use `terminate` tool/function call."
)
