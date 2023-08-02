
from lxml.html import fromstring
from lxml.html.clean import Cleaner
import httpx
from pathlib import Path


base_url = "https://www.onlinesbi.sbi/" # change this
home_page = httpx.get(base_url + "/help/").content.decode(encoding="ascii", errors="ignore")


def generate_complete_url(url):
    if "https" in url:
        return url
    return base_url + url


cleaner = Cleaner(
    scripts = True,
    javascript = True,
    comments = True,
    style = True,
    inline_style = True,
    links = False,
    meta = True,
    page_structure = False,
    processing_instructions = True,
    embedded = True,
    frames = True,
    forms = True,
    annoying_tags = True,
    remove_tags = None,
    allow_tags = None,
    kill_tags = None,
    remove_unknown_tags = True,
    safe_attrs_only = True,
    add_nofollow = False,
)


all_text = []

for i, html in enumerate(Path(base_url).rglob("*html")):
    tree = fromstring(html.read_text("utf-8"))

    main_element = tree.xpath("//div[@class='main']")
    
    if not main_element:
        main_element = tree.xpath("//main[@class='main']")
    
    if not main_element:
        main_element = tree.xpath("//div[@class='aem-rte ']")

    for elem in main_element:

        for a in elem.xpath("//a"):
            href = a.get("href")
            text = a.text
            if href and text:
                text = text.strip()
                a.text = a.text + f" <{generate_complete_url(href)}> "
        cleaned_main = cleaner.clean_html(elem)

        texts = ""
        
        for x in cleaned_main.xpath("//*"):
            
            text = x.text
            if not text:
                continue
            
            text = text.split()
            if len(text) < 3:
                continue

            text = " ".join(text) + " "
            all_text.append(text)


all_text[:100]


def split_list_with_overlap(lst, batch_size, overlap):
    result = []
    start_idx = 0
    while start_idx < len(lst):
        end_idx = start_idx + batch_size
        batch = lst[start_idx:end_idx]
        result.append(batch)
        start_idx += batch_size - overlap
    return result


batch_size = 20
overlap = 10
batches = split_list_with_overlap(all_text, batch_size, overlap)

# Display the batches
for i, batch in enumerate(batches):
    print(f"Batch {i}: {''.join(batch)}")


