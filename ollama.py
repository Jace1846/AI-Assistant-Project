from openai import OpenAI
from memory import load_memory, save_memory, clear_memory
from functions.search import search, fetch_page

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def stream_response(messages):
    response = client.chat.completions.create(
        model="llama3.2",
        messages=messages,
        stream=True
    )

    print("\nAssistant: ", end="", flush=True)
    reply = ""
    for chunk in response:
        token = chunk.choices[0].delta.content
        if token:
            print(token, end="", flush=True)
            reply += token
    print("\n")
    return reply

messages = load_memory()
print("Assistant ready. Type 'search: your query' to search, 'clear memory' to reset, or just chat. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    if user_input.lower() == "clear memory":
        messages = clear_memory()
        print("\nMemory cleared.\n")
        continue

    if user_input.lower().startswith("search:"):
        query = user_input[7:].strip()
        print("Searching...")
        search_results = search(query)

        search_messages = messages + [{
            "role": "user",
            "content": f"User question: {query}\n\nSearch results:\n{search_results}\n\nAnswer using the search results."
        }]

        try:
            reply = stream_response(search_messages)
            messages.append({"role": "user", "content": query})
            messages.append({"role": "assistant", "content": reply})
            save_memory(messages)
        except Exception as e:
            print(f"\nError: {e}\n")

    else:
        messages.append({"role": "user", "content": user_input})

        try:
            reply = stream_response(messages)
            messages.append({"role": "assistant", "content": reply})
            save_memory(messages)
        except Exception as e:
            print(f"\nError: {e}\n")
            messages.pop()