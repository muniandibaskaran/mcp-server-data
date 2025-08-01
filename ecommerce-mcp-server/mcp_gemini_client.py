import asyncio
import os
from mcp_use import MCPAgent, MCPClient
import json
from langchain_google_genai import ChatGoogleGenerativeAI
async def main():
    config = {
        "mcpServers": {
            "http": {
                "url": "http://localhost:8000/sse"
            }
        }
    }

    client = MCPClient.from_dict(config)

    llm = ChatGoogleGenerativeAI(
        api_key='AIzaSyDlYjECGojlKTxjL9zq-wI80MCeyAWVlWc',
        model="gemini-2.5-flash-preview-05-20",
        max_retries=2,
        timeout=300,
        transport="rest"
    )
    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    while True:
        try:
            user_input = input("\nYou > ")
            if user_input.lower() in ['exit', 'quit']:
                print("\nExiting...")
                break
            if not user_input:
                continue
            print(" Translating your request into a command...")
            result = await agent.run(user_input)
            print(f"\nEcommerce Bot: {result}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break


if __name__ == "__main__":
    asyncio.run(main())