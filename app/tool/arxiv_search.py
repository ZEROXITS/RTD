import arxiv
from typing import List
from app.tool.base import BaseTool
from pydantic import Field

class ArxivSearchTool(BaseTool):
    name: str = "arxiv_search"
    description: str = "Search for scientific papers on ArXiv. Provide a search query."
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query for ArXiv papers",
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return (default 5)",
                "default": 5,
            },
        },
        "required": ["query"],
    }

    async def execute(self, query: str, max_results: int = 5) -> str:
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = []
            for result in search.results():
                results.append(f"Title: {result.title}\nAuthors: {', '.join(author.name for author in result.authors)}\nSummary: {result.summary}\nURL: {result.entry_id}\n")
            
            if not results:
                return "No papers found for the given query."
            
            return "\n---\n".join(results)
        except Exception as e:
            return f"Error searching ArXiv: {str(e)}"
