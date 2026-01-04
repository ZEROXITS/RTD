from typing import List

from tavily import TavilyClient

from app.tool.search.base import SearchItem, WebSearchEngine


class TavilySearchEngine(WebSearchEngine):
    """
    Tavily search engine implementation.
    Requires TAVILY_API_KEY environment variable to be set.
    """

    def __init__(self):
        self.client = TavilyClient()

    def perform_search(
        self, query: str, num_results: int = 5, *args, **kwargs
    ) -> List[SearchItem]:
        """
        Performs a search using the Tavily API.
        """
        # Tavily API supports max_results, include_answer, include_raw_content, search_depth
        # We will use basic search for now.
        
        # Extract lang and country from kwargs if available
        lang = kwargs.get("lang", "en")
        country = kwargs.get("country", "us")
        
        # Tavily search is more advanced, we will use the search endpoint
        response = self.client.search(
            query=query,
            max_results=num_results,
            search_depth="advanced",
            include_answer=False,
            include_raw_content=False,
        )

        results = []
        for item in response.get("results", []):
            results.append(
                SearchItem(
                    title=item.get("title", "No title"),
                    url=item.get("url", ""),
                    description=item.get("content", None),
                )
            )

        return results
