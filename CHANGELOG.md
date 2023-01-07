# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
### Fixed
### Removed

## [7.0.1] - 2023-01-07

### Added
- Add changelog

### Fixed
- Add python 3.11 support (@marteinn)
- Add django 4.1 support (@marteinn)
- Fix invalid assert (code-review-doctor)

## [7.0.0] - 2022-01-04

### Fixed
- Add Django 4.0 support
- Add Python 3.10 support

### Removed
- Drop Python 2 support
- Drop Python 3.6 support
- Drop support for EOL versions of Django (1 and 2)

## [6.0.2] - 2020-09-05

### Fixed
 - Make context_processor mandatory again

## [6.0.1] - 2020-08-30

### Fixed
- Solved XSS issue (@anthonynsimon, @marteinn)
- Add security policy

## [6.0.0] - 2020-04-28

### Added
- Add official support for Hypernova SSR service
- Add attribute “no_placeholder” when you want to skip the DRTT provided placeholder

### Fixed
- Add official Django 3 support (@niespodd, @marteinn)
- Remove context_processor required to run library (@niespodd)
- Solve issue with requests import (Aria Moradi)
- Use unit.patch instead of responses to mock requests (Umair)

### Removed
- Drop Django 1 support
- Drop pypy support


## [5.4.0] - 2019-04-28

### Added
- Make it possible to use your own SSRService

### Fixed
- Update docs
- Add project logo

## [5.3.0] - 2019-04-24

### Added
- Add SSRContext for passign values to SSR (@mikaelengstrom, @marteinn)
- Add support for disabling SSR using header HTTP_X_DISABLE_SSR

### Fixed
- Include example project
- Drop python 3.4 support

## [5.2.1] - 2018-08-10

### Fixed
- Add better SSR errors (thanks @mikaelengstrom)

## [5.2.0] - 2018-08-09

### Fixed
- Use render() if SSR is not available
- Fix bug when passing in standalone primitives in react_render
- Update docs

## [5.1.0] - 2018-05-22

### Added
- Add support for a replaceable tag manager (@aleehedl)
- Add configurable headers for SSR (@aleehedl, @marteinn)

## [5.1.0] - 2018-04-05

### Fixed
- Update react requirements in readme
- Change NotImplemented error to to_react_representation

### Removed
- Drop django support for django 1.10 and below
- Drop custom JSON serializer

## [4.0.0] - 2017-12-06

### Fixed
- Solved bug where to_react_representation triggered twice under SSR

### Removed
- Dropped support for django 1.8
- Removed templatetags for filters
