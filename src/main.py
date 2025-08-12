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

model = OllamaLLM(model="gemma3:4b")

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
You are a careful, grounded web QA assistant.

Today's date is {today_date}.

If the Sources are insufficient or conflicting, write exactly:
Not enough info in the provided sources.
and set not_answerable to true in the metadata block.

When answering:
- Keep it concise and factual.
- Every claim must map to at least one URL from Sources.
- Quote short snippets when exact wording matters, max 20 words.
- If sources conflict, state the conflict briefly and cite both. Prefer the most recent and primary source.

Web context:
{web}

Question:
{question}
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
