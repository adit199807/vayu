import asyncio
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
MODEL = os.environ.get('MINI_MODEL', '')
llm = ChatOpenAI(model=MODEL)


stdio_server_params = StdioServerParameters(
    command="python",
    args=["D:\\work spaces\\AI porjects\\vayu\\src\\mcp-servers\\MathServer.py"],
)

async def main():
    print('client running')
    async with stdio_client(stdio_server_params) as (read,write):    
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("session initialized")
            tools = await load_mcp_tools(session)
            
            agent = create_react_agent(llm,tools)
            result = await agent.ainvoke({"messages": [HumanMessage(content="What is (54 + 2) * 3?")]})
            print(result["messages"][-1].content)
        

if __name__ == '__main__':
    asyncio.run(main())