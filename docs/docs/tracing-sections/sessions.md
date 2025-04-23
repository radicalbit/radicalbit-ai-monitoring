---
sidebar_position: 3
---

# Sessions

The **Sessions** section allows you to group and analyze sequences of interactions, typically corresponding to a single user's engagement with your application over a period.

### What is a Session?

A **Session** groups together multiple related **Traces**. Think of it as a container for a complete user conversation or workflow. For example, if a user interacts multiple times with a chatbot (asking questions, getting responses), all the individual requests (traces) made during that interaction can be linked together under a single Session ID.

Grouping traces into sessions is useful for:

* Analyzing a user's complete journey or conversation flow.
* Calculating aggregate metrics (like total tokens or errors) across an entire interaction.
* Debugging issues that might span multiple requests within a single user engagement.
* Understanding how users interact with your application over time.

### The Sessions List View

This view provides a list of all recorded sessions, summarizing the activity within each one.


![Alt text](/img/tracing/sessions.png "Sessions summary")

**Session Information:**

Each row in the table represents a single session and provides aggregated information:

* **UUID:** The unique identifier for this specific session.
* **Traces:** The total number of individual traces that have been associated with this session.
* **Errors:** The total count of traces *within this session* that contained one or more errors. This helps quickly identify sessions where users might have encountered problems.
* **Completion tokens:** The sum of completion tokens across *all* traces belonging to this session.
* **Prompt tokens:** The sum of prompt tokens across *all* traces belonging to this session.
* **Total Tokens:** The grand total of tokens (prompt + completion) consumed during the entire session, indicating the overall LLM cost or usage for that interaction.
* **Created at:** The timestamp when the first trace associated with this session was recorded.
* **Last Trace at:** The timestamp of the most recent trace recorded within this session, indicating the time of the last activity.

From this list, you can typically click on a session's UUID to drill down further, often leading you to a filtered view of the Traces list showing only the traces belonging to that selected session.

> **Note:**     Human-in-the-loop within LangGraph, it may lead to an error.