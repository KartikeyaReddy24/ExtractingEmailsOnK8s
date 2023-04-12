from decode_k8s_secrets import decode_kubernetes_secrets
from search_and_extract_emails import *
from import_utils import *
from more_itertools import chunked
from variables import *

def process_data_to_database(re_match, website_links):

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
    email_url_set = set([(email, url) for email in re_match for url in website_links])

    try:
        # Create a connection pool and get a connection from the pool
        conn_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20, **db_params)
        conn = conn_pool.getconn()

        # Create a cursor object from the connection
        cur = conn.cursor()

        # Use a prepared statement for the insert query
        cur = conn.cursor()
        cur.execute("PREPARE insert_statement AS " + insert_query)

        # Use batching to process data in smaller chunks
        EMAIL_URL_BATCHES= chunked(email_url_set, BATCH_SIZE)
        for batch in EMAIL_URL_BATCHES:
            # Convert the batch to a list of tuples to pass as parameters to the prepared statement
            batch_values = [(email, url, datetime.now()) for email, url in batch]
            args_str = ','.join(cur.mogrify('(%s, %s, %s)', row).decode('utf8') for row in batch_values)
            cur.execute("EXECUTE insert_statement (%s)" % args_str)

        # Commit the changes
        conn.commit()

    except psycopg2.Error as e:
        # Handle any exceptions that occurred during the execution of the above code
        print(f"Error {e.pgcode}: {e.pgerror}")

    finally:
        # Close the cursor and connection
        cur.close()
        conn_pool.putconn(conn)
