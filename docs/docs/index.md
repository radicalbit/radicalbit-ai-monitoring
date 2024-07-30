---
sidebar_position: 1
---

# Introduction
Let's discover the **Radicalbit AI Monitoring Platform** in less than 5 minutes.

## Welcome!
This platform provides a comprehensive solution for monitoring and observing your Artificial Intelligence (AI) models in production.

### Why Monitor AI Models?
While models often perform well during development and validation, their effectiveness can degrade over time in production due to various factors like data shifts or concept drift. The Radicalbit AI Monitor platform helps you proactively identify and address potential performance issues.

### Key Functionalities
The platform provides comprehensive monitoring capabilities to ensure optimal performance of your AI models in production. It analyses both your reference dataset (used for pre-production validation) and the current datasets in use, allowing you to put under control:
* **Data Quality:** evaluate the quality of your data, as high-quality data is crucial for maintaining optimal model performance. The platform analyses both numerical and categorical features in your dataset to provide insights into
    * *data distribution*
    * *missing values*
    * *target variable distribution* (for supervised learning).

* **Model Quality Monitoring:** the platform provides a comprehensive suite of metrics specifically designed at the moment for classification and regression models. \
For classification these metrics include:
    * *Accuracy, Precision, Recall, and F1:* These metrics provide different perspectives on how well your model is classifying positive and negative cases.
    * *False/True Negative/Positive Rates and Confusion Matrix:* These offer a detailed breakdown of your model's classification performance, including the number of correctly and incorrectly classified instances.
    * *AUC-ROC and PR AUC:* These are performance curves that help visualize your model's ability to discriminate between positive and negative classes.

    For regression these metrics include:
   * *Mean Absolute Error, Mean Squared Error, Root Mean Squared Error, R²:* These metrics provide different perspectives on how well your model is predicting a numerical value.
    * *Residual Analysis:* This offers a detailed breakdown of your model's performance, comparing predictions with ground truth and predictions with residuals, i.e. the difference between predictions and ground truth.
* **Model Drift Detection:** analyse model drift, which occurs when the underlying data distribution changes over time and can affect model performance.

### Current Scope and Future Plans
This version focuses on classification, both binary and multiclass, and regression models. Support for additional model types is planned for future releases.
