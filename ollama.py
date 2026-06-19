from openai import OpenAI
from ddgs import DDGS
from memory import load_memory, save_memory, clear_memory
import requests
from bs4 import BeautifulSoup

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def fetch_page(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return text[:1000]
    except:
        return ""

def search(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

    if not results:
        return "No results found."

    formatted = ""
    for r in results:
        formatted += f"Title: {r['title']}\n"
        formatted += f"URL: {r['href']}\n"
        page_text = fetch_page(r['href'])
        if page_text:
            formatted += f"Content: {page_text}\n\n"
        else:
            formatted += f"Summary: {r['body']}\n\n"

    return formatted

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