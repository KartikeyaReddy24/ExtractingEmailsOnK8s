from import_utils import time, random, os, datetime, uuid, List, Tuple, \
    boto3, NoCredentialsError, search, pd, requests, load_workbook, get_tld, re

from variables import *


def search_and_extract_emails(search_value):
    count=0
    for i in search(search_value, num_results=MAX_RESULTS_PER_SEARCH):
        print("Websearch Count: ",count)
        print(i)
        if count>0 and count % MAX_WEBSEARCHES == 0:
            print(f'\n\n\t\t::::::::::: You have now reached maximum Websearches. Please wait :::::::::::\n\n')
            time.sleep(WAIT_TIME_AFTER_REACHIGN_MAX_WEBSEARCHES)
        count+=1
        try:
            time.sleep(DELAY_TIME_AFTER_EVERY_SEARCH)
            r=requests.get(i, headers=headers)
            for re_match in re.findall(EMAIL_REGEX, r.text):
                print(f'\n\t',re_match)
        except:
            print("\n\tNot Found: ",i)