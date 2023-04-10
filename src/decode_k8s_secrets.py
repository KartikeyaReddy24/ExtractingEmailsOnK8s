from kubernetes import client, config
import base64

def decode_kubernetes_secrets(access_key_decoded, secret_key_decoded, postgres_user_decoded, postgres_password_decoded, postgres_db_name_decoded):
    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create a Kubernetes API client
    api_client = client.CoreV1Api()

    # Specify the name and namespace of the secret containing the AWS credentials
    secret_name = 'aws-credentials'
    namespace = 'default'

    # Read the contents of the secret
    secret = api_client.read_namespaced_secret(secret_name, namespace)

    # Decode the base64-encoded access key and secret key values
    access_key_decoded = base64.b64decode(secret.data['access-key-id']).decode('utf-8')
    secret_key_decoded = base64.b64decode(secret.data['secret-access-key']).decode('utf-8')

    secret_name = 'postgresdb-credentials'
    namespace = 'default'

    # Read the contents of the secret
    secret = api_client.read_namespaced_secret(secret_name, namespace)

    # Decode the base64-encoded access key and secret key values
    postgres_user_decoded = base64.b64decode(secret.data['postgres-user']).decode('utf-8')
    postgres_password_decoded = base64.b64decode(secret.data['postgres-password']).decode('utf-8')
    postgres_db_name_decoded = base64.b64decode(secret.data['postgres-dbname']).decode('utf-8')


    return access_key_decoded, secret_key_decoded, postgres_user_decoded, postgres_password_decoded, postgres_db_name_decoded  
