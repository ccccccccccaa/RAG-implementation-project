import xml.etree.ElementTree as ET
import os

def extract_urls_from_sitemap(sitemap_path: str) -> list[str]:
    """
    
    Parses a local sitemap XML file and extracts all URLs.
    Handles common sitemap namespaces.
    """
    
    urls = []
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()

        # Define common sitemap namespaces
        # The primary one is 'http://www.sitemaps.org/schemas/sitemap/0.9'
        # Sometimes there's no explicit prefix in the tags, sometimes there is.
        namespaces = {
            'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9',
            # Add other namespaces if your sitemap uses them
        }

        # Try to find <url>/<loc> elements
        # If your sitemap is a sitemap index file (linking to other sitemaps),
        # you'll need to parse <sitemap>/<loc> elements first and then recursively parse those.
        # This example handles a sitemap file with <url> entries.
        
        url_elements = root.findall('.//sitemap:url', namespaces)
        if not url_elements: # Try without prefix if not found (common for default namespace)
            url_elements = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')


        for url_element in url_elements:
            loc_element = url_element.find('sitemap:loc', namespaces)
            if loc_element is None: # Try without prefix
                 loc_element = url_element.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            
            if loc_element is not None and loc_element.text:
                urls.append(loc_element.text.strip())
        
        # Add logic here if it's a sitemap index file (contains <sitemap> tags)
        # For example:
        sitemap_index_elements = root.findall('.//sitemap:sitemap', namespaces)
        if not sitemap_index_elements:
            sitemap_index_elements = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap')

        if sitemap_index_elements:
            print(f"Sitemap index detected. You'll need to parse these sub-sitemaps: {[s.findtext('{http://www.sitemaps.org/schemas/sitemap/0.9}loc') for s in sitemap_index_elements]}")
            # For simplicity, this example doesn't recursively parse sitemap indexes.
            # You would download/parse each sub-sitemap URL.

    except ET.ParseError as e:
        print(f"Error parsing sitemap XML at {sitemap_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during sitemap parsing: {e}")
    return urls

if __name__ == "__main__":
    # **VERY IMPORTANT: Update this path to your actual sitemap file location**
    local_sitemap_path = "your/path/to/website.xml"
    # Replace "your_sitemap_filename.xml" with the actual name of your sitemap file

    if not os.path.exists(local_sitemap_path):
        print(f"CRITICAL ERROR: Sitemap file not found at '{local_sitemap_path}'. Please check the path.")
    else:
        print(f"Attempting to extract URLs from sitemap: {local_sitemap_path}")
        extracted_urls = extract_urls_from_sitemap(local_sitemap_path)
        
        if extracted_urls:
            print(f"Successfully extracted {len(extracted_urls)} URLs:")
            for url in extracted_urls:
                print(url)
        else:
            print("No URLs were extracted. Check sitemap content and parsing logic (e.g., namespaces).")
