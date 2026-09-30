import arxiv

client = arxiv.Client()
search = arxiv.Search(
    query="large language models",
    max_results=2
)

for i, result in enumerate(client.results(search)):
    print(f"\nResult {i+1}")
    print("Title:", result.title)
    print("Authors:", ", ".join(a.name for a in result.authors))
    print("Summary:", result.summary[:500])