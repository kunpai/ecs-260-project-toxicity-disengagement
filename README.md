# Toxicity and Disengagement in GitHub Repositories

This repository contains the code and data for the ECS 260 Toxicity Disengagement project. The project aims to develop a pipeline that can detect toxic comments and disengagement from GitHub repositories, and draw conclusions about the relationship between the two.

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

## Moderation API Token

To use OpenAI's moderation API, you need to create an API key. You can create a key by following the instructions [here](https://platform.openai.com/docs/api-reference/authentication).

Once you have created the key, you can store it in a file called `API.txt` in the `moderation` directory of the repository.

## Classifier Onnx Model

The classifier model required for the toxicity detection pipeline is not included in the repository. You can download the model from [this link](https://drive.google.com/file/d/1J6T5Faa9_EhQDFWZ2ulVuRonHt9xOJjC/view?usp=drive_link) and place it in the `toxicity_detector` directory of the repository.

## Data

The raw data used in the project is not included in the repository. You can download the data from [this link](https://drive.google.com/file/d/1NgA3A4MYbm1gZ4Vi0SQ_EBoCTKAw5qpr/view?usp=drive_link) to view the raw data.
However, the processed correlation matrices are included in the `results` directory of the repository.
Every plot is saved in the `plots` directory of the repository.
