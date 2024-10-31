---
sidebar_position: 3
---

# Reference
The Reference section stores all the information (statistics, model metrics and charts) related to the reference dataset. Throughout the platform, all the reference information is gray-coloured. 


## Data Quality
The **Data Quality** dashboard contains a descriptive analysis of the reference variables. It adapts itself accordingly to the model type and shows information such as:

- Number of observations
- Number of classes (not in regression task)
- Ground Truth Distribution
- Histograms for Numerical Features
- Descriptive Statistics for Numerical Features (average, standard deviation, ranges, percentiles, missing values)
- Bar Charts for Categorical Features
- Descriptive Statistics for Categorical Features(missing values, distinct values, frequencies)

![Alt text](/img/reference/reference-data-quality.png "Reference Data Quality")


## Model Quality

The **Model Quality** dashboard contains all the metrics used to evaluate the model performance. Many of them are computed through the `prediction`/`probability` compared to the `ground truth`. Naturally, the platform computes the proper metrics according to the chosen `Model Type`. 

![Alt text](/img/reference/reference-model-quality.png "Reference Modela Quality")


## Import

The **Import** section lists the path where your reference CSV is stored. If you have a private AWS, the file will be saved in a dedicated S3 bucket otherwise, it will be saved locally with Minio (which shares the same syntax as S3).
To see your reference dataset stored in Minio, visit the address [http://localhost:9091](http://localhost:9091).

![Alt text](/img/reference/reference-import.png "Reference Import")

