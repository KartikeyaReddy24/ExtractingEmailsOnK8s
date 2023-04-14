from import_utils import *
from variables import *
from process_data_to_database import process_data_to_database


def search_and_extract_emails(search_value):
    count = 0
    unique_emails=set()
    for website_links in search(search_value, num_results=MAX_RESULTS_PER_SEARCH):
        print("Websearch Count: ", count)
        print(website_links)
        if count > 0 and count % MAX_WEBSEARCHES == 0:
            print(
                "\n\n\t\t::::::::::: You have now reached maximum Websearches. Please wait :::::::::::\n\n"
            )
            time.sleep(WAIT_TIME_AFTER_REACHIGN_MAX_WEBSEARCHES)
        count += 1
        try:
            time.sleep(DELAY_TIME_AFTER_EVERY_SEARCH)
            r = requests.get(website_links, headers=headers)
            for re_match in re.findall(EMAIL_REGEX, r.text):
                if re_match not in unique_emails:
                    unique_emails.add(re_match)
                print(f"\n\t", re_match)
                process_data_to_database(re_match, website_links)
        except:
            print("\n\tNot Found: ", website_links)
