import os
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import BraveSearchWrapper
from rich.console import Console
from rich.markdown import Markdown

console = Console()

model = OllamaLLM(model="gemma3:4b")

# Brave search wrapper
search = BraveSearchWrapper(
    api_key=os.environ["BRAVE_SEARCH_API_KEY"],
    search_kwargs={"count": 5}
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
You are helpful AI web search assistant.

Web context:
{web}

Question:
{question}

Answer clearly and cite URLs inline when useful.
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
    result = chain.invoke({"question": question, "web": web})
    console.print(Markdown(result))