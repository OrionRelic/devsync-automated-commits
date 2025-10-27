from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import httpx
from bs4 import BeautifulSoup
from typing import Optional

app = FastAPI(
    title="Country Information API",
    description="API to fetch and generate Markdown outlines from Wikipedia country pages",
    version="1.0.0"
)

# Configure CORS to allow GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["GET"],  # Only allow GET requests
    allow_headers=["*"],
)


def get_wikipedia_url(country: str) -> str:
    """
    Construct the Wikipedia URL for a given country name.
    """
    # Replace spaces with underscores and capitalize appropriately
    formatted_country = country.strip().replace(" ", "_")
    return f"https://en.wikipedia.org/wiki/{formatted_country}"


def fetch_wikipedia_page(url: str) -> str:
    """
    Fetch the HTML content of a Wikipedia page.
    """
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, follow_redirects=True)
            response.raise_for_status()
            return response.text
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Wikipedia page not found for the given country")
        raise HTTPException(status_code=502, detail=f"Error fetching Wikipedia page: {str(e)}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Error connecting to Wikipedia: {str(e)}")


def extract_headings(html_content: str, country: str) -> list:
    """
    Extract all headings (H1 to H6) from the HTML content.
    Returns a list of tuples (level, text).
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the main content area (Wikipedia's main content is in the 'mw-parser-output' div)
    content = soup.find('div', class_='mw-parser-output')
    
    if not content:
        content = soup
    
    headings = []
    
    # Extract all heading tags
    for tag in content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        # Get the heading level (1-6)
        level = int(tag.name[1])
        
        # Get the text content, excluding edit links and other non-content elements
        # Remove spans with class 'mw-editsection' (edit links)
        for edit_section in tag.find_all('span', class_='mw-editsection'):
            edit_section.decompose()
        
        text = tag.get_text().strip()
        
        # Skip empty headings
        if text:
            headings.append((level, text))
    
    return headings


def generate_markdown_outline(country: str, headings: list) -> str:
    """
    Generate a Markdown-formatted outline from the extracted headings.
    """
    markdown_lines = ["## Contents", ""]
    
    # Add the country name as the main heading
    markdown_lines.append(f"# {country}")
    markdown_lines.append("")
    
    for level, text in headings:
        # Skip if this is the main title (usually matches country name)
        if level == 1 and text.lower() == country.lower():
            continue
        
        # Convert heading level to Markdown format
        # H2 becomes ##, H3 becomes ###, etc.
        markdown_prefix = "#" * level
        markdown_lines.append(f"{markdown_prefix} {text}")
    
    return "\n".join(markdown_lines)


@app.get("/api/outline", response_class=PlainTextResponse)
async def get_country_outline(
    country: Optional[str] = Query(
        None,
        description="Name of the country to fetch information for",
        example="Vanuatu"
    )
):
    """
    Fetch Wikipedia page for a country and return a Markdown outline of its headings.
    
    Parameters:
    - country: The name of the country (required)
    
    Returns:
    - A Markdown-formatted outline of the Wikipedia page headings
    """
    if not country:
        raise HTTPException(status_code=400, detail="Country parameter is required")
    
    # Get Wikipedia URL
    wiki_url = get_wikipedia_url(country)
    
    # Fetch the Wikipedia page
    html_content = fetch_wikipedia_page(wiki_url)
    
    # Extract headings
    headings = extract_headings(html_content, country)
    
    if not headings:
        raise HTTPException(status_code=404, detail="No headings found on the Wikipedia page")
    
    # Generate Markdown outline
    markdown_outline = generate_markdown_outline(country, headings)
    
    return markdown_outline


@app.get("/")
async def root():
    """
    Root endpoint providing API information.
    """
    return {
        "message": "Country Information API for GlobalEdu",
        "description": "Fetch Wikipedia country information as Markdown outlines",
        "usage": "GET /api/outline?country=<country_name>",
        "example": "/api/outline?country=Vanuatu",
        "documentation": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "Country Information API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
