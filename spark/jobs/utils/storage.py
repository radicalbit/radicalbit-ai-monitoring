import os


def configure_storage(spark_context):
    backend = os.getenv('STORAGE_BACKEND', 'minio')
    hadoop_conf = spark_context._jsc.hadoopConfiguration()

    if backend == 'gcs':
        hadoop_conf.set('fs.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem')
        hadoop_conf.set(
            'fs.AbstractFileSystem.gs.impl',
            'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS',
        )
        hadoop_conf.set('fs.gs.project.id', os.getenv('GCS_PROJECT_ID', ''))
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if creds_path:
            hadoop_conf.set('google.cloud.auth.type', 'SERVICE_ACCOUNT_JSON_KEYFILE')
            hadoop_conf.set('google.cloud.auth.service.account.json.keyfile', creds_path)
        else:
            hadoop_conf.set('google.cloud.auth.type', 'APPLICATION_DEFAULT')
    else:
        hadoop_conf.set('fs.s3a.access.key', os.getenv('AWS_ACCESS_KEY_ID'))
        hadoop_conf.set('fs.s3a.secret.key', os.getenv('AWS_SECRET_ACCESS_KEY'))
        hadoop_conf.set('fs.s3a.endpoint.region', os.getenv('AWS_REGION'))
        endpoint = os.getenv('S3_ENDPOINT_URL')
        if endpoint:
            hadoop_conf.set('fs.s3a.endpoint', endpoint)
            hadoop_conf.set('fs.s3a.path.style.access', 'true')
            if endpoint.startswith('https://'):
                hadoop_conf.set('fs.s3a.connection.ssl.enabled', 'true')
                hadoop_conf.set('fs.s3a.connection.ssl.cert-check', 'false')
            elif endpoint.startswith('http://'):
                hadoop_conf.set('fs.s3a.connection.ssl.enabled', 'false')
