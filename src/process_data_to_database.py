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
    try:
        # Create a connection pool and get a connection from the pool
        conn_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20, **db_params)
        conn = conn_pool.getconn()

        # Create a cursor object from the connection
        cur = conn.cursor()

        # Use batching to process data in smaller chunks
        EMAIL_URL_BATCHES= chunked(email_urls, BATCH_SIZE)
        EST_OFFSET = timedelta(hours=-5)
        batch_values=[]
        batch_values.append((EMAIL_URL_BATCHES, datetime.now(timezone.utc).astimezone(timezone(EST_OFFSET))))
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
