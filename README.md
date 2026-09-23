# Relative Tech Support

*Because every family has one.*

A simple AI-powered app to help Grandma fix her tech problems, one step at a time.

## Features

- Friendly, conversational AI tech support
- Step-by-step troubleshooting without overwhelming the user
- Simple explanations for users with limited technical experience
- Multi-turn conversations that keep track of the current troubleshooting session
- Safety-focused guidance for potentially destructive or sensitive actions
- Simple web interface built with Gradio

## Built With

- Python
- OpenAI API
- Gradio
- python-dotenv
- Jupyter Notebook

## Setup

### 1. Create a virtual environment

```powershell
python -m venv .venv
```
### 2. Activate the virtual environment

```powershell
.venv\Scripts\Activate.ps1
```
### 3. Install dependencies

```powershell
pip install -r requirements.txt
```
### 4. Configure your API key

Copy `.env.example` to a new file named `.env`, then add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

Never commit your `.env` file or API key to Git.
### 5. Run the app

Open `relative_tech_support.ipynb` in Jupyter or a compatible editor and run all cells from top to bottom.

Once the final cell runs, Gradio will start the app and provide a local URL in the notebook output.