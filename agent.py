import restate

from pydantic import BaseModel
from google.adk import Runner
from google.adk.agents.llm_agent import Agent
from google.adk.apps import App
from google.genai.types import Content, Part

from restate.ext.adk import RestatePlugin, RestateSessionService, restate_object_context

APP_NAME = "agents"


# MODELS
class ChatMessage(BaseModel):
    """In this example, use the same session ID for multi-turn conversation, otherwise provide a new session ID for each message."""

    session_id: str = "123"
    message: str = (
        "Reimburse my hotel for my business trip of 5 nights for 800USD of 24/04/2025"
    )


# TOOLS
async def check_eligibility(
    date: str, amount: float, category: str, reason: str
) -> bool:
    """Check claim eligibility"""

    async def is_eligible() -> bool:
        # ... call external systems or databases to verify eligibility ...
        return True

    # Durable step with retries and recovery
    return await restate_object_context().run_typed("Check eligibility", is_eligible)


async def human_approval(
    date: str, amount: float, category: str, reason: str
) -> str:
    """Ask for human approval for high-value claims."""
    # Create an awakeable for human approval
    approval_id, approval_promise = restate_object_context().awakeable(type_hint=str)

    # Request human review
    def request_review():
        # Notify human reviewer (e.g., via email or dashboard)
        print(
            f"""🔔 Review requested for claim for {reason}. Submit via: \n ")
              curl localhost:8080/restate/awakeables/{approval_id}/resolve --json 'true'"""
        )
    await restate_object_context().run_typed("Request review", request_review)

    # Wait for human approval
    return await approval_promise


# AGENT
agent = Agent(
    model="gemini-2.5-flash",
    name="claim_approval_agent",
    description="Insurance claim evaluation agent that handles human approval workflows.",
    instruction="""You are an insurance claim evaluation agent. Use these rules: 
    - if the amount is more than 1000, ask for human approval using tools; 
    - if the amount is less than 1000, use the check_eligibility tool and then decide by yourself.""",
    tools=[human_approval, check_eligibility],
)

app = App(name=APP_NAME, root_agent=agent, plugins=[RestatePlugin()])
runner = Runner(app=app, session_service=RestateSessionService())

agent_service = restate.VirtualObject("ClaimAgent")


# HANDLER
@agent_service.handler()
async def run(ctx: restate.ObjectContext, message: ChatMessage) -> str | None:
    events = runner.run_async(
        user_id=ctx.key(),
        session_id=message.session_id,
        new_message=Content(role="user", parts=[Part.from_text(text=message.message)]),
    )

    final_response = None
    async for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            if event.content.parts[0].text:
                final_response = event.content.parts[0].text
    return final_response
