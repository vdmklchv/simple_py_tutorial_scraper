import requests
from bs4 import BeautifulSoup
import pathlib


def retrieve_content(url: str) -> BeautifulSoup:
    """returns soup of webpage for passed url"""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


# create text file TODO
path = pathlib.Path("/Users/vdmclcv/bs4tests")
if path.exists():
    file = path / "python_doc.txt"
    if file.exists():
        with open(file, "w") as old_file:
            old_file.truncate()
    else:
        pathlib.Path.touch(file)

# get links from index page
index_page_soup = retrieve_content("https://docs.python.org/3/tutorial/")
links_bs4 = index_page_soup.select("li > a.reference.internal")
links_bs4_filtered = filter(lambda link: '#' not in link.get('href'), links_bs4)

# get content from each of links
for entry in links_bs4_filtered:
    # create URL
    entry_url = "https://docs.python.org/3/tutorial/" + entry.get('href')
    # fetch URL content
    url_soup = retrieve_content(entry_url)
    # fetch section text in URL content
    section_text = url_soup.select("div.section")[0].get_text()
    amended_section_text = section_text.replace('â', "'")
    amended_section_text = amended_section_text.replace('Â¶', "")
    # open file for writing
    with open(file, 'a') as target_file:
        target_file.write(amended_section_text)
        target_file.write('\n\n\n')
