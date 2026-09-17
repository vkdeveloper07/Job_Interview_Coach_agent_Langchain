import os;
import logging;
import openai;
from dotenv import load_dotenv;
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import sys;
from langchain_core.prompts import PromptTemplate

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("email_humanizer")

load_dotenv()
if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY").startswith("sk-your"):
    logger.error("OPENAI_API_KEY not set. Copy .env.example to .env and add your key.")
    sys.exit(1)

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.7)

# ----------------------------------------------------------------------
# Tools
# ----------------------------------------------------------------------

Analyse_Target_Role_Prompt = PromptTemplate(
    input_variables=["job_description", "candidate_profile"],
    template="You are an expert in analyzing job roles. " \
    "Please analyze the following job description and candidate profile:" \
    "Job Description: {job_description}" \
    "Candidate Profile: {candidate_profile}" \
    "Identify critical skills, likely interview themes, strengths, and preparation gaps." \
    "Return ONLY a role-readiness assessment directly related to the candidate's experience, without any additional commentary."
)

Prepare_Interview_Questions_Prompt = PromptTemplate(
    input_variables=["role_readiness_assessment"],
    template=" Generate technical and behavioural questions with STAR-style " \
    "guidance and follow-up probes: {role_readiness_assessment} " \
    "Return ONLY a personalized interview practice pack directly related to the candidate's experience, without any additional commentary."
)

@tool
def analyse_target_role(job_description: str, candidate_profile: str) -> str:
    """
    Analyze the target role and candidate profile to identify critical skills, likely interview themes, strengths, and preparation gaps.
    """
    prompt = Analyse_Target_Role_Prompt.format(job_description=job_description, candidate_profile=candidate_profile)
    response = llm.invoke(prompt)
    return response.content

@tool
def prepare_interview_questions(role_readiness_assessment: str) -> str:
    """
    Prepare personalized interview questions based on the role readiness assessment.
    """
    prompt = Prepare_Interview_Questions_Prompt.format(role_readiness_assessment=role_readiness_assessment)
    response = llm.invoke(prompt)
    return response.content

# ----------------------------------------------------------------------
# Agent
# ----------------------------------------------------------------------
System_Prompt = """
Act as a rigorous interview coach. Always use Tool 1 before Tool 2 and use only the candidate experience provided.
"""
agent = create_agent(
    model=llm,
    tools=[analyse_target_role, prepare_interview_questions],
    system_prompt=System_Prompt)

def run_interview_coach_agent(job_description: str, candidate_profile: str) -> str:
    """
    Run the interview coach agent to analyze the target role and prepare interview questions.
    """
    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Job Description:\n{job_description}\n\n"
                    f"Candidate Profile:\n{candidate_profile}"
                ),
            }
        ]
    })
    return result["messages"][-1].content

def main() -> None:
    print("Interview Coach Agent")

    while True:
        print("Paste the job description, then type End on a new line:")
        job_description_lines = []
        while True:
            line = input()
            if line == "End":
                break
            job_description_lines.append(line)

        job_description = "\n".join(job_description_lines).strip()
        if job_description.lower() == "exit":
            break
        if not job_description.strip():
            print("Job description cannot be empty. Please try again.")
            continue

        print("Paste the candidate profile, then type End on a new   line:")
        candidate_profile_lines = []
        while True:
            line = input()
            if line == "End":
                break
            candidate_profile_lines.append(line)

        candidate_profile = "\n".join(candidate_profile_lines).strip()
        if not candidate_profile.strip():
            print("Candidate profile cannot be empty. Please try again.")
            continue

        try:
            result = run_interview_coach_agent(job_description, candidate_profile)
            print("Interview Coach Agent Result:")
            print("\n" + "=" * 60)
            print(result)
            print("\n" + "=" * 60)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()