"""
This is the main file for the ibay scraper
"""

from telegram_channel_sender import send_update
from playwright.sync_api import sync_playwright
from playwright._impl._api_types import TimeoutError

UPDATES = ""
POSTED_IDS = []
CURRENT_IDS = []  # clean on every cycle


def update_posted(appending_id: int):
    """
    Update the posted_ids.txt file with the new id
    """
    with open("logs/posted_ids.txt", "a") as posted_id_file:
        posted_id_file.write("\n" + str(appending_id))


def print_logs(log_text):
    """
    Write to the log.txt file
    """
    print(log_text)
    with open("logs/log.txt", "w") as log_file:
        log_file.write(f"{log_text}\n")


def load_prev_posted_urls():
    """
    Load the posted_ids.txt file into a variable
    """
    with open("logs/posted_ids.txt") as posted_id_file:
        content = posted_id_file.read()
        content = content.split("\n")
        for the_id in content:
            POSTED_IDS.append(the_id)


def collect_links(url):
    """
    Collects the links from the page
    """
    with sync_playwright() as play:
        ibay_browser = play.chromium.launch(headless=True)
        ibay_page = ibay_browser.new_page()
        ibay_page.goto(url)

        # <div class="col m7 s8">
        # <h5><a href="1-room-apartment-for-rent-12000-monthly-call-7339371-o5031551.html?ref=latest">
        # 1 Room Apartment for rent 12000 monthly call 7339371</a>
        # </h5>
        # </div>

        items_xpath = "div.col.m7.s8"
        items = ibay_page.query_selector_all(items_xpath)
        link_objects = items

        if len(link_objects) == 0:
            print_logs(f"Error finding {items}")

        for link_obj in link_objects:
            # get the a tag
            main_link = link_obj.query_selector("a").get_attribute("href")
            # print(main_link, link_obj)

            # the_link = f'https://ibay.com.mv/{ibay.scrape_attribute(item_sj, tag="a", attribute="href")}'
            the_link = f'https://ibay.com.mv/{main_link}'
            # print(the_link)
            link_present = False
            for posted_id in POSTED_IDS:
                if posted_id in the_link:
                    print_logs(f"Link has {posted_id}, ignoring as already posted")
                    link_present = True
                    break
                else:
                    continue
            if not link_present:
                if "daily" in the_link.casefold() or "hourly" in the_link.casefold():
                    print_logs("Pre daily hourly filter")
                    continue
                else:
                    links.append(the_link)  # technically should save a lot of time

        ibay_browser.close()


def process_listing(listing):
    """
    Process the listing id and date
    """
    listing_id_num = None
    date = None
    while listing.find(" ") != -1:
        listing = listing.replace(" ", "")
        breaker_pos = listing.find("|")
        listing_id_num = listing[10:breaker_pos]
        date = listing[-11:]
    # print(listing,id,date)
    return listing_id_num, date

def update_formatter():
    """
    Formats the update to be sent to the channel
    """

    def listing_name_with_link():
        """
        Formats the listing name with link
        """
        # listing_link = "https://t.me/dhivehishop"
        return f'🏠 **{listing_name.upper()}**'
        # return f'**[{listing_name.upper()}]({listing_link})**'

    def price():
        """
        Formats the price
        """
        if "MVR" not in listing_price:
            return ''
        return f"\n      💴 __{listing_price}__"

    def listing_numbers():
        """
        Formats the listing numbers
        """
        return f'\n      📞 [{listing_num}](tel: {listing_num}), {dnumbers_to_str}'

    def ibay_link():
        """
        Formats the ibay link
        """
        return f'\n      🔗 [LINK]({listing_link})'

    def seperator():
        """
        Formats the seperator
        """
        return f'\n`-----------`'
        # return f'2 ROOMS W/ ATTACHED TOILETS, SITTING ROOM+ BALCONIES'

    dnumbers_to_str = ""
    if len(dnumbers) > 0:
        for num in dnumbers:
            dnumbers_to_str = f"{dnumbers_to_str} [{num}](tel:{num}),"
    else:
        dnumbers_to_str = " HIDDEN_NUM"

    # `ID:`
    # `Date:{listing_id_date[1]}`

    update = f"""{listing_name_with_link()}{price()}{listing_numbers()}{ibay_link()}{seperator()}"""
    CURRENT_IDS.append(listing_id_date[0])
    with open("logs/current.txt", "a") as file:
        file.write(f"\n{listing_id_date[0]}")
    return update


def regex_search(param, description):
    """
    Search for the numbers in the description via regex
    """
    import re

    regex = re.compile(param)
    match = regex.search(description)
    if match is not None:
        return match.group()
    else:
        return None


if __name__ == "__main__":

    # 1. loading the old posts from the file into a variable
    print_logs("1. loading the old posts from the file into a variable")
    load_prev_posted_urls()

    # 2. Setup link urls
    print_logs("2. Selenium Init")
    ibay_root = "https://ibay.com.mv"
    ibay_latest = "https://ibay.com.mv/modules.php?mod=Extra_Pages&pg=latest&off=0"
    ibay_housing = "https://ibay.com.mv/housing-real-estate-b19.html?ref=popcat"
    links = []

    # 3. Collecting the links
    print_logs("3. Setting additional  pages and collect all links")
    additional_pages = 5
    for i in range(0, additional_pages):
        link = f"https://ibay.com.mv/index.php?page=browse&cid=19&off={i}"
        collect_links(link)

    # 4. The main Functions Begin now!
    print_logs("4. The main Functions Begin now!")
    for link in links:
        print_logs("5. Should we send it now? -- Checking")

        if len(UPDATES) > 1200:
            send_update(UPDATES)
            UPDATES = str()

        print_logs("Update Handling done")

        print_logs("6. Browsing and assigning the variables")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(link)
            listing_link = link

            # get the listing id and date
            # listing_id = ibay.xpath_by_attribute("div", "style", "color:#666;")
            # listing_id = ibay.xpath_by_attribute_adder(listing_id, "style", "font-size:12px;")
            # <div style="color:#666; font-size:12px;">Listing ID : 5032600 | Last Updated : 26-Sep-2023
            # </div>

            try:
                listing_id_xpath = "div[style='color:#666; font-size:12px;']"
                listing_id = page.query_selector(listing_id_xpath)
                print_logs("Waiting for objects: Listing ID")
                listing_id_sj = page.wait_for_selector(listing_id_xpath)
                listing_id_content = listing_id_sj.inner_text()
                listing_id_date = process_listing(listing_id_content)
                ListingID = listing_id_date[0]
                LastUpdated = listing_id_date[1]
            except TimeoutError:
                print_logs("Listing id not found")
                continue

            print_logs("Waiting for objects: Listing ID 2")
            print_logs("7. If listing id is present, we write the listing id to file and go to next")
            if listing_id in POSTED_IDS:
                print_logs(f"{listing_id}, was posted before:Skipping!")
                update_posted(ListingID)
                continue
            print_logs("5pass")

            listing_name = page.query_selector("div.iw-details-heading")
            if listing_name == 0:
                print_logs("Listing name not found")

            print_logs("8. If listing name is not found lets write the listings id to file and go to next")
            if listing_name == 0:
                print_logs("Listing name not found")
                update_posted(ListingID)
                continue

            print_logs("6pass")
            listing_name = listing_name.inner_text()
            if "hourly" in str(listing_name).casefold() or "daily" in str(listing_name).casefold():
                print_logs(f"Hourly/daily filter,{listing_name}")
                update_posted(ListingID)
                continue
            print_logs("7pass")

            print_logs("9. Is the user also not found? Then go to next")

            listing_user = page.query_selector("a.iw-user-name")
            if listing_user == 0:
                print_logs("user not found")
                update_posted(ListingID)
                continue
            listing_user = listing_user.inner_text()
            print_logs("8pass")

            listing_num = page.query_selector("td.i-detail-des-n")
            print_logs("9pass")

            # sometimes there won't be a number so...
            print_logs("10. Number not found? --  go to next")
            if listing_num is not None:
                listing_num = listing_num.inner_text()
            else:
                listing_num = "HIDDEN_NUM"
                print_logs("listing_num not found")
                update_posted(ListingID)
                continue
            print_logs("10pass")

            listing_price = page.query_selector("div.iw-d-price-col")

            # sometimes there won't be a number so...
            if listing_price is not None:
                listing_price = listing_price.inner_text()
                if len(listing_price) < 5:
                    print_logs("Skipping listing as price not found")
                    update_posted(ListingID)
                    continue
            else:
                print_logs("listing_price not found")
                update_posted(ListingID)
                continue

            # get phonenumbers from description
            listing_description = page.query_selector("div.details-page_product-desc")
            if listing_description is not None:
                listing_description = listing_description.inner_text()
            else:
                listing_description = "NO_DESC"

            if listing_description != "NO_DESC":
                dnumbers = []
                description_content = listing_name + listing_description

                dhiraagu = regex_search(r"7\d\d\d\d\d\d", description_content)
                if dhiraagu is not None:
                    dnumbers.append(dhiraagu)

                ooredoo = regex_search(r"9\d\d\d\d\d\d", description_content)
                if ooredoo is not None:
                    dnumbers.append(ooredoo)

                ll_dhiraagu = regex_search(r"3\d\d\d\d\d\d", description_content)
                if ll_dhiraagu is not None:
                    dnumbers.append(ll_dhiraagu)

                ll_ooredoo = regex_search(r"6\d\d\d\d\d\d", description_content)
                if ll_ooredoo is not None:
                    dnumbers.append(ll_ooredoo)

            UPDATES += "\n\n" + update_formatter()

            print_logs("Finalizing")
            page.close()

    # Sending of the very final update
    print_logs("Sending of the very final update")
    send_update(UPDATES)
    with open("logs/posted_ids.txt", "a") as f:
        for idx in CURRENT_IDS:
            print_logs("inside 14 pass")
            print_logs(f.write("\n" + idx))
    print_logs("15pass")