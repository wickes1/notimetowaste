import chainlit as cl
from chainlit.types import ThreadDict


@cl.action_callback("action_button")
async def on_action(action: cl.Action):
    print("The user clicked on the action button!")

    return "Thank you for clicking on the action button!"


@cl.on_chat_start
async def on_chat_start():
    # Elements
    image = cl.Image(path="./image.png", name="image1", display="inline")

    # User Session
    cl.user_session.set("counter", 0)

    # Action
    actions = [
        cl.Action(name="action_button", value="example_value", description="Click me!")
    ]

    print("A new chat session has started!")

    # Message
    await cl.Message(
        content="Welcome to the minimal example!",
        elements=[image],
        actions=actions,
    ).send()


# Step
@cl.step
async def tool():
    # Simulate a running task
    await cl.sleep(1)

    return "Response from the tool!"


@cl.on_message
async def on_message(msg: cl.Message):
    counter = cl.user_session.get("counter")
    counter += 1
    cl.user_session.set("counter", counter)

    tool_res = await tool()

    resp = cl.Message(content="")
    await resp.send()

    await cl.sleep(1)

    resp.content = f"Received: {msg.content}, You have sent {counter} messages! Tool response: {tool_res}"

    await resp.update()


@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    print("The user resumed a previous chat session!")
