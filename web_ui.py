import asyncio
import gradio as gr
from app.agent.manus import Manus
from app.logger import logger
from app.schema import AgentState
import os

async def run_agent(prompt, history):
    if not prompt.strip():
        history.append({"role": "assistant", "content": "Please enter a valid prompt."})
        yield history
        return
    
    # Add user message to history
    history.append({"role": "user", "content": prompt})
    history.append({"role": "assistant", "content": "Thinking..."})
    yield history
    
    agent = await Manus.create()
    try:
        logger.info(f"Processing prompt: {prompt}")
        
        # Initialize agent with the request
        agent.update_memory("user", prompt)
        
        # Run the agent loop manually to capture steps
        content = ""
        async with agent.state_context(AgentState.RUNNING):
            while agent.current_step < agent.max_steps and agent.state != AgentState.FINISHED:
                agent.current_step += 1
                step_result = await agent.step()
                
                # Update content with step progress
                content += f"\n\n**Step {agent.current_step}:**\n{step_result}"
                history[-1]["content"] = content
                yield history
                
                if agent.is_stuck():
                    agent.handle_stuck_state()
        
        history[-1]["content"] += "\n\n✅ **Task completed!**"
        yield history
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}")
        history[-1]["content"] += f"\n\n❌ **An error occurred:** {str(e)}"
        yield history
    finally:
        await agent.cleanup()

with gr.Blocks(title="RTD AI Agent Interface") as demo:
    gr.Markdown("# 🤖 RTD: The Future of General AI Agents")
    gr.Markdown("Welcome to the RTD Web Interface. Enter your request below and the agent will start working on it step-by-step.")
    
    # In Gradio 6, type="messages" is default or handled differently, removing it to avoid TypeError
    chatbot = gr.Chatbot(label="RTD Conversation", height=500)
    with gr.Row():
        msg = gr.Textbox(
            label="Your Request", 
            placeholder="e.g., Search for the latest news about SpaceX and summarize it.",
            scale=4
        )
        submit_btn = gr.Button("Send", variant="primary", scale=1)
    
    clear = gr.Button("Clear History")

    # Use streaming output
    msg.submit(run_agent, [msg, chatbot], [chatbot])
    submit_btn.click(run_agent, [msg, chatbot], [chatbot])
    
    # Clear input after submit
    msg.submit(lambda: "", None, msg)
    submit_btn.click(lambda: "", None, msg)
    
    clear.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    # Ensure workspace exists
    os.makedirs("/home/ubuntu/RTD/workspace", exist_ok=True)
    demo.queue().launch(server_name="0.0.0.0", server_port=7860)
