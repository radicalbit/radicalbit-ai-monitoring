# Changelog

## [0.8.2](https://github.com/radicalbit/radicalbit-ai-monitoring/compare/v0.8.1...v0.8.2) (2024-06-28)

### Bug Fixes

* dockerfile ui environment variables ([#40](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/40)) ([15f8bbe](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/15f8bbe157a0d2ffe77ebdf1f6cc4075fe473da3))
* manage types for all the fiels ([#47](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/47)) ([64218fa](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/64218fa618d626b5ed2acbc9b6a695c969203a65))
* **ui:** Improve polling and other fixies ([#36](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/36)) ([951905f](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/951905fe008651f9afa6f57eeb5462470d764cff))

### Chores

* add latest reference and current uuids to modelOut dto ([#32](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/32)) ([f8fdb5a](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/f8fdb5afcd94ffbf2e2e83d46d9f10b7403b352e))
* add statistics for multiclassification + refactoring and improvements ([#35](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/35)) ([18588ea](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/18588eab6894275c2e29e20a9ea7d5b74b34d142))
* allow to select the modelType and update the valid types prediction array ([#43](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/43)) ([0c2ad1a](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/0c2ad1ae860a17290f0c96c18b132e1cf977a61c))
* **api:** get all reference/current datasets not paginated ([#26](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/26)) ([6967044](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/696704485683f081436818cf52aed117c1ec81d7))
* change type from secondary-light to primary ([#42](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/42)) ([f2af815](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/f2af8153c30cbd8491cd94414cddc8ab72d759b1))
* data quality for multiclass + fix class metrics ([#41](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/41)) ([7cc870a](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/7cc870ad0afad5581065128d91ee5241e7a71002))
* fix binary ([#48](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/48)) ([1a66a72](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/1a66a721e30e26526324b95e257ead5df24aa1cf))
* get all models not paginated ([#27](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/27)) ([06bd2ef](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/06bd2ef7cb63a362e8f9091fee439794cbdde8d0))
* refactoring of metrics part ([#38](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/38)) ([6cb8bbe](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/6cb8bbef4cbfcfa588c34fe4636d2d1c4b64934d))
* **sdk:** added ability to set S3 endpoint url if needed ([#34](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/34)) ([c6a8f14](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/c6a8f1406c928de70bb1192329d62a7dc3f784e6))
* **sdk:** get all reference and current datasets ([#31](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/31)) ([5b1832d](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/5b1832d1b7558cc94ae29d58f0a93cb62f0949bb))
* **ui:** add multi-classification folder structure and refactoring binary folder structure ([#45](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/45)) ([7285847](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/7285847458d5b292b1d15c463720a809b73d46b9))


## [0.8.1](https://github.com/radicalbit/radicalbit-ai-monitoring/compare/v0.8.0...v0.8.1) (2024-06-25)

### Bug Fixes

* removed all .count() and replaced with attribute in the class definition ([#16](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/16)) ([b86c5ec](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/b86c5ecd7ce1e828f3e32079ba96e7bf68abd510))
* **ui:** fix import path for DataQualityMetrics and ModelQualityMetrics in import-detail-modal ([#24](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/24)) ([0be20d5](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/0be20d579a4e29cea8c370018cf0b4fdc1cccd14))
* **ui:** show filename in import-detail-modal header ([#25](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/25)) ([99629c5](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/99629c5b28d55f82c431829a71133b0041599617))

### Chores

* force dataType to TABULAR ([#7](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/7)) ([c9c37ff](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/c9c37ff8a78f1dfbb72aee1b8831928cb66cc1dc))
* **sdk:** align reference metrics business models with API ([#11](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/11)) ([0db1dfe](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/0db1dfe365adb7a1973b6302359bc18c158bf720))
* **sdk:** apply ruff format and lint like done in API project ([#18](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/18)) ([41fd0cf](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/41fd0cf440ab09c51908dc060792063fcc093557))
* **sdk:** get current dataset statistics ([#13](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/13)) ([dec2d05](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/dec2d05c08a9249e5c6e2e39cad2b6212f05f115))
* **sdk:** get current model quality metrics ([#21](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/21)) ([74fef65](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/74fef65bc4a43a0a0f5a4b8d43693ad7dc02a8d0))
* **sdk:** get data quality for current dataset ([#19](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/19)) ([fce83aa](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/fce83aa76d9c5d3a99e1e6720dbd2bd4dc1a243a))
* **sdk:** implement get current dataset drift ([#15](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/15)) ([7513b39](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/7513b39aed144d6c14cf60aaeabdffae1fa8b3f0))
* **sdk:** manage all metrics based on model type ([#22](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/22)) ([8d2710e](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/8d2710ef8040ba65d46615eb971940bd2d05d94d))

## 0.8.0 (2024-06-20)

### Features

* first public release ([b00ff4f](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/b00ff4f0de8fc07b0f55ab54b4b288c1f386378d))
