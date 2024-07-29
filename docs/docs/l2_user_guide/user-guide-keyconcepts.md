---
sidebar_position: 3
---

# Key Concepts

This section introduces the fundamental concepts and terminologies used within the `radicalbit-ai-monitoring` Platform. Understanding these concepts is crucial for the effective utilization of the platform.

## Model Type

The radicalbit-ai-monitoring platform supports various types of models, each suited for different types of tasks:

- **Binary Classification**: Models that categorize data into one of two possible classes (e.g., spam or not spam).
- **Multiclass Classification**: Models that categorize data into one of three or more possible classes (e.g., type of fruit: apple, orange, pear).
- **Regression**: Models that predict a continuous value (e.g., predicting house prices based on various features).

Accordingly to the `Model Type`, the platform will compute specific metrics to evaluate the performance over time.

## Data Type

The platform can handle different types of data, which are crucial for the kind of analysis achieved to evaluate the consistency of the information:

* **Tabular**: Data is organized into a table and saved in CSV format.
* **Text**: Not available yet.
* **Image**: Not available yet.

## Reference Dataset

The reference dataset is a static dataset used as a benchmark for comparison. It represents the ideal or expected data distribution and quality, against which the current dataset's performance and quality are evaluated. This dataset is typically:

- **Historical Data**: Derived from historical data that the model was trained on or validated against. It serves as a baseline to compare new incoming data.
- **Preprocessed**: Cleaned and preprocessed to ensure it represents the best possible version of the data, free from anomalies or errors.
- **Comprehensive**: Should cover all possible scenarios and variations that the model is expected to handle, ensuring it is robust and reliable.
- **Static**: Unlike the current dataset, the reference dataset remains unchanged over time to provide a consistent benchmark for monitoring purposes.

> **_TIP:_** A good example of a reference dataset is the training set.

Using the reference dataset, the platform can:

* **Detect Data Drift**: By comparing the current dataset to the reference dataset, the platform can identify significant deviations in data patterns.
* **Evaluate Model Performance**: The reference dataset provides a baseline for assessing whether the model's performance on new data aligns with its performance on known, reliable data.
* **Ensure Data Quality**: Regularly comparing the current dataset to the reference dataset helps maintain high data quality standards by highlighting inconsistencies and anomalies.

By maintaining a high-quality reference dataset, the `radicalbit-ai-monitoring` platform ensures that any changes in data or model performance can be promptly identified and addressed.

##  Current Dataset

The current dataset is the most recent data being fed into the model for predictions. It should be continuously monitored to ensure consistency with the reference dataset and to detect any anomalies or changes. To achieve this, the current dataset must have the same schema as the reference.

Using the current dataset, the platform can:

- **Monitor Performance Metrics**: Continuously assess how well the model is performing on new data by tracking key metrics such as accuracy, precision, recall and others.
- **Detect Drifts**: Identify unusual patterns or anomalies in the data that may indicate issues with data collection processes or changes in underlying data distributions.
- **Adapt to Changes**: Provide insights into when the model may need retraining or adjustment due to shifts in the data, known as data drift.
- **Ensure Timeliness**: By constantly updating and analyzing the current dataset, the platform ensures that the model's predictions are based on the most up-to-date information available.

By effectively managing and monitoring the current dataset, the `radicalbit-ai-monitoring` platform helps maintain the reliability and accuracy of models in a changing environment.

## Data Quality

Data quality refers to the accuracy, completeness, and reliability of the data used by the models. High data quality is essential for the performance and reliability of the models. The platform monitors various data quality indicators and charts to ensure its integrity:

- **Descriptive Statistics**: Metrics such as mean, median, standard deviation and range are computed to summarize the central tendency and dispersion of the data.
- **Histograms**: Visual representations to identify distributions, outliers, and any potential anomalies in the data.
- **Frequency Distribution**: Charts such as bar plots are used to display the distribution of categories and highlight any imbalances or anomalies.
- **Detect Data Quality Issues**: Identify inaccuracies, inconsistencies, missing values, and outliers in the data.
- **Monitor Changes Over Time**: Track data quality metrics over time to detect any degradation or improvement in data quality.

By incorporating detailed charts and statistics for both numerical and categorical data, the `radicalbit-ai-monitoring` platform ensures comprehensive monitoring and maintenance of data quality, crucial for the robust performance of the models.

## Model Quality

Model quality is a measure of how well a model performs its task. It includes classic metrics such as accuracy, precision, recall and F1 score. The platform evaluates these metrics to ensure the model maintains high performance over time. Naturally, to compute them, the user have to include the ground truth into the dataset.

The model quality changes given the chosen Model Type and thanks to this, it includes the following metrics:

- **Binary Classification**: Accuracy, Precision, Recall, F1 score, Confusion Matrix
- **Multiclass Classification**: Accuracy, Precision, Recall, F1 score, Confusion Matrix
- **Regression**: Mean Absolute Error, Mean Squared Error, Root Mean Squared Error, R², Residual Analysis

The platform provides detailed visualizations and reports for these metrics, allowing users to:

- **Monitor Performance Trends**: Track changes in model performance over time to ensure the model remains effective.
- **Identify Weaknesses**: Pinpoint specific areas where the model may be underperforming, such as particular classes in a classification model or high-error regions in a regression model.
- **Compare Models**: Evaluate and compare the performance of different models or model versions, aiding in model selection and improvement.

By highlighting the differences in evaluation criteria and metrics for various model types, the `radicalbit-ai-monitoring` platform ensures that users can effectively assess and maintain the quality of their models.

## Data Drift

Data drift occurs when the statistical properties of the current dataset differ significantly from the reference dataset. This can affect model performance. The platform monitors for data drift to alert users of potential issues that may require model retraining or adjustment. 

To detect data drift, the platform uses several statistical tests and metrics tailored to the type of data and model:

- **Chi-square Test**: Used primarily for categorical data, this test evaluates whether the distribution of categories in the current dataset significantly differs from the reference dataset. It compares the observed frequencies of categories in the current dataset against the expected frequencies derived from the reference dataset. A significant Chi-square test result indicates that the categorical distribution has changed, signalling potential data drift.
- **2-sample Kolmogorov-Smirnov (KS) Test**: This non-parametric test is used for numerical data to compare the distributions of the reference and current datasets. It evaluates the maximum difference between the cumulative distributions of the two datasets. A significant KS test result indicates that the distributions are different, suggesting data drift. The KS test is sensitive to changes in both the central tendency and the shape of the distribution.
- **Population Stability Index (PSI)**: This metric is used for both categorical and numerical data to quantify the shift in the distribution between the reference and current datasets. PSI measures the divergence between the two distributions, with higher values indicating greater drift. It is particularly useful for identifying gradual changes over time. PSI is calculated by dividing the data into bins and comparing the relative frequencies of each bin between the reference and current datasets.

Using these tests and metrics, the platform can:

- **Detect Significant Changes**: Identify when the current data distribution has shifted enough to potentially impact model performance.
- **Trigger Alerts**: Notify users when significant data drift is detected, allowing for timely intervention.
- **Guide Retraining**: Provide insights into which specific features or aspects of the data have drifted, helping to guide model retraining efforts.
- **Visualize Drift**: Offer visual representations of the drift, such as distribution plots and bar charts, to help users understand the nature and extent of the drift.

By employing these methods, the `radicalbit-ai-monitoring` platform ensures comprehensive monitoring for data drift, helping maintain the reliability and accuracy of the models in a changing data environment.