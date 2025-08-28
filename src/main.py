import os
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import BraveSearchWrapper
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv
from datetime import date

load_dotenv()

console = Console()

model = OllamaLLM(model="qwen2.5:7b-instruct")

today_date = date.today().strftime("%B/%d/%Y")
# Brave search wrapper
search = BraveSearchWrapper(
    api_key=os.environ["BRAVE_SEARCH_API_KEY"], search_kwargs={"count": 8}
)


def web_snippets(query: str) -> str:
    docs = search.download_documents(query)
    lines = []
    for d in docs:
        title = d.metadata.get("title", "")
        url = d.metadata.get("link", "")
        snippet = (d.page_content or "").strip()
        if len(snippet) > 300:
            snippet = snippet[:300] + "..."
        lines.append(f"- {title} \n {url}\n {snippet}")
    return "\n".join(lines) if lines else "No web results."


template = """
## web  


Use the `web` tool to access up-to-date information from the web or when responding to the user requires information about their location. Some examples of when to use the `web` tool include:  

- Local Information: Use the `web` tool to respond to questions that require information about the user's location, such as the weather, local businesses, or events.  
- Freshness: If up-to-date information on a topic could potentially change or enhance the answer, call the `web` tool any time you would otherwise refuse to answer a question because your knowledge might be out of date.  
- Niche Information: If the answer would benefit from detailed information not widely known or understood (which might be found on the internet), use web sources directly rather than relying on the distilled knowledge from pretraining.  
- Accuracy: If the cost of a small mistake or outdated information is high (e.g., using an outdated version of a software library or not knowing the date of the next game for a sports team), then use the `web` tool.  


The `web` tool has the following commands:  
- `search()`: Issues a new query to a search engine and outputs the response: {web}  
- `web_snippets(query: str)` Opens the given URL and displays it: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("------------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break

    web = web_snippets(question)
    result = chain.invoke({"question": question, "web": web, "today_date": today_date})
    console.print(Markdown(result))
