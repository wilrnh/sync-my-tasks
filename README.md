
<div align="center">
  sync-my-tasks
  <br />
  Copy tasks between apps
  <br />
  <br />
  <a href="https://github.com/wilrnh/sync-my-tasks/issues/new?assignees=&labels=type:bug&template=bug_report.md&title=">Report a Bug</a>
  ·
  <a href="https://github.com/wilrnh/sync-my-tasks/issues/new?assignees=&labels=type:enhancement&template=feature_request.md&title=">Request a Feature</a>
  .
  <a href="https://github.com/wilrnh/sync-my-tasks/discussions/categories/q-a">Ask a Question</a>
</div>

# Table of Contents
<details open="open">
<summary>Table of Contents</summary>

- [Getting Started](#getting-started)
- [Development](#development)
- [Deployment](#deployment)
- [Contribute](#contribute)
- [License](#license)

</details>

# Getting Started
[(Back to top)](#table-of-contents)

## Installation

Install the app from Pypi:

```sh
# Install using pip
pip install sync-my-tasks

# Run it
sync-my-tasks -h

sync-my-tasks.

Usage:
    sync-my-tasks (--from-asana --asana-workspace=<name> [--asana-token-file PATH])  (--to-mstodo)
    sync-my-tasks (-h | --help)
    sync-my-tasks --version

Options:
  -h --help                   Show this screen.
  --version                   Show version.
  --from-asana                Pull tasks from Asana.
  --asana-workspace=<name>    Name of workspace
  --asana-token-file PATH     Path to file containing the Asana Personal token. [default: ./asana-token]
  --to-mstodo                 Push tasks to Microsoft To-Do.
```

### Manual Installation:

1. Clone the repo: `git clone https://github.com/wilrnh/sync-my-tasks.git`
1. Install dependencies: `poetry install`
1. Start the app: `python sync-my-tasks/command.py`

## Usage

### Asana

### Microsoft To-Do

# Development
[(Back to top)](#table-of-contents)

## Architecture

sync-my-tasks is a CLI tool that copies tasks between apps. Since different apps provide varying APIs for the import and export of tasks, sync-my-tasks abstracts their functionality into _providers_ which are in charge of interfacing with their respective APIs and handling import and export.

Each provider is responsible for either importing or exporting a well defined `list` of `TaskList`s, or both.

`TaskList`: a named `list` of `Task`s
`Task`: an object representing a task, that is generic enough to be imported/exported between any provider.

# Deployment
[(Back to top)](#table-of-contents)

Github Actions will automcatically build and deploy releases to [Pypi](https://pypi.org/project/sync-my-tasks/).

# Contribute
[(Back to top)](#table-of-contents)

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply [open an issue](https://github.com/wilrnh/sync-my-tasks/issues/new?assignees=&labels=type:enhancement&template=feature_request.md&title=). Please feel free to [ask questions](https://github.com/wilrnh/sync-my-tasks/discussions/categories/q-a)!
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

# License
[(Back to top)](#table-of-contents)

Distributed under the MIT License. See `LICENSE` for more information.