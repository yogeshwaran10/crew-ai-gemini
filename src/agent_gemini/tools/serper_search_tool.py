import os
import json
import requests
from typing import Type, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SerperSearchInput(BaseModel):
    """Input schema for SerperSearchTool."""
    query: str = Field(..., description="The search query to look up on the web.")
    num_results: int = Field(5, description="Number of search results to return.")
    search_type: str = Field("search", description="Type of search: 'search', 'news', 'images', or 'places'.")


class SerperSearchTool(BaseTool):
    """Tool for performing web searches using the Serper API."""
    name: str = "Web Search"
    description: str = (
        "Searches the internet for information on a given topic. "
        "Useful for finding recent or factual information about any subject. "
        "Provide a clear and specific search query for best results."
    )
    args_schema: Type[BaseModel] = SerperSearchInput
    
    # Define class attributes instead of instance variables
    api_key: str = os.getenv("SERPER_API_KEY", "")
    api_url: str = "https://google.serper.dev/search"
        
    def _run(self, query: str, num_results: int = 5, search_type: str = "search") -> str:
        """
        Execute a web search using the Serper API.
        
        Args:
            query: The search query string
            num_results: Number of results to return (default: 5)
            search_type: Type of search to perform (default: 'search')
            
        Returns:
            A formatted string containing search results
        """
        # Get API key from environment if not already set as class attribute
        api_key = self.api_key or os.getenv("SERPER_API_KEY")
        if not api_key:
            return "Serper API key not found in environment variables. Please set SERPER_API_KEY in your .env file."
        
        # Validate search_type
        valid_search_types = ["search", "news", "images", "places"]
        if search_type not in valid_search_types:
            return f"Invalid search type: {search_type}. Must be one of: {', '.join(valid_search_types)}"
        
        try:
            # Prepare the headers and payload
            headers = {
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": query,
                "num": num_results
            }
            
            # Make the API request
            response = requests.post(
                self.api_url, 
                headers=headers,
                json=payload
            )
            
            # Check for errors
            response.raise_for_status()
            
            # Parse the response
            results = response.json()
            
            # Format the results
            formatted_results = self._format_results(results, search_type, num_results)
            
            return formatted_results
            
        except requests.exceptions.RequestException as e:
            return f"Error performing web search: {str(e)}"
        except json.JSONDecodeError:
            return "Error parsing search results"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
    
    def _format_results(self, results: dict, search_type: str, num_results: int) -> str:
        """Format the search results into a readable string."""
        formatted = f"Search results for query: '{results.get('searchParameters', {}).get('q', 'Unknown query')}'\n\n"
        
        # Handle organic search results
        if search_type == "search" and "organic" in results:
            organic = results["organic"][:num_results]
            for i, result in enumerate(organic, 1):
                formatted += f"{i}. {result.get('title', 'No title')}\n"
                formatted += f"   Link: {result.get('link', 'No link')}\n"
                formatted += f"   Snippet: {result.get('snippet', 'No description')}\n\n"
        
        # Handle news search results
        elif search_type == "news" and "news" in results:
            news = results["news"][:num_results]
            for i, result in enumerate(news, 1):
                formatted += f"{i}. {result.get('title', 'No title')}\n"
                formatted += f"   Source: {result.get('source', 'Unknown source')}\n"
                formatted += f"   Published: {result.get('date', 'Unknown date')}\n"
                formatted += f"   Link: {result.get('link', 'No link')}\n"
                formatted += f"   Snippet: {result.get('snippet', 'No description')}\n\n"
        
        # Handle image search results
        elif search_type == "images" and "images" in results:
            images = results["images"][:num_results]
            for i, result in enumerate(images, 1):
                formatted += f"{i}. Image: {result.get('title', 'No title')}\n"
                formatted += f"   Source: {result.get('source', 'Unknown source')}\n"
                formatted += f"   Link: {result.get('imageUrl', 'No image URL')}\n\n"
        
        # Handle places search results
        elif search_type == "places" and "places" in results:
            places = results["places"][:num_results]
            for i, result in enumerate(places, 1):
                formatted += f"{i}. {result.get('name', 'Unnamed location')}\n"
                formatted += f"   Address: {result.get('address', 'No address')}\n"
                formatted += f"   Rating: {result.get('rating', 'No rating')}/5 ({result.get('reviewCount', '0')} reviews)\n\n"
                
        elif "answerBox" in results:
            answer = results["answerBox"]
            if "answer" in answer:
                formatted += f"Quick Answer: {answer.get('answer', '')}\n\n"
            elif "snippet" in answer:
                formatted += f"Quick Answer: {answer.get('snippet', '')}\n\n"
            
            if "snippetHighlighted" in answer:
                highlights = answer.get("snippetHighlighted", [])
                if highlights:
                    formatted += "Highlights:\n"
                    for highlight in highlights:
                        formatted += f"- {highlight}\n"
                    formatted += "\n"
        
        # If no results found
        else:
            formatted += "No results found for this search type.\n"
        
        return formatted
