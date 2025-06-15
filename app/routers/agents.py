"""
This module uses LangChain and OpenAI to create a simple research agent.
It searches for articles, extracts content, and generates a New York Times-style article on a given topic.
"""

import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_groq import ChatGroq

from newspaper import Article

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
        except:
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

# Fungsi utama
from datetime import datetime

def generate_article(topic):
    print(f"🔍 Searching for articles about: {topic}")
    links = search_links(topic)
    print(f"✅ Found {len(links)} links.")
    
    print("📰 Extracting article contents...")
    content = extract_articles(links)
    
    if not content:
        return "❌ Failed to extract article content from any links."

    print("🧠 Generating final article...\n")
    response = chain.run(topic=topic, content=content, date=datetime.now().strftime("%B %d, %Y"))
    return response

# Contoh pemanggilan
article = generate_article("Simulation theory")
print(article)
