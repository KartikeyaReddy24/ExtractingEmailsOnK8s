from import_utils import *
from variables import *

from search_and_extract_emails import search_and_extract_emails
from decode_k8s_secrets import decode_kubernetes_secrets


def process_sqs_message():
    while True:
        # access_key_decoded, secret_key_decoded, _,_ = decode_kubernetes_secrets()

        client = boto3.resource(
            "sqs",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=REGION_NAME_SQS,
        )
        url = SQS_URL + str(SQS_QUEUE_NAME)
        receipt = client.Queue(url=url).receive_messages(MaxNumberOfMessages=1)
        req_session = requests.session()
        for cell in receipt:
            print("\nSearching for: ", cell.body)
            search_value = ""
            for val in cell.body.split():
                search_value += val + "+"

            search_and_extract_emails(search_value)

            req_session.cookies.clear()
            cell.delete(QueueUrl=url, ReceiptHandle=cell.receipt_handle)
            print("\n\n\t::::::: This SQS message is now deleted :::::::")
            time.sleep(10)
