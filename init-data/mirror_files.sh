#!/bin/sh

# Set the MinIO alias
/usr/bin/mc alias set myminio http://minio:9000 minio minio123

# Create the test-bucket bucket if it doesn't exist
/usr/bin/mc mb myminio/test-bucket

# Copy files from the project root to the correct paths in the MinIO bucket
/usr/bin/mc cp /data/binary_classification/reference-income.csv myminio/test-bucket/48c3d064-b86b-437c-83ac-9b54bd5fdf9e/reference/dc929555-7be2-4188-b995-993177c83e8b/
/usr/bin/mc cp /data/binary_classification/current1-income.csv myminio/test-bucket/48c3d064-b86b-437c-83ac-9b54bd5fdf9e/current/35d5c8af-332b-4e88-b302-e20e97c53f34/
/usr/bin/mc cp /data/multiclass-classification/3_classes_reference.csv myminio/test-bucket/b1773457-b858-4b99-ae98-9639c999681a/reference/0fa1749a-e0b1-490c-91db-294db6b62ebe/
/usr/bin/mc cp /data/multiclass-classification/3_classes_current1.csv myminio/test-bucket/b1773457-b858-4b99-ae98-9639c999681a/current/b404a54e-f159-499f-a0c2-edf09c562e3a/
/usr/bin/mc cp /data/regression/regression_abalone_reference.csv myminio/test-bucket/3b9fbe63-6ae4-4907-8fc9-786e8a885992/reference/396d3a6f-fa7a-4c8c-8b0e-25da5c56b743/
/usr/bin/mc cp /data/regression/regression_abalone_current1.csv myminio/test-bucket/3b9fbe63-6ae4-4907-8fc9-786e8a885992/current/0e61138f-ca9a-4502-aa90-4aea64c1a91f/

# Exit the script
exit 0
