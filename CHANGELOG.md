# Changelog
All notable changes to this product will be documented in this file.

## [1.10.0] - 2025-01-09

### Added
* Unittests for pattern recognizers and person recognizer
* ner-model-configuration to presidio nlp-engine-configuration to fix MISC warning

### Changed
* Versions of spacy language models from 3.5 to 3.8

## [1.9.0] - 2024-11-11

### Added
* Single-focus logging functionality for debugging a specific recognizer.
* Generally more logging for recognizers.

### Changed
* Detected US addresses do not raise an InvalidParamException anymore in certain texts that contain many line breaks.
* Third party dependency pyap was removed

## [1.8.0] - 2024-09-16

### Added
* Optional language detection
* Logging

## [1.7.0] - 2024-07-11

### Added
* Support for Python 3.11
* Black and isort code formatting

### Changed
* Only load language models for specificed supported_languages in TextAnonymizer for faster initialization.
* Replaced setuptools with poetry-core as build tool.
* Language models are downloaded and installed as part of package installation instead of seperate step afterwards.
* Li-Numbers are not falsely detected as phone numbers anymore

### Removed
* Support for Python 3.7-3.9

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
