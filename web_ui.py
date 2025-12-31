import asyncio
import gradio as gr
from app.agent.manus import Manus
from app.logger import logger
import os

async def run_agent(prompt, history):
    if not prompt.strip():
        return history + [("User", prompt), ("RTD", "Please enter a valid prompt.")]
    
    agent = await Manus.create()
    try:
        # We need to capture the agent's output. 
        # For now, we'll just run it and return a placeholder or the final result if possible.
        # Note: OpenManus/Manus agent usually logs its progress.
        logger.info(f"Processing prompt: {prompt}")
        await agent.run(prompt)
        return history + [(prompt, "Task completed! Check the logs/terminal for detailed output or look for generated files in the workspace.")]
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}")
        return history + [(prompt, f"An error occurred: {str(e)}")]
    finally:
        await agent.cleanup()

def chat_wrapper(message, history):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    new_history = loop.run_until_complete(run_agent(message, history))
    return "", new_history

with gr.Blocks(title="RTD AI Agent Interface") as demo:
    gr.Markdown("# 🤖 RTD: The Future of General AI Agents")
    gr.Markdown("Welcome to the RTD Web Interface. Enter your request below and the agent will start working on it.")
    
    chatbot = gr.Chatbot(label="RTD Conversation")
    msg = gr.Textbox(label="Your Request", placeholder="e.g., Search for the latest news about SpaceX and summarize it.")
    clear = gr.Button("Clear")

    msg.submit(chat_wrapper, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
