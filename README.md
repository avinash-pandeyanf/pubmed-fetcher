# PubMed Industry Paper Fetcher

A Python tool to fetch PubMed papers with authors from pharmaceutical/biotech companies.

## Features

- Search PubMed using advanced query syntax
- Filter papers with industry affiliations
- Export results to CSV
- Command-line interface

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/pubmed-fetcher.git
cd pubmed-fetcher

2. **Install dependencies using Poetry**

```bash
poetry install

3. **Set up environment**

```bash
echo "PUBMED_EMAIL=your.email@example.com" > .env

##Usage
#Basic Command
```bash
poetry run get-papers-list "your search query" [options]
```bash
poetry run get-papers-list "cancer treatment" --file output.csv
