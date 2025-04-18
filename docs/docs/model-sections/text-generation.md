---
sidebar_position: 5
---

# Text generation
The Text Generation section is dedicated to monitoring and analyzing the outputs of your text generation models. It helps you understand the performance and characteristics of the generated text.

> NOTE: in this section, you will always see the last uploaded text generation data. In case you need previous analysis, you can browse among them in the `Import` section.

## Model Quality / Overview

The main dashboard for analyzing text generation model quality provides both summary statistics and detailed examples.

Key components include:

* **Overall Metrics**: Presents high-level indicators calculated across the entire file:    
    - **Number of sentences** (7) 
    - **Perplexity overall** (1.22)
    - **Probability overall** (0.896).
* **Detailed Sequence List**: Shows individual generated sequences with associated metrics (Perplexity, Probability), model details (`gpt-4o-2024-08-06`) and part of the generated text. Tokens within the text are often highlighted to indicate specific properties.
* **Filtering Capabilities**: Allows users to filter the sequence list based on specific tokens.

![Alt text](/img/text_generation/overview.png "Text Generation Model Quality / Overview")

## Model Detail

By expanding one of the cards containing a phrase, you will be able to see more details, such as:

* **Individual Generation Details**: Here you can analyze the entire generated text itself. Tokens within the text might be highlighted (e.g., in green, yellow, red) potentially indicating prediction confidence, probability levels, or other linguistic features.
* **Visualization**: A bar chart at the bottom provides a visual representation of certain data points, possibly showing the distribution of probabilities scores across tokens within a selected sequence.

![Alt text](/img/text_generation/detail.png "Text Generation Model Quality Detail")

## Import

The **Import** section lists the path where your completions JSONs are stored. If you have a private AWS, the files will be saved in a dedicated S3 bucket otherwise, they will be saved locally with Minio (which shares the same syntax as S3).
To see your text generation files stored in Minio, visit the address [http://localhost:9091](http://localhost:9091).

Here, you can browse between all the text generation files you have uploaded over time.

![Alt text](/img/text_generation/import.png "Text Generation Import")

