from selenium.webdriver import ChromeOptions, Chrome
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")


def scrape_website(website):
    print("Connecting to Scraping Browser...")
    # sbr_connection = RemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    option = ChromeOptions()
    with Chrome(options=option) as driver:
        driver.start_client()
        driver.get(website)
        html = driver.page_source
        return html


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


# region - Moegliche Loesungen


def login_to_website(driver):
    # Moegliche Loeesung wenn man sich Anmelden muss...
    driver.find_element("ContinVue").click()
    driver.find_element("Username or email address").send_keys(os.getenv("EMAIL"))
    driver.find_element("Password").send_keys(os.getenv("PASSWORD"))
    driver.find_element("button type=submit").click()
    driver.add_credential(user=os.getenv("EMAIL"), password=os.getenv("PASSWORD"))
    element = driver.execute("findElement", {"css": ".post__post > div"})
    print(f"Element found {element}!")


def solve_captcha(driver):
    print("Waiting captcha to solve...")
    solve_res = driver.execute(
        "executeCdpCommand",
        {
            #  Der Befehl wurde nicht gefunden.
            #  Jedoch den Code behalten,
            #  sollte mal ein Problem eintreffen
            "cmd": "Captcha.waitForSolve",
            "params": {"detectTimeout": 10000},
        },
    )
    print("Captcha solve status:", solve_res["value"]["status"])
    print("Navigated! Scraping page content...")


# endregion
