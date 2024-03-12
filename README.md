# ecs260-project

This repository contains the code and data for the ECS 260 Toxicity Disengagement project. The project aims to develop a pipeline that can detect toxic comments and disengagement from GitHub repositories.

## Installation

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

## GitHub API Token

To use the GitHub API, you need to create a personal access token. You can create a token by following the instructions [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

Once you have created the token, you can store it in a file called `.env` in the specific directories of the repository. The file should contain the following line:

```bash
GITHUB_TOKEN='<your_token_here>'
```
