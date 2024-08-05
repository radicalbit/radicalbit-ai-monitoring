# Release Process

This document outlines the steps to release the project. Follow these guidelines to ensure a smooth and consistent release process.

# Steps to Release

## Create the release PR

We use the [release-please](https://github.com/googleapis/release-please-action) GitHub Action to perform the release. Below you can find the configuration that we use into this repository:

* [workflow manifest](.github/workflows/release-please.yaml)
* [action configuration](.github/release-config.json)

Manually invoke the release-please [workflow](https://github.com/radicalbit/radicalbit-ai-monitoring/actions/workflows/release-please.yaml). The outcome will be the creation of a release PR, that will include the updates to be released, along with the updated [CHANGELOG.md](./CHANGELOG.md) file.

![alt text](manually-invoke-release-please.png)  

The new release will follow the [semver](https://semver.org) specificationRelease plese will determine the upcoming version bump by parsing the githistoryof the `main` branch, looking for [Conventional Commits](https:/wwwconventionalcommits.org/) messages.

## (Optional) Update docs version
We use [Docusaurus](https://docusaurus.io) for our documentation. If needed, we must add a new [documentation version](https://docusaurus.io/docs/versioning) created after the same semver tag that will be used for the release.

For example, if we were going to release the `v1.2.3` version of the application along updates to its documentation, we would have to release a `v1.2.3` documentation version that will be included into the docs site "version dropdown"

![alt text](image.png)

To create a new documentation version, please manually invoke the corresponding [workflow](https://github.com/radicalbit/radicalbit-ai-monitoring/actions/workflows/prepare-docs-for-release.yaml) passing two params:

* `version`: the documentation version that will be created. Must be the same version of the upcoming application release (`v1.2.3` if we were following the previous example)
* `release-branch`: must be the string `release-please--branches--main` as it's a conventional/default branch name that is used by release-please

Please be aware that both inputs will be validated, so you could get errors depending on input passed.

## Perform the release
To perform the release, you must again invoke the release-please [workflow](https://github.com/radicalbit/radicalbit-ai-monitoring/actions/workflows/release-please.yaml). Please carefully check that everything is in order before doing that, as this action will:

* merge the release PR on `main` branch
* create/push a Git tag that follows the determined semver version i.e. `v1.2.3`
* invoke all github actions that will publish the newly tagged artifacts where necessary i.e. Docker Hub, PyPi, etc. etc.