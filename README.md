## Setup and Run the Application

This application is a template for using GitHub Copilot App for agents og skillsets.

![agents](docs/extensions-agent.drawio.svg)

![skillsets](docs/extensions-skillset.drawio.svg)

### Installation and local development

1. Create venv, install poetry, and install dependencies using Poetry:

```sh
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install Poetry and dependencies
pip install poetry
poetry install

# run the application or start a debug session using F5
python -m main
```
## Create GitHub App - common instructions

Please follow the [GitHub docs for setting up a Copilot App](https://docs.github.com/en/copilot/building-copilot-extensions/creating-a-copilot-extension/creating-a-github-app-for-your-copilot-extension#creating-a-github-app).

You need to create one app for the agent and one for the skillset.

### Create settings
Copy your codespace URL from the ports tab. This URL will be used to set up the GitHub App.
- It should look like this: `https://codespace-port.app.github.dev`

Fill in:
- GitHub App name: copilot-agent/skillset-initals (must be unique)
- Homepage URL: https://codespace-port.app.github.dev (not important)
- Deactivate webhook
- Add Account permission `Copilot Chat`
- Create the app on your account
- After creation:
  - [General] Set callback URL to your codespace: `https://codespace-port.app.github.dev/`
  - `Save changes`
- Follow the instructions below to set up the app for either agent or skillset.
- After setup:
  - [Install App] Install the app on your account

## GitHub App - Agent setup

### Configure the app

- [Copilot] Set App Type to `Agent`
- [Copilot] Set URL to be the agent endpoint `https://codespace-port.app.github.dev/agents/blackbeard`
- [Copilot] Set Inference description to `Talk as Blackbeard the pirate`
- `Save`


## GitHub App - Skillset setup

### Configure the app
- [Copilot] Set App Type to `Skillset`
- [Copilot] Click on `Add new skill` and insert values from [Add new skillset](#add-new-skillset) below.
- `Save`


### Add new skillset values
``` sh
# Name
get-quote

# Inference description
Generates a random quote from a famous person

# URL
Insert the URL that codespace generates. It should include the endpoint.
https://codespace-port.app.github.dev/skillsets/random-quote

# Parameters
{
  "type": "object",
  "properties": {
    "parameter_name": {
      "type": "string",
      "description": "Name of the repository"
    }
  }
}
```

Remember to install the app on your account after setting up the app.
- [Install App] Install the app on your account