"""Scrape data from PSA and save it to one csv-file for each card."""

import math
import os
import time
from typing import Any, List, Tuple, Union

from bs4 import BeautifulSoup
import pandas as pd
import requests


def scrape() -> None:
    """Parse urls to `scrape_psa_prizes` and store as .csv-files."""
    # Read in urls from urls.txt.
    if not os.path.exists("input/input.csv"):
        raise ValueError("'input.csv' not found")

    df = pd.read_csv("input/input.csv", sep=";")
    urls = df["link (str)"].tolist()

    # If psa-prizes/output/data doesn't exist, create it.
    if not os.path.exists("output/data"):
        os.makedirs("output/data")

    # Iterate over all urls.
    for url in urls:
        # Execute web scraping.
        scrape_psa_prizes(url)


def scrape_psa_prizes(card_url: str) -> None:
    """Scrape data as specified by "link (str)" in `input.csv`."""
    print("collecting data for {}".format(card_url))

    # Get html data from input url.
    sess = requests.Session()
    sess.mount("https://", requests.adapters.HTTPAdapter(max_retries=5))
    r = sess.get(card_url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html5lib")
    time.sleep(5)

    # Get image url links.
    images = _get_image_urls(soup)

    # Get sale prices.
    prizes = _get_prizes(soup)

    # Get dates of the sales.
    dates = _get_sale_dates(soup)

    # Get PSA grades and qualifiers.
    grades, quals = _get_grades(soup)

    # Get lot url links.
    lots = _get_lot_urls(soup)

    # Get auction houses.
    a_houses = _get_auction_houses(soup)

    # Get names of the sellers.
    sellers = _get_seller_names(soup)

    # Get sale types (auction, BIN, Best Offer, etc).
    sale_types = _get_sale_types(soup)

    # Get PSA certification numbers.
    certs = _get_psa_certs(soup)

    # Create a dataframe.
    df = pd.DataFrame(
        {
            "date": dates,
            "grade": grades,
            "qualifier": quals,
            "prize": prizes,
            "auction_house": a_houses,
            "seller": sellers,
            "sale_type": sale_types,
            "psa_certification": certs,
            "img_url": images,
            "lot_url": lots,
        }
    )

    # Write to Excel file.
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


def _get_prizes(soup: Any) -> List[float]:  # noqa: D102
    prices = [
        float(n.string.strip("$").replace(",", ""))
        for n in soup.find_all("div", {"class": "item item-price"})
    ]

    return prices


def _get_sale_dates(soup: Any) -> List[str]:  # noqa: D102
    dates = [n.string for n in soup.find_all("div", {"class": "item item-date"})]
    return dates


def _get_grades(
    soup: Any
) -> Tuple[List[Union[str, float]], List[Union[str, float]]]:  # noqa: D102
    """Prefer grades as floats not strings. One str converts whole col to str."""
    grade_data = soup.find_all("div", {"class": "item item-grade"})
    grades: List[Union[str, float]] = []
    quals: List[Union[str, float]] = []
    for n in grade_data:
        html = str(n)
        try:
            grades.append(float(html.split("</span>")[1].split("<")[0].strip()))
        except ValueError:
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


def _get_psa_certs(soup: Any) -> List[int]:  # noqa: D102
    certs = [
        int(str(n).split("</span>")[1].split("<")[0])
        for n in soup.find_all("div", {"class": "item item-cert"})
    ]
    return certs


def _get_file_name(card_url: str) -> str:  # noqa: D102
    f_name = card_url.split("-cards/")[1].split("/values")[0].replace("/", "-")
    return "{}.csv".format(os.path.join("output/data", f_name))
