---
sidebar_position: 4
---

# Settings

The **Settings** section provides essential information for integrating the tracing functionality into your application via the SDK, as well as options for managing the current project itself.

This page contains the following key areas:

### SDK Integration & Initialization

This part introduces the underlying technology (mentioning OpenLLMetry and Open Telemetry) and provides the necessary instructions to configure the Traceloop SDK within your application code.

* **Initialization Code:** A crucial Python code snippet demonstrates how to initialize the `Traceloop` library:

    ```python
    from traceloop.sdk import Traceloop

    Traceloop.init(
        api_endpoint="http://localhost:9000/api/otel",
        api_key="<YOUR_API_KEY>" # Replace with your actual API key
    )
    ```

    * **`api_endpoint`**: Specifies the URL where the telemetry data (traces, spans) must be sent.
    * **`api_key`**: Use an API key for authentication. You can either generate a new key in the 
    API key management section or use the default key provided when the project was initially created.

![Alt text](/img/quickstart/tracing_settings.png "Settings")

### API Key Management

Within the Settings section, you can manage the API keys required for your application's SDK to securely connect and send data to the platform. This area displays a list of your current API keys,
showing their user-defined name, a portion of the key itself for identification, and the creation date.
You have options to generate new keys using the '+' button and revoke existing ones by deleting them using the trash bin icon, allowing you to control application access and rotate credentials as needed.

![Alt text](/img/tracing/tracing_settings_api.png "Settings")

You can manage the project by selecting the **ellipsis icon** (...). Here you can:

* Change the project name
* Delete the project

