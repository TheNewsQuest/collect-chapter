<p align="center"><img src="https://i.ibb.co/wyMr7F2/image.png" width="500" height="280"/></p>

# Collect Chapter - Be prepared when the storm comes!

In this chapter, a pipeline is built in order to gather all the essential items (data) for various reasons.

## Source

The data will be collected from various newsletter sources, including different genres.

## Frequency

Different kinds of data will be scheduled to crawl at different intervals and different times of a day due to data's variety.

# Getting Started

## Installation

In order to run the project successfully, all the dependencies must be resolved using the following command:

```bash
pip install -r requirements.txt
```

## Project Setup

You can run project in different ways either using the Dagster CLI or the Dagster UI (Dagit). In this project, the Dagit way is preferred as interactions with jobs are so intuitive and straightforward on the UI.

1. Run command `dagit -p 3141`
2. Now you can access Dagit via `localhost:3141`

## Contribution Guide

All the commit messages must be following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) guide for semantic purposes! Otherwise your commits will be rejected automatically by commit hook!

#### <a name="commit-header"></a>Commit Message Header

```
<type>(<scope>): <short summary>
  │       │             │
  │       │             └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │       │
  │       └─⫸ Commit Scope: Feature scopes
  │
  └─⫸ Commit Type: build|ci|docs|feat|fix|perf|refactor|test|chore
```

The `<type>` and `<summary>` fields are mandatory, the `(<scope>)` field is optional.

##### Type

Must be one of the following:

- **build**: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
- **ci**: Changes to our CI configuration files and scripts (example scopes: Circle, BrowserStack, SauceLabs)
- **docs**: Documentation only changes
- **feat**: A new feature
- **fix**: A bug fix
- **perf**: A code change that improves performance
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **test**: Adding missing tests or correcting existing tests
- **chore**: Adding commit that is not related to code (resolve conflicts, etc...)

##### Scope (Optional)

The scope should be the name of the feature's scope that you're developing, it is OPTIONAL so feel free to skip it if you want to be more generic!
