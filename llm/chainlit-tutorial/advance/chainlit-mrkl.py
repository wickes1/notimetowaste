import chainlit as cl
from langchain.agents import AgentExecutor, Tool, initialize_agent
from langchain.chains import LLMMathChain
from langchain.chat_models.ollama import ChatOllama
from langchain.llms.ollama import Ollama
from langchain.utilities.serpapi import SerpAPIWrapper
from langchain_google_community import GoogleSearchAPIWrapper


@cl.on_chat_start
def on_chat_start():
    llm = ChatOllama(
        temperature=0,
        streaming=True,
        model="mistral:7b-instruct-v0.2-q6_K",
    )
    llm1 = Ollama(
        temperature=0,
        model="mistral:7b-instruct-v0.2-q6_K",
    )
    search = GoogleSearchAPIWrapper()
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions",
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math",
        ),
    ]
    agent = initialize_agent(
        tools,
        llm1,
        agent="chat-zero-shot-react-description",
        verbose=True,
        allow_dangerous_requests=True,
        agent_executor_kwargs=dict(
            return_intermediate_steps=True,
            handle_parsing_errors="If successfully execute the plan then return summarize and end the plan. Otherwise, please call the API step by step.",
            max_iterations=5,
        ),
    )
    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    await cl.make_async(agent.run)(message.content, callbacks=[cb])
