#!/bin/sh

# Set the MinIO alias
/usr/bin/mc alias set myminio http://minio:9000 minio minio123

# Create the test-bucket bucket if it doesn't exist
/usr/bin/mc mb myminio/test-bucket

# Copy files from the project root to the correct paths in the MinIO bucket
/usr/bin/mc cp /data/binary_classification/reference-income.csv myminio/test-bucket/e02f2aed-cd29-4703-8faf-2dcab9fc668e/reference/ee43cc3d-d71c-43f2-be0b-55da73d509c5/
/usr/bin/mc cp /data/binary_classification/current1-income.csv myminio/test-bucket/e02f2aed-cd29-4703-8faf-2dcab9fc668e/current/63b173f8-6150-41f5-8a6b-a1e08a3a7c12/
/usr/bin/mc cp /data/multiclass-classification/3_classes_reference.csv myminio/test-bucket/756204a0-a6ba-44c2-b287-ca828e2b2441/reference/dd84c147-f6aa-4584-a2dc-3ca4cd00917b/
/usr/bin/mc cp /data/multiclass-classification/3_classes_current1.csv myminio/test-bucket/756204a0-a6ba-44c2-b287-ca828e2b2441/current/658f7c87-b557-4611-a29e-9ae0ae42ded7/
/usr/bin/mc cp /data/regression/regression_abalone_reference.csv myminio/test-bucket/6c48c7e1-442b-4c48-a218-95d07f40a805/reference/12fbe35a-3530-4e26-b53b-ee12dc47a874/
/usr/bin/mc cp /data/regression/regression_abalone_current1.csv myminio/test-bucket/6c48c7e1-442b-4c48-a218-95d07f40a805/current/03616777-0b1e-47ed-b1ad-273dc51d467d/

# Exit the script
exit 0
