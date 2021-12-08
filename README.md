# aviauth-api
![Version](https://shields.io/badge/version-0.1.0-blue)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/julleks/aviauth-api/blob/develop/LICENSE)

Authentication microservice based on FastAPI


# Overview

This project provides authentication and authorization service for external applications.
It allows using other applications without storing any user data in them.

Keeping all the data in a single place and clear management of access permissions for each
authorized application is a goal of this project.

We can end up with 3 products:
- Independent application for integration with external apps
- Open source authentication microservice ready-to-use
- Pip package for FASTApi


### Problem Statement

Most of the web application require registration or authentication using external services 
(as google or facebook), that have almost unlimited access to users data. Easy management of 
applications and permissions they have is something that missing.
Personal data is not personal anymore.


### Proposed Solution

Implement a service that keeps all the user's data encrypted and providing it
to external applications based on configured permissions.


# Success Criteria

- Running application in production environment
- Allowing to perform any user story described below
- Compliance with all requirements of the project


# User Stories

- Register accounts
- CRUD operations on user data
- Several emails / phone numbers / avatars per user
- Register / Manage applications
- Generate authentication tokens (multiple tokens per app)
- Manage permissions per app
- List / Delete active tokens
- See access history
- [2FA](https://en.wikipedia.org/wiki/Multi-factor_authentication)


# Scope

- Only creation of the API is the scope of the project. No frontend or other UI is required.
- A service for checking username availability in some popular applications
can be implemented in future iterations.


### Requirements

- [FastAPI](https://fastapi.tiangolo.com) web framework
- [SQLAlchemy](https://www.sqlalchemy.org) ORM
- Test coverage with [pytest](https://docs.pytest.org/en/6.2.x/contents.html)
- [OpenAPI](https://swagger.io/specification/) specification
- [GitHub actions](https://github.com/features/actions) as CI/CD tool
- [AWS](http://aws.amazon.com) infrastructure
- Managing infrastructure with [Terraform](https://www.terraform.io)
- [Trunk-based development](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development)
- [Open Source](https://opensource.org)
- [REST](https://restfulapi.net) API


### Non-Requirements

- 

### Conventions 

- [Semantic Versioning](documentation/conventions/semantic-versioning.md)
- [Changelog Convention](documentation/conventions/changelog.md)
- [Conventional Commits](documentation/conventions/conventional-commits.md)
- [Atomic commits](documentation/conventions/atomic-commits.md)



### Under discussion

- Blockchain usage
- Data encryption
- Docstring convention
- Code format convention
- Naming convention
- Documentation
- Database
- Project structure
- Clean architecture
- Automatic changelog generation
- Automatic versioning / tagging
