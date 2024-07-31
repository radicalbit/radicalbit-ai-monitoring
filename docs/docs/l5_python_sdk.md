---
sidebar_position: 1
---

# Python SDK
In this document are exposed all classes implemented inside the [Python SDK](https://pypi.org/project/radicalbit-platform-sdk/). 


### Client

To interact with the Radicalbit AI platform via the SDK, the first thing that must be done is to create the client.
The only required parameter is the `base_url`, which is the URL of the running platform.

```python
from radicalbit_platform_sdk.client import Client

base_url = "http://localhost:9000/"
client = Client(base_url)
```

Once you have a client instance, you can interact with models inside the platform.
ß
The available methods of a client instance are:

* **`create_model(model: CreateModel)`**: it is used to create a brand new model inside the platform.

It requires a [CreateModel](#createmodel) instance and returns the created [Model](#model).

```python
from radicalbit_platform_sdk.models import (
	CreateModel,
	DataType,
	FieldType,
	ModelType,
	ColumnDefinition,
	OutputType,
	Granularity,
	SupportedTypes,
) 

model_definition = CreateModel(
	name="My model",
	modelType=ModelType.BINARY,
	dataType=DataType.TABULAR,
	granularity=Granularity.HOUR,
	features=[
		ColumnDefinition(
			name="first_name", 
			type=SupportedTypes.string, 
			field_type=FieldType.categorical
		),
		ColumnDefinition(
			name="last_name",
			type=SupportedTypes.string,
			field_type=FieldType.categorical
		),
		ColumnDefinition(
			name="age",
			type=SupportedTypes.int,
			field_type=FieldType.numerical
		),
	],
	outputs=OutputType(
		prediction=ColumnDefinition(
			name="prediction", 
			type=SupportedTypes.float, 
			field_type=FieldType.numerical
		),
		output=[
			ColumnDefinition(
				name="adult", 
				type=SupportedTypes.string, 
				field_type=FieldType.categorical
			)
		],
	),
	target=ColumnDefinition(
		name="prediction", 
		type=SupportedTypes.float, 
		field_type=FieldType.numerical
	),
	timestamp=ColumnDefinition(
		name="prediction_timestamp", 
		type=SupportedTypes.datetime, 
		field_type=FieldType.datetime
	),
) 

model = client.create_model(model_definition)
```

* **`get_model()`**: It gets a specific and existing model by its identifier. It requires the id of an existing model and returns the [Model](#model) instance.

```python
model = client.get_model(model_uuid)
```

* **`search_models()`**: It gets a list of models. It returns a list of [Model](#model).

```python
models = client.search_models()
```


### Model

It represents an instance of a monitored model.

The available methods of a model instance are:

* **`uuid()`**: It returns the UUID identifier of the model
* **`name()`**: It returns the name of the model
* **`description()`**: It returns the model’s description, if provided
* **`model_type()`**: It returns the [ModelType](#modeltype)
* **`data_type()`**: It returns the [DataType](#datatype)
* **`granularity()`**: It returns the [Granularity](#granularity) used by metrics aggregation
* **`features()`**: It returns a list of [ColumnDefinition](#columndefinition) representing all the feature definitions
* **`target()`**: It returns a [ColumnDefinition](#columndefinition) representing the ground truth
* **`timestamp()`**: It returns a [ColumnDefinition](#columndefinition) representing the prediction timestamp. This field is used as reconciliation between reference and current datasets
* **`outputs()`**: It returns an [OutputType](#outputtype) representing the model outputs, including prediction and possibly prediction probability fields
* **`frameworks()`**: It returns the used frameworks, if defined
* **`algorithm()`**: It returns the used algorithm, if defined
* **`delete()`**: It deletes the actual model from the platform
* **`update_features(features: List[ColumnDefinition])`**: Update the model features definition if reference dataset is not provided.
* 
* **`load_reference_dataset(file_name: str, bucket: str, object_name: Optional[str] = None, aws_credentials: Optional[AwsCredentials] = None, separator: str = ‘,’)`**: It uploads a reference dataset file to an S3 bucket and then binds it to the model. It returns a [ModelReferenceDataset](#modelreferencedataset). 

Method properties are:
* **`file_name`**: The name of the reference file
* **`bucket`**: The name of the S3 bucket.
* **`object_name`**: The optional name of the object uploaded to S3. Default value is None.
* **`aws_credentials`**: [AwsCredentials](#awscredentials) used to connect to S3 bucket. Default value is None.
* **`separator`**: Optional value to define separator used inside CSV file. Default value is ","

```python
reference_dataset = model.load_reference_dataset(
	file_name="reference.csv", bucket="my-bucket"
)
``` 
 
* **`bind_reference_dataset(dataset_url: str, aws_credentials: Optional[AwsCredentials] = None, separator: str = ‘,’)`**: It binds an existing reference dataset file already uploded to S3 to the model. It returns a [ModelReferenceDataset](#modelreferencedataset). 

Method properties are:

* **`dataset_url`**: The url of the file already uploaded inside S3
* **`aws_credentials`**: [AwsCredentials](#awscredentials) used to connect to S3 bucket. Default value is None.
* **`separator`**: Optional value to define separator used inside CSV file. Default value is ","

```python
reference_dataset = model.bind_reference_dataset(
	dataset_url="s3://my-bucket/reference.csv"
)
```

* **`load_current_dataset(file_name: str, bucket: str, correlation_id_column: Optional[str] = None, object_name: Optional[str] = None, aws_credentials: Optional[AwsCredentials] = None, separator: str = ‘,’)`**: It uploads a current dataset file to an S3 bucket and then bind it to the model. 
It returns a [ModelCurrentDataset](#modelcurrentdataset). 

Method properties are:
* **`file_name`**: The name of the reference file
* **`bucket`**: The name of the S3 bucket.
* **`correlation_id_column`**: The name of the column used for correlation id
* **`object_name`**: The optional name of the object uploaded to S3. Default value is None.
* **`aws_credentials`**: [AwsCredentials](#awscredentials) used to connect to S3 bucket. Default value is None.
* **`separator`**: Optional value to define separator used inside CSV file. Default value is ","

```python
current_dataset = model.load_current_dataset(
file_name="reference.csv",
bucket="my-bucket",
correlation_id_column="prediction_identifier"
)
``` 
 
* **`bind_current_dataset(dataset_url: str, correlation_id_column: str, aws_credentials: Optional[AwsCredentials] = None, separator: str = ‘,’)`**: It binds an existing current dataset file already uploded to S3 to the model. It returns a [ModelCurrentDataset](#modelcurrentdataset). 

Method properties are:
* **`dataset_url`**: The url of the file already uploaded inside S3
* **`correlation_id_column`**: The name of the column used for correlation id
* **`aws_credentials`**: [AwsCredentials](#awscredentials) used to connect to S3 bucket. Default value is None.
* **`separator`**: Optional value to define separator used inside CSV file. Default value is ","

```python
current_dataset = model.bind_current_dataset(
	dataset_url="s3://my-bucket/reference.csv",
	correlation_id_column="prediction_identifier"
)
```

* **`get_reference_datasets()`**: It returns a list of [ModelReferenceDataset](#modelreferencedataset) representing all the current datasets and related metrics
* **`get_current_datasets()`**: It returns a list of [ModelCurrentDataset](#modelcurrentdataset) representing all the current datasets and related metrics


### ModelReferenceDataset
* It represent an instance of uploaded reference dataset.The available methods are:
* **`uuid()`**: the UUID identifier of the uploaded dataset
* **`path()`**: The URL of the dataset in the object storage
* **`date()`**: When dataset was uploaded
* **`status()`**: The status job of the while it is calculating metrics
* **`statistics()`**: If job status is `SUCCEEDED` then returns the dataset statistics
* **`data_quality()`**: If job status is `SUCCEEDED` then returns the data quality metrics of the current dataset
* **`model_quality()`**: If job status is `SUCCEEDED` then returns the model quality metrics of the current dataset


### ModelCurrentDataset
It represents an instance of uploaded current dataset.

The available methods are:

* **`uuid()`**: The UUID identifier of the uploaded dataset
* **`path()`**: The URL of the dataset in the object storage
* **`date()`**: When dataset was uploaded
* **`status()`**: The status job while it is calculating metrics
* **`statistics()`**: If job status is `SUCCEEDED` then returns the dataset statistics
* **`data_quality()`**: If job status is `SUCCEEDED` then returns the data quality metrics of the current dataset
* **`model_quality()`**: If job status is `SUCCEEDED` then returns the model quality metrics of the current dataset
* **`drift()`**: If job status is `SUCCEEDED` then returns the drift metrics of the current dataset


### CreateModel

It contains the definition of a model to be created.

Its properties are:

* **`name`**: The name of the model.
* **`description`**: An optional description to explain something about the model.
* **`model_type`**: The [ModelType](#modeltype) of the model
* **`data_type`**: It explains the [DataType](#datatype) used by the model
* **`granularity`**: The [Granularity](#granularity) of window used to calculate aggregated metrics
* **`features`**: A list of [ColumnDefinition](#columndefinition) representing the features set
* **`outputs`**: An [OutputType](#outputtype) definition to explain the output of the model
* **`target`**: The [ColumnDefinition](#columndefinition) used to represent model’s target
* **`timestamp`**: The [ColumnDefinition](#columndefinition) used to store when prediction was done
* **`frameworks`**: An optional field to describe the frameworks used by the model
* **`algorithm`**: An optional field to explain the algorithm used by the model


### ModelType

Enumeration used to define the type of the model and to calculate the right metrics.
Available values are: `REGRESSION`, `BINARY` and `MULTI_CLASS`.


### DataType

Enumeration used to define the type of data managed by the model.
Available values are: `TABULAR`, `TEXT` and `IMAGE`


### Granularity

Enumeration used to define the granularity used by aggregations inside metrics calculation.
Available values are: `HOUR`, `DAY`, `WEEK` and `MONTH`.


### ColumnDefinition

It contains the definition of a single column inside a dataset.

Its properties are:

* **`name`**: The name of the column
* **`type`**: The [SupportedTypes](#supportedtypes) of the data represented inside this column
* **`field_type`**: The [FieldType](#fieldtype) of the field


### SupportedTypes

Enumeration used to define the available types that a column definition could have.
Available values are: `int`, `float`, `str`, `bool` and `datetime`


### FieldType

Enumeration used to define the categorical type of the field.
Available values are: `categorical`, `numerical` and `datetime`.


### OutputType

It defines the output of the model.

Its properties are:

* **`output`**: A list of [ColumnDefinition](#columndefinition) representing the outputs set
* **`prediction`**: The [ColumnDefinition](#columndefinition) used to represent the prediction
* **`prediction_proba`**: An optional [ColumnDefinition](#columndefinition) used to represent the prediction probability


### AwsCredentials

It defines credentials needed to authenticate to an S3 compatible API service.

Its properties are:

* **`access_key_id`**: Access key ID needed to authenticate to APIs
* **`secret_access_key`**: Secret access key needed to authenticate to APIs
* **`default_region`**: Region to be used
* **`endpoint_url`**: Optional value to define an S3 compatible API endpoint, if different than AWS. By default is `None`
