from import_utils import time, random, os, datetime, uuid, List, Tuple, \
    boto3, NoCredentialsError, search, pd, requests, load_workbook, get_tld, re, base64

from variables import *

from search_and_extract_emails import search_and_extract_emails
from decode_k8s_secrets import decode_kubernetes_secrets

def process_sqs_message():
    while True:
        access_key_decoded, secret_key_decoded, postgres_user_decoded, postgres_password_decoded, postgres_db_name_decoded = decode_kubernetes_secrets(None, None, None, None, None)

        client = boto3.resource('sqs',aws_access_key_id=access_key_decoded,
                                aws_secret_access_key=secret_key_decoded,region_name=REGION_NAME_SQS)
        url = SQS_URL + str(SQS_QUEUE_NAME)
        receipt = client.Queue(url=url).receive_messages(MaxNumberOfMessages=1)
        req_session=requests.session()
        for cell in receipt:
            print("\nSearching for: ",cell.body)
            search_value=''
            for val in cell.body.split():
                search_value+=val+'+'
            
            search_and_extract_emails(search_value)

            req_session.cookies.clear()
            cell.delete(QueueUrl=url, ReceiptHandle=cell.receipt_handle)
            print("\n\n\t::::::: This SQS message is now deleted :::::::")
            time.sleep(10)