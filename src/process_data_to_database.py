from decode_k8s_secrets import decode_kubernetes_secrets
from search_and_extract_emails import *
from import_utils import *
from variables import *


def process_data_to_database(email_ids, website_link):

    #_,_,postgres_user_decoded, postgres_password_decoded = decode_kubernetes_secrets()

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
    email_urls=[]
    for email in email_ids:
       email_urls.append((email,website_link))
    print("EMAIL URLS:", email_urls)

    # Create a connection pool and get a connection from the pool
    conn_pool = psycopg2.pool.SimpleConnectionPool(
        1, 20, **db_params)
    conn = conn_pool.getconn()

    # Create a cursor object from the connection
    cur = conn.cursor()

    # Use batching to process data in smaller chunks
    EMAIL_URL_BATCHES = chunked(email_urls, BATCH_SIZE_FOR_EMAILIDS)
    try:
        for batch in EMAIL_URL_BATCHES:
            batch_values = [(email,url, datetime.now(timezone.utc).astimezone(EASTERN_TIME_ZONE)) for email, url in batch]
            execute_values(cur, insert_query, batch_values)

        # Commit the changes
        conn.commit()
        print("Data successfully inserted into database!")
    except Exception as e:
        # Handle any exceptions that occurred during the execution of the above code
        print(f"Error: {e}")
        conn.rollback()
    finally:
        # Close the cursor and connection
        cur.close()
        conn_pool.putconn(conn)
