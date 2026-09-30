# Relative Tech Support

*Because every family has one.*

Relative Tech Support (RTS) is an AI-powered troubleshooting assistant designed to make everyday technology problems a little less frustrating. It provides friendly, patient, step-by-step support through a simple conversational interface, with the ability to use both text and images during troubleshooting.

**Live Demo:** [Try Relative Tech Support on Hugging Face](https://huggingface.co/spaces/RudyBCreative/relative-tech-support)

## About the Project

Relative Tech Support started with a simple idea: what would an AI tech-support assistant look like if it were designed for the family member who just wants their Wi-Fi, printer, phone, or computer to work without being buried in technical jargon?

RTS is also a hands-on learning project. I began building it as a true beginner in Python and software development, using concepts I was learning as a foundation and then branching out through experimentation, research, and AI-assisted development. The goal has not been to build everything from memory, but to understand the decisions being made, test assumptions instead of simply trusting them, and add complexity only when it solves a real problem.

Version 0.3 marks the project's first public deployment. It is still intentionally small, but it now represents an end-to-end application that can be run locally, inspected as a reproducible project, or used through its public Hugging Face Space.

## Features

- Friendly, conversational AI tech support designed for non-technical users
- Step-by-step troubleshooting that focuses on one manageable action at a time
- Multi-turn conversations that preserve troubleshooting context
- Image uploads for visual troubleshooting
- Follow-up questions that can reference previously shared images
- Streaming responses for a more responsive conversational experience
- Safety-focused guidance around credentials, destructive actions, and uncertain information
- Lightweight safeguards for public use, including upload limits, request rate limiting, bounded output, and queue limits

## Tech Stack

- **Python** - application logic
- **OpenAI Responses API** - AI responses and image understanding
- **GPT-5 nano** - current model
- **Gradio** - conversational web interface
- **python-dotenv** - local environment variable management
- **Hugging Face Spaces** - public deployment
- **Jupyter Notebook** - retained as an earlier prototyping and learning artifact

## How It Works

RTS uses a Gradio chat interface to collect a user's message, optional image, and conversation history. The Python application converts that information into the format expected by the OpenAI Responses API and streams the model's response back to the interface.

The system prompt gives RTS its troubleshooting behavior: patient explanations, one manageable step at a time, limited jargon, and clear boundaries around sensitive credentials or potentially destructive actions.

When images are included, RTS can use them as part of the troubleshooting context. Images from the current conversation can also be reconstructed into later requests so follow-up questions can refer to something the user shared earlier.

## Public Deployment Safeguards

Making RTS publicly accessible introduced a different set of concerns than running it locally. Version 0.3 adds several lightweight safeguards intended to keep the current public demo reasonably bounded without introducing infrastructure that the project does not yet need.

Current safeguards include:

- A 10 MB limit on uploaded images
- Basic image file-type validation before processing
- A rolling limit of 30 requests per 10 minutes per client IP
- A maximum queue size of 10 requests
- A 2,500-token maximum output per model response
- API credentials stored as private environment secrets rather than in source code
- Provider-side spending protection by keeping automatic API credit refills disabled
- User-friendly handling for API errors and incomplete model responses

These controls are intentionally lightweight. The rate limiter is stored in application memory and resets when the process restarts, and IP-based limiting is not a substitute for authentication or a persistent distributed rate-limiting system. Those tradeoffs are acceptable for the current scope of the project and can be revisited if RTS grows beyond a small public demonstration.

## Running Locally

### 1. Clone the repository

```powershell
git clone https://github.com/RudyBCreative/relative-tech-support.git
cd relative-tech-support
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure your API key

Copy `.env.example` to a new file named `.env`, then add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

Never commit your `.env` file or API key to Git.

### 6. Run the application

```powershell
python app.py
```

Gradio will start the application and provide a local URL in the terminal.

If PowerShell execution policy prevents activation of the virtual environment, the application can also be run directly with the virtual environment's Python executable:

```powershell
.\.venv\Scripts\python.exe app.py
```

## Project Evolution

RTS has been developed iteratively, with each version adding capabilities after the previous version was working and understood well enough to build on.

### v0.1.0 - Working Chatbot

The first version established the core idea: a conversational tech-support assistant with a patient, approachable personality and a focus on helping users work through problems one step at a time.

This version proved the basic application flow and established the behavior that continues to define RTS.

### v0.2.0 - Multimodal Support

Version 0.2 expanded RTS beyond text-only troubleshooting by adding image uploads and conversation history. Users could show RTS what they were seeing, continue the conversation, and ask follow-up questions that referenced previously shared information and images.

This version also marked the point where RTS began growing beyond a basic chatbot experiment into a more capable troubleshooting application.

### v0.3.0 - First Public Deployment

Version 0.3 moved RTS from a local prototype to a standalone application that could be deployed and used publicly. The notebook-based prototype was converted into a standalone Python application, and the project was prepared for deployment on Hugging Face Spaces.

Making the application public also introduced new concerns around resource usage, uploaded files, API costs, failure handling, and basic abuse prevention. Lightweight safeguards were added and deliberately tested, including image size and file-type validation, request rate limiting, queue limits, bounded model output, and handling for incomplete responses.

The public deployment was then tested with text conversations, image-based troubleshooting, conversation history, and anonymous access. Version 0.3 represents the first point at which RTS became a publicly accessible end-to-end application rather than only a local learning project.

## Learning & Development

RTS began while I was learning Python and LLM application development with no formal software development background. The project became a practical way to move beyond isolated examples and apply new concepts to an application I actually wanted to build. As the project evolved, that meant learning not only about model APIs and Python, but also Git, environment management, multimodal inputs, application structure, deployment, testing, security boundaries, and the tradeoffs involved in making an AI application publicly accessible.

AI has been an active part of that development process, serving as a learning partner, code reviewer, troubleshooting tool, research assistant, and implementation aid. I do not approach the project as an exercise in writing every line of syntax from memory. Instead, the goal is to increasingly understand what the code is doing, question recommendations, test behavior, make informed decisions about what belongs in the application, and build the ability to recognize when something does not make sense.

## Current Limitations & Future Exploration

RTS is currently a small public demonstration rather than a production-scale support platform. Its rate limiting is stored in application memory, resets when the application restarts, and relies on client IP addresses rather than user authentication. Conversation context exists only within the active Gradio session, and the application does not maintain persistent user accounts, troubleshooting histories, or long-term memory.

Future versions may explore improvements such as additional model options, more structured troubleshooting tools, expanded support for common problem categories, and more capable application-level controls. As the project evolves, new features will be added selectively when they provide enough practical or learning value to justify the additional complexity.

The current priority is not to make RTS as feature-rich as possible, but to continue improving it while keeping the application understandable, maintainable, and appropriate for its actual use.