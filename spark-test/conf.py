def create_secrets():
    return {
        "AWS_ACCESS_KEY_ID": "minio",
        "AWS_SECRET_ACCESS_KEY": "minio123",
        "AWS_REGION": "us-east-1",
        "S3_ENDPOINT_URL": "http://minio:9000",
        "POSTGRES_URL": "jdbc:postgresql://postgres:5432/radicalbit",
        "POSTGRES_DB": "radicalbit",
        "POSTGRES_HOST": "postgres",
        "POSTGRES_PORT": "5432",
        "POSTGRES_USER": "postgres",
        "POSTGRES_PASSWORD": "postgres",
        "POSTGRES_SCHEMA": "public",
    }
