import itchat
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def RomanticCrown(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req).read()

    html_soup = BeautifulSoup(response, "html.parser")
    size_container = html_soup.optgroup
    if size_container is None:
        return "403"
    size_m = size_container.find('option', attrs={'value': 'P0000EDP000B'})
    if size_m is None:
        return "403"
    if "out of stock" in size_m.text:
        return False
    else:
        return True


if __name__ == '__main__':
    url = 'https://global.romanticcrown.com/product/inuit-corduroy-down-parkaoatmeal/2797/?cate_no=36&display_group=1'
    RomanticCrown(url)
