import chainlit as cl


@cl.on_chat_start
async def main():
    # Ask Text Input
    res = await cl.AskUserMessage(content="What is your name?", timeout=10).send()
    if res:
        await cl.Message(
            content=f"Your name is: {res['output']}",
        ).send()

    files = None

    # Ask File Input
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a python file to begin!",
            accept={"text/plain": [".py"]},
        ).send()

    text_file = files[0]

    with open(text_file.path, "r", encoding="utf-8") as f:
        text = f.read()

    # Let the user know that the system is ready
    await cl.Message(
        content=f"`{text_file.name}` uploaded, it contains {len(text)} characters!"
    ).send()

    # Ask Action
    res = await cl.AskActionMessage(
        content="Pick an action!",
        actions=[
            cl.Action(name="continue", value="continue", label="✅ Continue"),
            cl.Action(name="cancel", value="cancel", label="❌ Cancel"),
        ],
    ).send()

    if res and res.get("value") == "continue":
        await cl.Message(
            content="Continue!",
        ).send()
