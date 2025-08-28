import asyncio
import os # For file operations
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    DefaultMarkdownGenerator,
    PruningContentFilter, # Helps clean up the extracted content
    CrawlResult
)

# (Include the load_urls_from_txt function from above here)
def load_urls_from_txt(filepath: str) -> list[str]:
    urls = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if url: 
                    urls.append(url)
        print(f"Loaded {len(urls)} URLs from {filepath}")
    except FileNotFoundError:
        print(f"ERROR: URLs file not found at {filepath}")
    except Exception as e:
        print(f"ERROR: Could not read URLs from {filepath}: {e}")
    return urls

async def main_crawl_urls(urls_filepath: str, output_directory: str = "crawled_markdown_content"):
    """
    Main asynchronous function to crawl a list of URLs from a file
    and save their content as Markdown.
    """
    urls_to_crawl = load_urls_from_txt(urls_filepath)
    if not urls_to_crawl:
        print("No URLs to crawl. Exiting.")
        return

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: {output_directory}")

    # Configure the browser. headless=True is usually preferred for batch crawling.
    # verbose=True will print more logs from playwright/chromium.
    browser_config = BrowserConfig(
        headless=True,  # Set to False if you want to see browser windows (slower)
        verbose=False,   # Set to True for more detailed browser logs
        # You can also specify other browser options if needed, e.g., user_agent
        # user_agent="RMITCyberSecBotAsyncCrawler/1.0 (Assignment Project)"
    )

    # Configure the crawler run.
    # DefaultMarkdownGenerator tries to convert HTML content to clean Markdown.
    # PruningContentFilter attempts to remove boilerplate like navs, footers.
    # You might need to experiment with different filters or customize them.
    crawler_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(
                # You can adjust pruning strength if needed, e.g.
                # pruning_factor=0.5 # (default is 0.5)
            )
        ),
        # You can also specify CSS selectors to target specific content areas
        # css_selectors_to_extract_text_from = ["main", "article", ".content"], # Example
        # max_page_size_bytes=2_000_000 # Optional: limit page size
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for i, url in enumerate(urls_to_crawl):
            print(f"Crawling URL {i+1}/{len(urls_to_crawl)}: {url}")
            try:
                result: CrawlResult = await crawler.arun(
                    url=url, config=crawler_config
                )

                if result and result.markdown and result.markdown.raw_markdown:
                    # Generate a filename (sanitize it)
                    filename_base = url.replace("http://", "").replace("https://", "").replace("/", "_")
                    filename = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in filename_base)
                    filename = filename[:150] + ".md" # Limit length and add .md extension
                    
                    filepath = os.path.join(output_directory, filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(result.markdown.raw_markdown)
                    print(f"SUCCESS: Saved Markdown for {url} to {filepath}")
                    # print(f"First 200 chars of Markdown: {result.markdown.raw_markdown[:200]}")
                elif result and result.error_message:
                     print(f"CRAWL ERROR for {url}: {result.error_message} (Status: {result.status_code})")
                else:
                    print(f"INFO: No Markdown content or unexpected result for {url} (Status: {result.status_code})")

            except Exception as e:
                print(f"CRITICAL ERROR during crawling {url}: {e}")
            
            # Optional: Add a small delay between requests if needed, though asyncio handles concurrency well.
            # await asyncio.sleep(1) # e.g., 1-second delay

    print(f"Finished crawling {len(urls_to_crawl)} URLs.")

if __name__ == "__main__":
    # **IMPORTANT**: Replace this with the actual path to your TXT file containing URLs
    urls_file = "your/path/to/cleantextURL.txt"
    
    # Check if the URLs file exists before running
    if not os.path.exists(urls_file):
        print(f"FATAL: The URLs input file was not found at '{urls_file}'")
        print("Please create this file with one URL per line, or correct the path.")
    else:
        asyncio.run(main_crawl_urls(urls_filepath=urls_file, output_directory="rmit_markdown_content"))
