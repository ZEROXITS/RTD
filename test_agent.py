import asyncio
from app.agent.manus import Manus
from app.logger import logger
import sys

async def test():
    print("Starting Agent Test...")
    try:
        agent = await Manus.create()
        print("Agent created successfully.")
        prompt = "Hello, who are you?"
        print(f"Sending prompt: {prompt}")
        
        # Manual step execution to see what's happening
        agent.update_memory("user", prompt)
        print("Thinking...")
        result = await agent.step()
        print(f"Step Result: {result}")
        
        # Check memory for assistant response
        responses = [m for m in agent.memory.messages if m.role == "assistant"]
        if responses:
            print(f"Assistant Response: {responses[-1].content}")
        else:
            print("No assistant response found in memory.")
            
        await agent.cleanup()
        print("Test completed.")
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
