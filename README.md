# Job Interview Coach Agent

A terminal-based interview preparation assistant built with LangChain and OpenAI. The agent analyzes a job description and candidate profile, then creates a personalized interview practice pack.

## Features

- Analyzes role requirements and candidate strengths or preparation gaps.
- Generates technical and behavioural interview questions.
- Provides STAR-style guidance and follow-up probes.
- Supports multi-line job descriptions and candidate profiles pasted into the terminal.
- Uses the candidate profile as the source of truth for interview preparation.

## Requirements

- Python 3.10 or later
- An OpenAI API key

## Installation

Create and activate a virtual environment if needed:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```env
OPENAI_API_KEY=your_openai_api_key
```

Do not commit `.env` or expose your API key. It is excluded by `.gitignore`.

## Run

```powershell
python interview_coach_agent.py
```

Paste the complete job description, including any number of lines. Type `End` on its own line when finished:

```text
Paste the job description, then type End on a new line:
We are looking for a Python developer...
Responsibilities:
- Build APIs
- Write automated tests
End
```

Paste the candidate profile the same way:

```text
Paste the candidate profile, then type End on a new line:
Python developer with four years of FastAPI experience.
Skills: Python, FastAPI, SQL, Docker
End
```

The agent prints the role-readiness assessment and personalized interview practice pack. Enter `exit` as the job description to quit.

## How It Works

1. The terminal collects the multi-line job description.
2. The terminal collects the multi-line candidate profile.
3. The LangChain agent invokes `analyse_target_role`.
4. The agent invokes `prepare_interview_questions` using the role assessment.
5. The final assistant message is printed to the terminal.

The program uses `ChatOpenAI` with the `gpt-4.1-mini` model and a temperature of `0.7`.

## Project Structure

```text
.
├── interview_coach_agent.py  # Application and agent tools
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── .gitignore                 # Local secrets and Python artifacts
```

## Direct Function Usage

The agent can also be called from another Python file:

```python
from interview_coach_agent import run_interview_coach_agent

result = run_interview_coach_agent(
    job_description="Python backend developer with FastAPI experience",
    candidate_profile="Four years of Python development and two years of FastAPI"
)

print(result)
```

## Notes

- A valid `OPENAI_API_KEY` is required when the module starts.
- API calls may incur OpenAI usage charges.
- The current terminal input sentinel is case-sensitive: use exactly `End`.
