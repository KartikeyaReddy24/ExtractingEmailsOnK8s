from decode_k8s_secrets import decode_kubernetes_secrets
from search_and_extract_emails import *
from import_utils import *
from more_itertools import chunked
from variables import *
from datetime import datetime, timezone, timedelta

def process_data_to_database(email_ids, website_links):

    # _,_,postgres_user_decoded, postgres_password_decoded = decode_kubernetes_secrets()

    # Define the database connection parameters
    db_params = {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
     }

    # Define the SQL query to insert the data
    insert_query = INSERT_QUERY
    # Define the list of email and url tuples to insert
    email_urls = list(zip(email_ids,website_links))
    email_set=set()
    try:
        # Create a connection pool and get a connection from the pool
        conn_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20, **db_params)
        conn = conn_pool.getconn()

        # Create a cursor object from the connection
        cur = conn.cursor()

        # Use batching to process data in smaller chunks
        EMAIL_URL_BATCHES= chunked(email_urls, BATCH_SIZE)
        for batch in EMAIL_URL_BATCHES:
            # Convert the batch to a list of tuples to pass as parameters to the prepared statement
            EST_OFFSET = timedelta(hours=-5)
            batch_values=[]
            for email,url in batch:
                if email in email_set:
                    continue
                email_set.add(email)
                batch_values.append((email, url, datetime.now(timezone.utc).astimezone(timezone(EST_OFFSET))))
            args_str = ','.join(cur.mogrify('(%s, %s, %s)', row).decode('utf8') for row in batch_values)
            cur.execute(insert_query % args_str)
        # Commit the changes
        conn.commit()

    except psycopg2.Error as e:
        # Handle any exceptions that occurred during the execution of the above code
        print(f"Error {e.pgcode}: {e.pgerror}")

    finally:
        # Close the cursor and connection
        cur.close()
        conn_pool.putconn(conn)
