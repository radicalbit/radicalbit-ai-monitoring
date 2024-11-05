# Release Process

This document outlines the steps required to release the project. Currently, the release process is "semi-automatic," involving the following procedures.

Adhering to these steps will ensure a smooth and seamless release flow.

# Steps to Release

## Create the release PR

We use the [release-please](https://github.com/googleapis/release-please-action) GitHub Action to perform releases. Configuration details can be found in the following manifests:

* [workflow manifest](.github/workflows/release-please.yaml)
* [action configuration](.github/release-config.json)

Begin by manually triggering the release-please [workflow](https://github.com/radicalbit/radicalbit-ai-monitoring/actions/workflows/release-please.yaml). This will generate a release PR that includes the updates for release along with the updated [CHANGELOG.md](./CHANGELOG.md) and [version.txt](./version.txt) files. 

**Please ensure that the newly created PR has the `autorelease: pending` label.**

![manually-invoke-release-please](https://github.com/user-attachments/assets/d0245757-c9fc-44b0-bb59-8d91ec23ec1b)

The new release will adhere to the [semver](https://semver.org) specification: release-please will determine the upcoming version bump by parsing the git history of the `main` branch, looking for [Conventional Commits](https:/wwwconventionalcommits.org/) messages.

## (Optional) Update semver version to release
If for some reason there is the need to change the semver version that is going to be released, it's sufficient to update the content of the release PR with the desired semver version and adapt the changelog accordingly.

## (Optional) Update docs version
We use [Docusaurus](https://docusaurus.io) for our documentation. If necessary, add a new [documentation version](https://docusaurus.io/docs/versioning) corresponding to the same semver tag as the upcoming release.

For instance, if releasing version `v1.2.3` of the application that carries updates to its documentation, you should also release a `v1.2.3` documentation version that will be included in the docs site "version dropdown"

![image](https://github.com/user-attachments/assets/e60a4108-8b7d-424a-b11e-a8e44437b258)

To create a new documentation version, manually invoke the related [workflow](https://github.com/radicalbit/radicalbit-ai-monitoring/actions/workflows/prepare-docs-for-release.yaml) with the following parameters:

* `version`: the documentation version to be created, matching the application release version (e.g., `v1.2.3`).
* `release-branch`: use `release-please--branches--main` as the branch name.

Both inputs will be validated, so errors may occur depending on the provided inputs.

## Merge the release PR
Merge the release PR to prepare for the tagged release. **Note that this action does not create a tagged release**; that will occur in the next step.


## Perform the release
To finalize the release, manually trigger the release-please [workflow](https://github.com/radicalbit/radicalbit-ai-monitoring/actions/workflows/release-please.yaml) again. Ensure everything is correct before proceeding, as this step will:

* create and push a Git tag following the determined semver version (e.g., `v1.2.3`).
* invoke all github actions that will publish the newly tagged artifacts i.e. Docker Hub, PyPi, etc. etc.
* update the release PR label from `autorelease: pending` to `autorelease: tagged`.
