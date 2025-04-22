---
sidebar_position: 5
---

# All metrics
List of all available Metrics and Charts.

## CSV summary

* Number of variables
* Number of observations
* Number of missing values
* Percentage of missing values
* Number of duplicated rows
* Percentage of duplicated rows
* Number of **numerical** variables
* Number of **categorical** variables
* Number of **datetime** variables

Summary with all variable name and type (float, int, string, datetime).

## Data quality

* **Numerical** variables
  * Average
  * Standard deviation
  * Minimum
  * Maximum
  * Percentile 25%
  * Median
  * Percentile 75%
  * Number of missing values
  * Histogram with 10 bins
* **Categorical** variables
  * Number of missing values
  * Percentage of missing values
  * Number of distinct values
  * For each distinct value:
    * count of observations
    * percentage of observations
* **Ground truth**
  * if categorical i.e. for a classification model: bar plot *(for both reference and current for an easy comparison)*
  * if numerical, i.e. for a regression model: histogram with 10 bins *(for both reference and current for an easy comparison)*

## Model quality

* Classification model
  * Number of classes
  * Accuracy *(for both reference and current for an easy comparison)*
  * Line chart of accuracy over time
  * Confusion matrix
  * Log loss, *only for binary classification at the moment*
  * Line chart of log loss over time, *only for binary classification at the moment*
  * For each class:
    * Precision *(for both reference and current for an easy comparison)*
    * Recall *(for both reference and current for an easy comparison)*
    * F1 score *(for both reference and current for an easy comparison)*
    * True Positive Rate *(for both reference and current for an easy comparison)*
    * False Positive Rate *(for both reference and current for an easy comparison)*
    * Support *(for both reference and current for an easy comparison)*
* Regression model
  * Mean squared error *(for both reference and current for an easy comparison)*
  * Root mean squared error *(for both reference and current for an easy comparison)*
  * Mean absolute error *(for both reference and current for an easy comparison)*
  * Mean absolute percentage error *(for both reference and current for an easy comparison)*
  * R-squared *(for both reference and current for an easy comparison)*
  * Adjusted R-squared *(for both reference and current for an easy comparison)*
  * Variance *(for both reference and current for an easy comparison)*
  * Line charts for all of the above over time
  * Residual analysis:
    * Correlation prediction/ground_truth
    * Residuals plot, i.e, scatter plot for standardised residuals and predictions
    * Scatter plot for predictions vs ground truth and linear regression line
    * Histogram of the residuals
    * Kolmogorov-Smirnov test of normality for residuals
* Text generation
  * Probability: In language modeling, probability refers to the likelihood that the model assigns to a specific sequence of text occurring.

  * Perplexity: Perplexity is a standard metric that measures how "surprised" or uncertain the model is when predicting the text sequence. 

## Data Drift

Data drift for all features using different algorithms depending on the data type: float, int, categorical. We use the following algorithms (but others will be added in the future):
- Numerical: 
  * [Two-Sample Kolmogorov-Smirnov](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test#Two-sample_Kolmogorov%E2%80%93Smirnov_test)
  * [Population Stability Index](https://scholarworks.wmich.edu/dissertations/3208/)
  * [Wasserstein Distance](https://en.wikipedia.org/wiki/Wasserstein_metric)
  * [Jensen Shannon Divergence](https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence)
  * [Hellinger Distance](https://en.wikipedia.org/wiki/Hellinger_distance)
  * [Kullback Leibler Divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)
- Categorical:
  * [Chi-Square Test](https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test)
  * [Jensen Shannon Divergence](https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence)
  * [Kullback Leibler Divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)
  * [Hellinger Distance](https://en.wikipedia.org/wiki/Hellinger_distance)
