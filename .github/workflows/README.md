# Radicalbit OS Platform CI/CD

Here are stored all workflows used to Build/deploy packages and Docker Images for Radicalbit Open Source Platform.

# Convention used

Workflow files are intentionally named as `<service>-<workflow>.yaml` since the workflows themself are triggered only if there are changes in the relative service, and even in the workflow itself.

For example, we need to trigger the SDK workflow, only if there are any changes in the sdk folder or to sdk-workflow.yaml file.

# Local development / testing

It is possible to test workflows in local environment using [act](https://nektosact.com/)

## Prerequisites

- Docker daemon running
- act cli installed

## How To

To view all available jobs to run

```bash
act -l
```

The output should look similar to

```bash
Stage  Job ID    Job name  Workflow name  Workflow file   Events           
0      checkout  checkout  dummy-api-wf   api-dummy.yaml  push,pull_request
0      checkout  checkout  dummy-sdk-wf   sdk-dummy.yaml  push,pull_request
0      checkout  checkout  dummy-ui-wf    ui-dummy.yaml   push,pull_request
```

You can run a given job by specifying the Job ID to act cli

```bash
act -j checkout
```

*Note: if more jobs have the same id, act will run all jobs. To specify a workflow, you can use the `-W <path>` flag:*

```bash
act -j checkout -W .github/workflows/<filename>.yaml
```

### Notes on Docker Actions

Act by default uses a docker image to *"emulate"* the behaviour of a github runner. To use your environment as runner just add the `-P <platform>=self-hosted` flag as shown in the example below:

```bash
act -P ubuntu-22.04=-self-hosted -j checkout -W .github/workflows/<filename>.yaml
```