import chainlit as cl


@cl.on_message
async def on_message(msg: cl.Message):
    if not msg.elements:
        await cl.Message(content="No file attached").send()
        return

    # Processing images exclusively
    images = [file for file in msg.elements if "image" in file.mime]

    # Read the first image
    with open(images[0].path, "r") as f:
        pass

    await cl.Message(content=f"Received {len(images)} image(s)").send()
