---
sidebar_position: 1
---

# Installation

To install the platform you can choose from two different approaches.

* **Using the main repository:** Clone [the main repository](https://github.com/radicalbit/radicalbit-ai-monitoring) and activate the Docker daemon. Finally, run the following command:
  ```bash
  docker compose --profile ui --profile init-data up
  ```
See [README file](https://github.com/radicalbit/radicalbit-ai-monitoring/blob/main/README.md) for further information and details.

* **Using the Python Installer:**  Install the [Python installer](https://pypi.org/project/radicalbit-ai-monitoring/) via `poetry` or `pip`.

  * With poetry:
    1. Clone the repository using  `git clone https://github.com/radicalbit/radicalbit-ai-monitoring-installer.git`.  
    2. Move inside the repository using  `cd radicalbit-ai-monitoring-installer`.
    3. Install poetry using  `poetry install`.

  * With pip: Just run `pip install radicalbit-ai-monitoring`.

  Once you have installed the Python package, activate the Docker daemon and run the following commands:

  ```
  rbit-ai-monitoring platform install
  rbit-ai-monitoring platform up
  ```

After all the containers are up & running, you can go to [http://localhost:5173](http://127.0.0.1:5173/) and play with the platform.
