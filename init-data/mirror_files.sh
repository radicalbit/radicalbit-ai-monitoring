#!/bin/sh

# Set the MinIO alias
/usr/bin/mc alias set myminio http://minio:9000 minio minio123

# Create the test-bucket bucket if it doesn't exist
/usr/bin/mc mb myminio/test-bucket

# Copy files from the project root to the correct paths in the MinIO bucket
/usr/bin/mc cp /data/binary_classification/reference-income.csv myminio/test-bucket/e02f2aed-cd29-4703-8faf-2dcab9fc668e/reference/db15546e-16a3-4482-8317-323d66dbe409/
/usr/bin/mc cp /data/binary_classification/current1-income.csv myminio/test-bucket/e02f2aed-cd29-4703-8faf-2dcab9fc668e/current/b73334fb-aac0-400c-9103-fe894e13bd95/
/usr/bin/mc cp /data/multiclass-classification/3_classes_reference.csv myminio/test-bucket/756204a0-a6ba-44c2-b287-ca828e2b2441/reference/d8cb36a9-2f8b-4e45-bab0-aeaa259a9f46/
/usr/bin/mc cp /data/multiclass-classification/3_classes_current1.csv myminio/test-bucket/756204a0-a6ba-44c2-b287-ca828e2b2441/current/dda74c14-91de-4ae8-a432-3a2f8ccdd153/
/usr/bin/mc cp /data/regression/regression_abalone_reference.csv myminio/test-bucket/6c48c7e1-442b-4c48-a218-95d07f40a805/reference/6ae1390e-656a-45aa-acd4-6f6b38e6acf4/
/usr/bin/mc cp /data/regression/regression_abalone_current1.csv myminio/test-bucket/6c48c7e1-442b-4c48-a218-95d07f40a805/current/edb6ed6c-6e2d-44fa-8a60-40540aec9c03/

# Exit the script
exit 0
