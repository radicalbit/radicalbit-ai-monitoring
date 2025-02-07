---
sidebar_position: 2
---

# Charts SDK
This document defines the `RadicalBitChart` class, which is responsible for generating various charts to visualize model quality and data distribution. 

The class includes methods to create linear charts for metrics like recall, F1 score, precision, false positive rate, true positive rate, confusion matrices, AUC-ROC, PR-AUC, and more. 

Additionally, it provides methods to display the distribution of numerical features and generates residual plots for regression models.


## Global Methods
Every methods listed below return a list of `EChartsRawWidget`, responsible of chart render into a notebook.

These methods recognize the `model_type` directly from the model passed as an argument, so they show the list of available graphs in to the model type.

* **`data_quality(data=RbitChartData) -> List[EChartsRawWidget]`**
	
	Combines distribution and numerical feature charts to provide an overall view of data quality.

	```python
	from radicalbit_platform_sdk.client import Client
	from radicalbit_platform_sdk.charts import RadicalbitChart, RbitChartData

	base_url = "http://localhost:9000"
	client = Client(base_url)
	model = client.get_model(id="e02f2aed-cd29-4703-8faf-2dcab9fc668e")

	ref = model.get_reference_datasets()[0]
	cur1 = model.get_current_datasets()[0]

	RadicalbitChart().data_quality(data=RbitChartData(
		model=model,
		reference=ref,
		current=cur1
	))

	```

* **`model_quality(data=RbitChartData) -> List[EChartsRawWidget\`**
	
	Generates a comprehensive set of charts to assess the performance and predictive accuracy of models, including linear charts for metrics like precision, recall, F1 score, and confusion matrices.

	```python
	from radicalbit_platform_sdk.client import Client
	from radicalbit_platform_sdk.charts import RadicalbitChart, RbitChartData

	base_url = "http://localhost:9000"
	client = Client(base_url)
	model = client.get_model(id="e02f2aed-cd29-4703-8faf-2dcab9fc668e")

	ref = model.get_reference_datasets()[0]
	cur1 = model.get_current_datasets()[0]

	RadicalbitChart().model_quality(data=RbitChartData(
		model=model,
		reference=ref,
		current=cur1
	))

	```


## Common Methods

* **`distribution_chart(data=RbitChartData) -> EChartsRawWidget`**

	Creates a chart showing the distribution of numerical features in the dataset.

	![Alt text](/img/chart-sdk/Distribution.png "Distribution")

* **`numerical_feature_chart(data=RbitChartData) -> EChartsRawWidget`**

	Similar to `distribution_chart`, but specifically for numerical feature analysis.

	![Alt text](/img/chart-sdk/NumericalFeature.png "Numerical Feature")

* **`confusion_matrix(data=RbitChartResidualData) -> EChartsRawWidget`**

	Generates a confusion matrix visualization to evaluate the performance of a classification model, either current or reference based on available data.

	![Alt text](/img/chart-sdk/ConfusionMatrix.png "Confusion Matrix")

## Binary Classification

* **`accuracy_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Generates a linear chart depicting accuracy metrics.

	![Alt text](/img/chart-sdk/Accuracy.png "Accuracy")

* **`precision_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Shows precision metrics in a linear chart format.

	![Alt text](/img/chart-sdk/Precision.png "Precision")

* **`recall_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Displays recall metrics on a linear chart.

	![Alt text](/img/chart-sdk/Recall.png "Recall")

* **`f1_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Generates a linear chart for F1 scores, which is a combination of precision and recall.

	![Alt text](/img/chart-sdk/F1.png "F1")

* **`true_positive_rate_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Shows true positive rates on a linear chart.

	![Alt text](/img/chart-sdk/TruePositiveRate.png "True Positive Rate")

* **`false_positive_rate_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Displays false positive rates in a linear chart format.
	
	![Alt text](/img/chart-sdk/FalsePositiveRate.png "False Positive Rate")

* **`log_loss_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Generates a linear chart for log loss, which is used to measure the performance of classification models where the prediction values are probabilities.

	![Alt text](/img/chart-sdk/LogLoss.png "Log Loss")

* **`auc_roc_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Shows AUC-ROC (Area Under the Receiver Operating Characteristic Curve) metrics in a linear chart.

	![Alt text](/img/chart-sdk/AUC-ROC.png "AUC-ROC")

* **`pr_auc_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Displays PR-AUC (Precision Recall Area Under the Curve) on a linear chart.

	![Alt text](/img/chart-sdk/PR-AUC.png "PR-AUC")

## Multi Classification

* **`multiclass_recall_chart(data=RbitChartLinearData)`**

	Generates a linear chart displaying recall metrics for each class in a multi-class classification model.

	![Alt text](/img/chart-sdk/MulticlassRecall.png "Multiclass Recall")

* **`multiclass_f1_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Creates a linear chart showing the F1 score for each class in a multi-class classification model.

	![Alt text](/img/chart-sdk/MulticlassF1.png "Multiclass F1")

* **`multiclass_precision_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Generates a linear chart illustrating precision metrics for each class in a multi-class classification model.

	![Alt text](/img/chart-sdk/MulticlassPrecision.png "Multiclass Precision")

* **`multiclass_false_positive_rate_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Produces a linear chart that shows the false positive rate for each class in a multi-class classification model.

	![Alt text](/img/chart-sdk/MulticlassFalsePositiveRate.png "Multiclass False Positive Rate")

* **`multiclass_true_positive_rate_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Displays a linear chart of true positive rates across different classes in a multi-class setting.

## Regression

* **`predicted_actual_chart(data=RbitChartResidualData) -> EChartsRawWidget`**

	Generates a chart comparing predicted vs actual values for regression models.

	![Alt text](/img/chart-sdk/PredictedActual.png "Predicted Actual")

* **`residual_scatter_chart(data=RbitChartResidualData) -> EChartsRawWidget`**

	Shows the scatter plot of residuals to assess homoscedasticity in regression models.

	![Alt text](/img/chart-sdk/ResidualsPlot.png "Residual Plot")

* **`residual_bucket_chart(data=RbitChartResidualData) -> EChartsRawWidget`**

	Displays a chart where residuals are grouped and visualized, useful for understanding distribution patterns.

	![Alt text](/img/chart-sdk/Residuals.png "Residual bucket")

* **`mse_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Generates a linear chart for Mean Squared Error in regression models.

	![Alt text](/img/chart-sdk/MSE.png "MSE")

* **`rmse_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Shows the Root Mean Squared Error on a linear chart, which is another metric used to evaluate regression models.

	![Alt text](/img/chart-sdk/RMSE.png "RMSE")

* **`mae_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Displays Mean Absolute Error in a linear chart format for regression analysis.

	![Alt text](/img/chart-sdk/MAE.png "MAE")

* **`mape_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Generates a linear chart for Mean Absolute Percentage Error, which is useful for assessing the accuracy of predicted values relative to actual values in regression models.

	![Alt text](/img/chart-sdk/MAPE.png "MAPE")

* **`r2_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Shows R² (coefficient of determination) on a linear chart, indicating how well the model fits the data.

	![Alt text](/img/chart-sdk/Rsquared.png "R-Squared")

* **`adj_r2_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Displays adjusted R², which is useful for penalizing models that include too many explanatory variables relative to the number of observations.

	![Alt text](/img/chart-sdk/AdjRSquared.png "Adj R-Squared")

* **`variance_linear_chart(data=RbitChartLinearData) -> EChartsRawWidget`**

	Generates a linear chart for variance in regression analysis.

	![Alt text](/img/chart-sdk/Variance.png "Variance")
