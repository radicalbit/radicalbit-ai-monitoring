# Radicalbit Platform Python SDK Examples

Here will be available some tutorials to start to play with the Radicalbit Platform through the Python SDK.

### How to set up ###

The project is based on poetry for managing dependencies.

You should have poetry installed on your local machine. You can follow the instruction on https://python-poetry.org.

After you have poetry installed you can install the project's dependencies run:

```bash
poetry install
```

Then, activate an environment:

```bash
poetry shell
```

If you apply any change in the requirements, don't forget to run the following command:

```bash
poetry update
```


### Tutorials ###

| Task                      | Notebook                                             | Dataset to use                                                                                                | Dataset license                                                                                                                                                                            | Description                                                                                                                             |
|---------------------------|------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| Binary Classification     | notebooks/binary-classification-income-data.ipynb    | data/binary_classification/reference-income.csv,  data/binary_classification/current1-income.csv              | Kohavi,Ron. (1996). Census Income. UCI Machine Learning Repository. https://doi.org/10.24432/C5GP7S. Adapted by Radicalbit.                                                                | In this tutorial we monitor data and performance of a ML used to classify if the income is > 50K given a set of features.               |
| Multiclass Classification | notebooks/multiclass-classification-heart-data.ipynb | data/multiclass-classification/3_classes_reference.csv, data/multiclass-classification/3_classes_current1.csv | Janosi,Andras, Steinbrunn,William, Pfisterer,Matthias, and Detrano,Robert. (1988). Heart Disease. UCI Machine Learning Repository. https://doi.org/10.24432/C52P4X. Adapted by Radicalbit. | In this tutorial we monitor data for a multi-class classification task, in which we classify between 3 different heart disease types.   |
| Regression                | notebooks/regression_abalone.ipynb                   | data/regression/regression_abalone_reference.csv, data/regression/regression_abalone_current1.csv             | Nash,Warwick, Sellers,Tracy, Talbot,Simon, Cawthorn,Andrew, and Ford,Wes. (1995). Abalone. UCI Machine Learning Repository. https://doi.org/10.24432/C55C7W. Adapted by Radicalbit.        | In this tutorial we monitor data for a regression task, in which we compute the number of rings, and therefore the age, of an abalone.  |

