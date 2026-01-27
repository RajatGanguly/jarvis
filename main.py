import ollama
import base64

prompt = "medicine enzoflam"
# response = ollama.generate(model="llama3.2:latest", prompt=prompt)
# response = ollama.generate(model="llama3.2:latest", prompt=prompt, stream=True)
# print(type(response))
# print(response)

# for res in response:
#     print(res["response"], end="")

image = "test.png"

with open(image, "rb") as f:
    image_bytes = f.read()

image_64 = base64.b64encode(image_bytes).decode("utf-8")

response = ollama.generate(model="gemma3:4b", images=[image_64], prompt="Explain the image", stream=True)

# response = ollama.generate(model="gemma3:1b", images=[image_64, image_64], prompt="Explain the image", system="Explain in funny way", stream=True)

for res in response:
    print(res["response"], end="")