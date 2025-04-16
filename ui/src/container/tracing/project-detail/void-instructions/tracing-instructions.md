

The platform utilizes [OpenLLMetry](https://github.com/traceloop/openllmetry), an open-source library specifically designed for tracing LLM applications. Our system collects trace data through an OpenTelemetry collector, which then processes and visualizes the information in the Radicalbit AI Platform.

The Traceloop SDK in the project that needs to be monitored must be configured as follows at the beginning of the code:

```python
from traceloop.sdk import Traceloop

Traceloop.init(
    api_endpoint="http://localhost:9000/api/otel",
    api_key="<YOUR_API_KEY>" # Replace with your actual API key
)
```

### Session Management

To properly group traces by conversation or interaction thread, you must set a `session_uuid` for each distinct chat session:

```python
import uuid

# Generate a new session UUID at the beginning of each chat/thread
session_uuid = uuid.uuid4()
Traceloop.set_association_properties({"session_uuid": str(session_uuid)})
```

**Important**: Generate a new UUID for each new conversation thread to ensure proper trace grouping.