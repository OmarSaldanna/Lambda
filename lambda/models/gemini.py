# https://ai.google.dev/gemini-api/docs/text-generation?lang=python

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
)
response = chat.send_message("I have 2 dogs in my house.")
print(response.text)
response = chat.send_message("How many paws are in my house?")
print(response.text)


import gemini
import base64
import io

# Initialize Gemini model
model = gemini.load("gemini-1.5-flash")  # Adjust model name based on your setup

def process_image(image_url):
    # Replace with your actual image processing logic (e.g., using libraries like OpenCV)
    # Simulate processing for now
    return {"objects": ["unknown object"]}  # Placeholder result

def chat_with_gemini(prompt, context):
    if isinstance(prompt, dict) and prompt.get("type") == "image_url":
        image_data = base64.b64decode(prompt["image_url"]["url"].split(",")[1])
        image = io.BytesIO(image_data)
        processed_image_data = process_image(image)
        # Update context with processed image data (adapt based on your needs)
        context.append({"processed_image": processed_image_data})
        prompt = f"Image analysis suggests: {processed_image_data['objects']}. {messages[-1]['content'][1]['text']}"  # Combine image analysis and user text prompt
    response = model.run(prompt, context=context)
    messages.append({
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": response.text
            }
        ]
    })
    return response.text

# Message list to store conversation history
messages = []

# Context management (assuming a context window of 120 messages)
context = messages[-120:]

# User interaction loop (replace with your UI integration)
while True:
    user_input = input("You: ")
    if user_input.startswith("data:image/png;base64,"):
        # Handle image URL input
        prompt = {"type": "image_url", "image_url": {"url": user_input}}
    else:
        # Handle text input
        prompt = user_input

    response = chat_with_gemini(prompt, context)
    print("Assistant:", response)

    # Update context for subsequent interactions
    context.append({"user_text": user_input})
    context = context[-120:]  # Maintain sliding window







import gemini

# Initialize Gemini model
model = gemini.load("gemini-1.5-flash")  # Adjust model name based on your setup

def chat_with_gemini(prompt, context):
    response = model.run(prompt, context=context)
    messages.append({
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": response.text
            }
        ]
    })
    return response.text

# Generate response based on user prompt and context
prompt = messages[-1]["content"][1]["text"]  # Get user's text prompt
response = chat_with_gemini(prompt, context)
print(response)