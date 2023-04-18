from import_utils import *
from variables import *
from process_data_to_database import process_data_to_database


def search_and_extract_emails(search_value):
    count = 0
    unique_emails = set()
    for website_links in search(search_value, num_results=MAX_RESULTS_PER_SEARCH):
        print("Websearch Count: ", count)
        print(website_links)
        if count > 0 and count % MAX_WEBSEARCHES == 0:
            print("\n\n\t\t::::::::::: You have now reached maximum Websearches. Please wait :::::::::::\n\n")
            time.sleep(WAIT_TIME_AFTER_REACHIGN_MAX_WEBSEARCHES)
        count += 1
        try:
            time.sleep(DELAY_TIME_AFTER_EVERY_SEARCH)
            r = requests.get(website_links, headers=headers)
            for email in re.findall(EMAIL_REGEX, r.text):
                if email not in unique_emails:
                    unique_emails.add(email)
                    print(f"\n\t{email}")
            if len(unique_emails) >= BATCH_SIZE:
                email_list = list(unique_emails)
                print(f"Processing {len(email_list)} emails from {website_links} to the database")
                email_strings = [str(email) for email in email_list]
                process_data_to_database(email_strings, website_links)
                unique_emails.clear()
        except:
            print(f"\n\tNot Found: {website_links}")

    if len(unique_emails) > 0:
        email_list = list(unique_emails)
        print(f"Processing {len(email_list)} emails from the last website to the database")
        email_strings = [str(email) for email in email_list]
        process_data_to_database(email_strings, website_links)
        unique_emails.clear()
