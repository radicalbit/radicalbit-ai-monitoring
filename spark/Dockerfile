FROM python:3.10.14-slim AS build

WORKDIR /build
COPY poetry.lock pyproject.toml ./
RUN pip install --no-cache-dir poetry==1.8.3 && \
    poetry export -f requirements.txt -o requirements.txt


FROM spark:3.5.1-scala2.12-java17-python3-ubuntu

# Requirements from previous step
COPY --from=build /build/requirements.txt .

# Adding needed jar
RUN curl -o /opt/spark/jars/bcprov-jdk15on-1.70.jar https://repo1.maven.org/maven2/org/bouncycastle/bcprov-jdk15on/1.70/bcprov-jdk15on-1.70.jar && \
    curl -o /opt/spark/jars/bcpkix-jdk15on-1.70.jar https://repo1.maven.org/maven2/org/bouncycastle/bcpkix-jdk15on/1.70/bcpkix-jdk15on-1.70.jar && \
    curl -o /opt/spark/jars/hadoop-aws-3.3.4.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
    curl -o /opt/spark/jars/aws-java-sdk-bundle-1.12.723.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.723/aws-java-sdk-bundle-1.12.723.jar && \
    curl -o /opt/spark/jars/postgresql-42.7.3.jar https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev

# Install requirements coming from pyproject
RUN pip install --no-cache-dir -r requirements.txt

USER spark

# Load pyspark jobs
COPY jobs /opt/spark/custom_jobs

# Set python path for correct module loading
ENV PYTHONPATH "${PYTHONPATH}:/opt/spark/custom_jobs"