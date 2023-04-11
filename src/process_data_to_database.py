from decode_k8s_secrets import decode_kubernetes_secrets
from search_and_extract_emails import *
from import_utils import *


def process_data_to_database(re_match, website_links):

    # _,_,postgres_user_decoded, postgres_password_decoded = decode_kubernetes_secrets()

    # Define the database connection parameters
    db_params = {
        'host': 'extracting-emails-database.cglvu9svk8cj.us-east-1.rds.amazonaws.com',
        'port': 5432,
        'user': os.environ.get('POSTGRES_USER'),
        'password': os.environ.get('POSTGRES_PASSWORD') 
    }

    # Define the SQL query to insert the data
    insert_query = "INSERT INTO emails (email_address, source_url, created_at) VALUES (%s, %s, %s)"
    # Define the list of email and url tuples to insert
    email_url_set = set([(re_match, website_links)])

    try:
        # Connect to the database and create a cursor object
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Iterate through the email addresses and source URLs and insert them into the table
        for email, url in email_url_set:
            cur.execute(insert_query, (email, url, datetime.now()))

        # Commit the changes
        conn.commit()
        
    except psycopg2.Error as e:
        # Handle any exceptions that occurred during the execution of the above code
        print(f'Error {e.pgcode}: {e.pgerror}')
        
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

