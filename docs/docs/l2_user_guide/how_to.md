---
sidebar_position: 3
---

# Hands-On Guide

In ths guide we are focusing on how to use the GUI.

If you prefer to do everything using our SDK please refer to our [SDK Quickstarts](https://github.com/radicalbit/radicalbit-ai-monitoring/tree/main/docs/quickstarts).

## How to create a model

* From the Model main page ![Alt text](/img/how_to/new_model_step1.png "New model step 1")
click on the plus sign in the top right corner.

* Fill up the name of the model, the model type (at the moment only `Binary Classification` `Multiclass Classification` and `Regression` are available), the time granularity on which aggregations are computed (`Hour`, `Day`, `Week` or `Month`), and eventually (optional fields) Framework (e.g. scikit-learn) and Algorithm (e.g. KNeighborsClassifier), and then click `Next`
![Alt text](/img/how_to/new_model_step2.png "New model step 2")

* Upload a CSV file containing *all features*, *prediction*, eventually *prediction probability*, *ground truth* (i.e. the correct value for the set of feature that the model should predict), and a *timestamp* (we use it as a UUID for each row). At this stage a very small CSV file, about 10 rows, suffices, since we use it just to create a schema, input and output signatures for the model. If you prefer to upload your whole reference dataset this is perfectly fine, of course.

* Since your CSV file can contain fields you are not interested in monitoring, e.g. some custom UUID, you can choose the fields to carry forward ![Alt text](/img/how_to/new_model_step3.png "New model step 3")

* Next choose your `Target`, `Prediction`, `Timestamp` and, if present, `Prediction Probability` fields.

## Change field type

In your CSV file there might be some numerical variables which are actually categorical: for instance you might have the feature `Gender` which has values `{0,1}`: so we automatically infer it as an integer variables but clearly it makes no sense to compute numerical statistics on it, ince it is clearly the representation of a categorical feature. \
Hence, **as long as no reference dataset has been loaded yet**, in the `Overview` section, `Variables` tab, you are allowed to change the field type of any numerical feature to categorical.
![Alt text](/img/how_to/change_field_type.png "Change field type")

Please note that as soon as a reference dataset is loaded into the platform **this option is no longer available** because we are starting right away computing statistics and metrics on the variables according to their type.

## Load a reference dataset

Go to the `Reference` entry of the vertical navigation bar ![Alt text](/img/how_to/reference.png "Import Reference") click `Import Reference` and choose the right CSV file.

## Load a Current Dataset

* If no Current dataset has been published yet, just go to the `Current` entry of the vertical navigation bar ![Alt text](/img/how_to/first_current.png "Import First Current") click `Import Current` and choose the right CSV file.

* If some current dataset have already been imported and you want to add an extra one, go to the `Current` entry of the vertical navigation bar, then on the `Import` tab ![Alt text](/img/how_to/more_current.png "Import More Current")
click `Import Current` and choose the right CSV file.

