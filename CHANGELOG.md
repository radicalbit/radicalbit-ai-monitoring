# Changelog

## [0.9.0](https://github.com/radicalbit/radicalbit-ai-monitoring/compare/v0.8.2...v0.9.0) (2024-07-16)


### Features

* add current model quality regression ([#90](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/90)) ([65f4f65](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/65f4f65a33e989f3363f5d85a9146d52ee2cf27d))
* add current model quality to multiclass metrics ([#71](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/71)) ([9cd152f](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/9cd152f27aa79e826fd1889f1efccb48066e3075))
* add data quality for regression ([#78](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/78)) ([21d9139](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/21d9139528046536af31ead67e54e88e7f358d7f))
* add data quality multiclass current ([#56](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/56)) ([ccb6b79](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/ccb6b79d97a60ff236912add582a58b42c469959))
* add data quality regression for reference data ([#63](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/63)) ([92e327f](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/92e327f00658c9490cd6d74bead0c883e583bd4f))
* add latest current and reference job status to modelout ([#59](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/59)) ([f062c1d](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/f062c1d86ad8ffc6acb4ef171af96ed9257953ff))
* add multiclass dto for model quality of reference part ([#46](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/46)) ([20e2d6b](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/20e2d6b95dba69b2dcd2a99856439a0d778a36ab))
* add reference regression model quality ([#81](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/81)) ([2ee6365](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/2ee636520fa95ae6ccc6f6cd478ffd3e6b02c46f))
* add regression current statistics ([#72](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/72)) ([d873f05](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/d873f058c4bc374bd05c2dd3871908a74f9056d8))
* add residuals metrics to regression demo model, edit docker compose in order to block the start of api and ui before the up&running of k3s container first ([#108](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/108)) ([8f204d9](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/8f204d937f375c048961fd0bad61bcca71b961b0))
* add residuals to regression dto ([#106](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/106)) ([6a662aa](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/6a662aac7d476ddf3a29a1f668fdfd067fcdd6b1))
* add statistics in current dataset for multiclass ([#53](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/53)) ([3881f97](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/3881f97d8e8a46119fe38fb11a877a11f10b9224))
* add support calculations to data quality of classification ([#82](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/82)) ([ac26194](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/ac26194aa9276b8445137c03f0988405f6ab9c20))
* added drift for regression ([#95](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/95)) ([460f79e](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/460f79e18c9dfbe17256e23764aa307c1638bd97))
* added job for regression model quality ([#51](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/51)) ([9bf435a](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/9bf435a377b10b222031bb205a3d7c3694acb83d))
* added model quality metrics for current dataset for regression ([#87](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/87)) ([6a63d26](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/6a63d266f82e6b35ef9c79ba11ad2c10f34f34ea))
* added residual calculations, refactor tests ([#104](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/104)) ([e344365](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/e3443651ad37497d741f8060f5e41543129bb6f7))
* added residuals to regression current, fix current job for mq - regression reference ([#105](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/105)) ([2d4c024](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/2d4c02484cc03b9a336fafe747659efbcebe225d))
* added support to binary and multiclass for predictions ([#84](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/84)) ([bc61f93](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/bc61f934bf69b7108d2f5c5e2c198c406511dc32))
* edit docker compose to add init-data container ([#99](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/99)) ([fb6a08a](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/fb6a08a6277985a4775998d2e487cdefae6941c9))
* refactoring model quality dtos ([#92](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/92)) ([85d6a64](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/85d6a64d1f6a2edc8c1f751f0796617368d66a5d))
* reference multiclass model quality ([#49](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/49)) ([e0e68d2](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/e0e68d27d5a55f7d35756826aea36297e69fa08e))
* **spark:** added data quality for current regression ([#80](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/80)) ([7b5f6b5](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/7b5f6b5ec0dfcc537b77764dbb2b82dbc8e20daa))
* **spark:** added reference statistics for regression ([#55](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/55)) ([cdff426](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/cdff426cab8cfb9be1f827ff864be690e7ec508d))
* **spark:** model quality and drift for current - multiclass classification ([#74](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/74)) ([14d2cb9](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/14d2cb9a62f45299a0fd4cad6ca970acd5feaef2))
* **ui:** add model quality for multiclass and other improvement ([#85](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/85)) ([e75d1ea](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/e75d1ea3659594f563a838e3ba3c8a4956746322))
* **ui:** add reference multiclass model quality ([#69](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/69)) ([b505692](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/b505692afd73ed64acb8355af3685b1f0361de77))
* **ui:** add support model quality multiclass ([#93](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/93)) ([af3ec85](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/af3ec856ca9b9da1255d0f18610b9af0fe649a67))
* **ui:** implement chart for multi classification ([#68](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/68)) ([bfcd273](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/bfcd273e4b32a7e8aceadacab3180e2e9b9a5eff))
* **ui:** implement regression reference current ([#94](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/94)) ([0035b60](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/0035b60558aef9f0c89313bf5451247d11ab8210))
* **ui:** regression scaffolng ([#73](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/73)) ([26ef8f7](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/26ef8f754ec1bd743833e5f5857249177f873e39))
* update wizard ([#54](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/54)) ([379ee62](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/379ee62f41e9a35ca6882df0425ae95c8f37bf02))


### Bug Fixes

* check that prediction_proba is not None before checking its type ([#61](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/61)) ([6942317](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/6942317c58cdeeae17f43925bfc7345288410356))
* define single structure for drift metrics ([#67](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/67)) ([aed740b](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/aed740b0b8f62e1b22bd9d183306b62a1b409205))
* edit model quality regression dto and data quality regression dto ([#86](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/86)) ([c1dbcb2](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/c1dbcb243d6a969dfca665cdf0a0eff110878f57))
* filter NaN and None before model quality metrics ([#70](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/70)) ([02659e7](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/02659e73a6cf719f2f20f30b87d21138d019626b))
* return value for model quality regression to json ([#91](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/91)) ([ed4ffd6](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/ed4ffd6e28deb767aa4adaa7734bfd78f61ed285))
* set correlation id column as optional ([#88](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/88)) ([e9d2b99](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/e9d2b996b0131c93a725e0bb6b5bd98efa70fef5))
* set optional field of current multiclass model quality  ([#77](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/77)) ([17bed6b](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/17bed6b28ff50ca423373076f11a3ae65c3d1b20))
* **ui:** add missing template for regression modelType ([#102](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/102)) ([1ff9332](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/1ff9332406c7c29f43045ea1c17e8884160fb39b))
* **ui:** fix polling issue ([#110](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/110)) ([18fdd58](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/18fdd58345549adf493838b2ddce085086043437))
* **ui:** remove space ([#79](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/79)) ([c092d14](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/c092d14b107702b93a4f2b0fb74f6f6654590ac9))
* update pyproject and put package ([#107](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/107)) ([2a62b08](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/2a62b087ade74bf497cc17620734d38eaaced513))
* updated ks test with new phi value, fixed reference and current columns in class, fixed chi2 has_drift ([#58](https://github.com/radicalbit/radicalbit-ai-monitoring/issues/58)) ([5b484e4](https://github.com/radicalbit/radicalbit-ai-monitoring/commit/5b484e476d5c92ba785d82935b9ba02748173342))

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
