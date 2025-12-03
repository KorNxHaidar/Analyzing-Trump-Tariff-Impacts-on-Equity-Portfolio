from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

prompt = """Create a photorealistic image of an orange cat
with a green eyes, sitting on a couch."""

# Call the API to generate content
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=prompt,
)

# The response can contain both text and image data.
# Iterate through the parts to find and save the image.
for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("cat.png")