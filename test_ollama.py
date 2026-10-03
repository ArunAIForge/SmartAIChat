import ollama

response = ollama.chat(
    model="phi4-mini",
    messages=[
        {
            "role": "user",
            "content": "Explain dependency injection in ASP.NET Core in simple terms."
        }
    ]
)

print(response["message"]["content"])