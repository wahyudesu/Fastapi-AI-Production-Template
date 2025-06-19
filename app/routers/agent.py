"""Agents router: Generate NYT-style articles using LangChain and OpenAI."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_groq import ChatGroq
from datetime import datetime
from newspaper import Article

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "Not found"}}
)

# Inisialisasi model (sama dengan GPT-4o di phi)
llm = ChatGroq(model_name="gpt-4o")

# Langkah 1: Cari artikel dari DuckDuckGo
search_tool = DuckDuckGoSearchResults()

def search_links(topic, num_results=5):
    results = search_tool.run(topic)
    links = [r['href'] for r in results[:num_results] if 'href' in r]
    return links

# Langkah 2: Ambil isi artikel dari setiap link
def extract_articles(links):
    articles = []
    for url in links:
        try:
            article = Article(url)
            article.download()
            article.parse()
            if article.text:
                articles.append(f"[{article.title}]({url})\n\n{article.text}")
        except Exception:
            continue
    return "\n\n---\n\n".join(articles)

# Langkah 3: Prompt untuk membuat artikel ala NYT
prompt_template = PromptTemplate(
    input_variables=["topic", "content"],
    template="""
You are a senior New York Times journalist.

Today's date is {date}.

Write a detailed, high-quality, NYT-worthy article on the topic: "{topic}".

Use the following sources:

{content}

---
Format in clear Markdown.
"""
)

# Chain
chain = LLMChain(llm=llm, prompt=prompt_template)

class ArticleRequest(BaseModel):
    topic: str
    num_results: Optional[int] = 5

@router.post("/generate-article", summary="Generate NYT-style article from topic")
async def generate_article_api(req: ArticleRequest):
    """
    Generate a New York Times-style article based on the given topic.
    """
    topic = req.topic
    num_results = req.num_results
    links = search_links(topic, num_results)
    content = extract_articles(links)
    if not content:
        return {"error": "Failed to extract article content from any links."}
    response = chain.run(topic=topic, content=content, date=datetime.now().strftime("%B %d, %Y"))
    return {"article": response}