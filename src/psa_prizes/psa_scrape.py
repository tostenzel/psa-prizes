"""Scrape data from PSA and save it to one csv-file for each card."""

import math
import os
import sys
import time
from typing import Any, List, Tuple, Union

from bs4 import BeautifulSoup
import pandas as pd
import requests


def scrape_psa_prizes(card_url: str) -> None:
    """Scrape data as specified in `urls.txt`."""
    print("collecting data for {}".format(card_url))

    # Get html data from input url
    sess = requests.Session()
    sess.mount("https://", requests.adapters.HTTPAdapter(max_retries=5))
    r = sess.get(card_url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html5lib")
    time.sleep(5)

    # Get image url links
    images = _get_image_urls(soup)

    # Get sale prices
    prices = _get_prices(soup)

    # Get dates of the sales
    dates = _get_sale_dates(soup)

    # Get PSA grades and qualifiers
    grades, quals = _get_grades(soup)

    # Get lot url links
    lots = _get_lot_urls(soup)

    # Get auction houses
    a_houses = _get_auction_houses(soup)

    # Get names of the sellers
    sellers = _get_seller_names(soup)

    # Get sale types (auction, BIN, Best Offer, etc)
    sale_types = _get_sale_types(soup)

    # Get PSA certification numbers
    certs = _get_psa_certs(soup)

    # Create a dataframe
    df = pd.DataFrame(
        {
            "date": dates,
            "grade": grades,
            "qualifier": quals,
            "price": prices,
            "auction_house": a_houses,
            "seller": sellers,
            "sale_type": sale_types,
            "psa_certification": certs,
            "img_url": images,
            "lot_url": lots,
        }
    )

    # Write to Excel file
    df.to_csv(_get_file_name(card_url), index=False)


def _get_image_urls(soup: Any) -> List[Union[str, float]]:  # noqa: D102
    image_data = [n for n in soup.find_all("div", {"class": "item-image"})]
    images: List[Union[str, float]] = []
    for n in image_data:
        html = str(n)
        if "href" not in html:
            images.append(math.nan)
            continue
        images.append(html.split('href="')[1].split('"')[0])
    return images


def _get_prices(soup: Any) -> List[float]:  # noqa: D102
    prices = [
        float(n.string.strip("$").replace(",", ""))
        for n in soup.find_all("div", {"class": "item item-price"})
    ]
    return prices


def _get_sale_dates(soup: Any) -> List[str]:  # noqa: D102
    dates = [n.string for n in soup.find_all("div", {"class": "item item-date"})]
    return dates


def _get_grades(soup: Any) -> Tuple[List[str], List[Union[str, float]]]:  # noqa: D102
    grade_data = soup.find_all("div", {"class": "item item-grade"})
    grades: List[str] = []
    quals: List[Union[str, float]] = []
    for n in grade_data:
        html = str(n)
        grades.append(html.split("</span>")[1].split("<")[0].strip())
        if "<strong>" in html:
            quals.append(html.split("<strong>")[1].split("<")[0].strip())
        else:
            quals.append(math.nan)
    return grades, quals


def _get_lot_urls(soup: Any) -> List[Union[str, float]]:  # noqa: D102
    lot_data = soup.find_all("div", {"class": "item item-lot"})
    base_url = "https://www.psacard.com"
    lots: List[Union[str, float]] = []
    for n in lot_data:
        html = str(n)
        if "href" not in html:
            lots.append(math.nan)
            continue
        lots.append(base_url + html.split('href="')[1].split('"')[0])
    return lots


def _get_auction_houses(soup: Any) -> List[str]:  # noqa: D102
    a_houses = [
        n.string for n in soup.find_all("div", {"class": "item item-auctionhouse"})
    ]
    return a_houses


def _get_seller_names(soup: Any) -> List[str]:  # noqa: D102
    sellers = [
        n.string for n in soup.find_all("div", {"class": "item item-auctionname"})
    ]
    return sellers


def _get_sale_types(soup: Any) -> List[str]:  # noqa: D102
    sale_types = [
        n.string for n in soup.find_all("div", {"class": "item item-auctiontype"})
    ]
    return sale_types


def _get_psa_certs(soup: Any) -> List[str]:  # noqa: D102
    certs = [
        str(n).split("</span>")[1].split("<")[0]
        for n in soup.find_all("div", {"class": "item item-cert"})
    ]
    return certs


def _get_file_name(card_url: str) -> str:  # noqa: D102
    f_name = card_url.split("-cards/")[1].split("/values")[0].replace("/", "-")
    return "{}.csv".format(os.path.join("data", f_name))


#######################################################################################
# main
#######################################################################################


def main() -> None:
    """Call `PsaScrapePrizes` using `urls.txt`."""
    # Input validation
    try:
        input_url = [sys.argv[1]]
        if not input_url or not isinstance(input_url, str):
            raise ValueError(
                "input must be a url string with base \
                 'https://www.psacard.com/auctionprices/'"
            )
    except IndexError:
        # If no input url provided, read in urls from urls.txt
        if not os.path.exists("urls.txt"):
            raise ValueError("no input url passed and 'urls.txt' not found")
        with open("urls.txt") as f:
            urls = [n for n in f.read().split("\n") if n]

    # If psa-scrape/data doesn't exist, create it
    if not os.path.exists("data"):
        os.makedirs("data")

    # Iterate over all urls
    for url in urls:
        # Initialize class and execute web scraping
        scrape_psa_prizes(url)
