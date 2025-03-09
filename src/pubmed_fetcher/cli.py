import typer
from pathlib import Path
import csv
from typing import Optional
from .fetcher import search_papers, fetch_paper_details, configure_email
from .processor import process_paper

app = typer.Typer()

@app.command()
def main(
    query: str = typer.Argument(..., help="Search query (required)"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Output CSV file"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode")
):
    configure_email()
    
    if debug:
        typer.echo(f"Searching PubMed for: {query}")
    
    pm_ids = search_papers(query)
    
    if debug:
        typer.echo(f"Found {len(pm_ids)} papers")
    
    papers = fetch_paper_details(pm_ids)
    processed = [p for p in (process_paper(paper) for paper in papers) if p]
    
    if not processed:
        typer.echo("No matching papers found.")
        return
    
    if file:
        with file.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=processed[0].keys())
            writer.writeheader()
            writer.writerows(processed)
        typer.echo(f"Saved to {file}")
    else:
        writer = csv.DictWriter(typer.get_text_stream('stdout'), fieldnames=processed[0].keys())
        writer.writeheader()
        writer.writerows(processed)

if __name__ == "__main__":
    app()