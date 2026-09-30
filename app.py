import os
import base64
import mimetypes
import time
from collections import defaultdict, deque

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

system_message = """
You are Relative Tech Support, a friendly and technically knowledgeable grandson
who has become the family's unofficial tech support.

Your personality:
- You are friendly, patient, conversational, and occasionally playful.
- Use light, affectionate humor when appropriate.
- Humor should be subtle and occasional, not a required part of a response.
  Most responses do not need a joke or playful metaphor. Avoid repeatedly
  using the same joke, metaphor, or playful theme.
- Never mock the user or make them feel foolish for not understanding technology.
- Assume the user may have little technical knowledge. Explain things in plain
  language and avoid unnecessary jargon.
- Your personality should feel more like "Okay Grandma, we'll fix the Wi-Fi again"
  than a formal corporate technical support agent.

When helping with a technical problem:
- Ask clarifying questions when the problem is unclear.
- Troubleshoot step-by-step rather than overwhelming the user with many steps at once.
- Start with simple and likely causes before moving to advanced troubleshooting.
- Give the user one manageable troubleshooting step at a time. Wait for the user's 
  response or result before continuing to the next step.
- Explain what you are asking the user to do and why when that explanation would
  help them understand the problem.
- Keep responses brief and easy to scan. Prefer 2-4 short sentences when possible.
  Give only the information needed for the user's immediate next step.
- Ask only one troubleshooting question at a time. Do not add a second
  question or request for additional information until the user responds.
- Give only one troubleshooting action at a time unless multiple actions are necessary as part of a single step.
- If more information is needed before troubleshooting, ask for that information 
  first and wait for the user's response before suggesting a fix.
- If the user sends an image without a message, briefly acknowledge what is visible and ask what they need help with. Stay focused on technical support rather than offering general image-description or image-editing services.

Safety and boundaries:
- Do not claim to have performed actions on the user's device.
- Do not ask the user to reveal passwords, API keys, or other sensitive credentials.
- Clearly warn the user before suggesting actions that could delete data, change
  important settings, or otherwise have potentially destructive consequences.
- If you do not have enough information to answer reliably, say so and ask for the information you need. Do not guess or invent details about the user's device, situation, or an image you cannot see.
"""

MODEL = "gpt-5-nano"

MAX_IMAGE_SIZE_MB = 10
MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024
RATE_LIMIT_REQUESTS = 30
RATE_LIMIT_WINDOW_SECONDS = 10 * 60

request_history = defaultdict(deque)

def is_rate_limited(client_ip):
    now = time.time()
    timestamps = request_history[client_ip]

    while timestamps and now - timestamps[0] > RATE_LIMIT_WINDOW_SECONDS:
        timestamps.popleft()

    if len(timestamps) >= RATE_LIMIT_REQUESTS:
        return True

    timestamps.append(now)
    return False

openai = OpenAI(api_key=api_key)

def chat(message, history, request: gr.Request):
    client_ip = request.client.host if request and request.client else "unknown"

    if is_rate_limited(client_ip):
        yield "You're sending messages pretty quickly. Please wait a few minutes and try again."
        return

    user_text = message.get("text", "")
    files = message.get("files", [])

    user_content = []

    if user_text:
        user_content.append({
            "type": "input_text",
            "text": user_text
        })

    if files:
      image_path = files[0]

      if os.path.getsize(image_path) > MAX_IMAGE_SIZE_BYTES:
        yield f"That image is too large. Please upload an image smaller than {MAX_IMAGE_SIZE_MB} MB."
        return

      mime_type, _ = mimetypes.guess_type(image_path)

      if mime_type is None or not mime_type.startswith("image/"):
        yield "That file doesn't appear to be an image. Please upload an image file."
        return

      base64_image = encode_image(image_path)

      user_content.append({
        "type": "input_image",
        "image_url": f"data:{mime_type};base64,{base64_image}"
      })

    input_messages = []

    for item in history:
        role = item.get("role")
        content = item.get("content")

        if role not in ["user", "assistant"]:
            continue

        if isinstance(content, str):
            input_messages.append({
                "role": role,
                "content": content
            })

        elif isinstance(content, list):
            history_content = []

            for part in content:
                if part.get("type") == "text":
                    history_content.append({
                        "type": "input_text" if role == "user" else "output_text",
                        "text": part.get("text", "")
                    })

                elif part.get("type") == "file" and role == "user":
                    file_info = part.get("file", {})
                    image_path = file_info.get("path")

                    if image_path:
                        base64_image = encode_image(image_path)
                        mime_type = file_info.get("mime_type") or "image/jpeg"

                        history_content.append({
                            "type": "input_image",
                            "image_url": f"data:{mime_type};base64,{base64_image}"
                        })

            if history_content:
                input_messages.append({
                    "role": role,
                    "content": history_content
                })

    input_messages.append({
        "role": "user",
        "content": user_content
    })

    try:
        response = openai.responses.create(
            model=MODEL,
            instructions=system_message,
            input=input_messages,
            max_output_tokens=2500,
            stream=True
        )

        response_text = ""

        for event in response:
            if event.type == "response.output_text.delta":
                response_text += event.delta
                yield response_text

            elif event.type == "response.incomplete" and not response_text:
                yield (
                    "Sorry, I wasn't able to finish that response. "
                    "Please try asking again."
                )

    except Exception as error:
        print(f"OpenAI API error: {error}")
        yield (
            "Sorry, I'm having trouble connecting to the support service "
            "right now. Please try again in a moment."
        )

demo = gr.ChatInterface(
    fn=chat,
    title="Relative Tech Support",
    description="Friendly, patient tech support for everyday problems. Type a message, upload an image, or both.",
    multimodal=True
)

if __name__ == "__main__":
    demo.queue(max_size=10)
    demo.launch()
