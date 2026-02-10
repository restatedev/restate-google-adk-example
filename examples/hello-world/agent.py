import restate

from google.adk import Runner
from google.adk.agents.llm_agent import Agent
from google.adk.apps import App
from google.genai.types import Content, Part

from restate.ext.adk import RestatePlugin, RestateSessionService, restate_object_context


# TOOL
async def get_weather(city: str) -> str:
    """Get the current weather for a city."""

    async def fetch_weather() -> str:
        # Call weather API, database, or any external service
        return f"The weather in {city} is sunny, 72°F"

    # Durable execution: automatically retries and recovers on failure
    return await restate_object_context().run_typed("Get weather", fetch_weather)


# AGENT
agent = Agent(
    model="gemini-2.5-flash",
    name="weather_agent",
    description="A helpful weather assistant.",
    instruction="You are a helpful weather assistant. Use the get_weather tool to look up weather information.",
    tools=[get_weather],
)

app = App(name="weather", root_agent=agent, plugins=[RestatePlugin()])
runner = Runner(app=app, session_service=RestateSessionService())

weather_service = restate.VirtualObject("WeatherAgent")


# HANDLER
@weather_service.handler()
async def run(ctx: restate.ObjectContext, message: str) -> str | None:
    events = runner.run_async(
        user_id=ctx.key(),
        session_id="session",
        new_message=Content(role="user", parts=[Part.from_text(text=message)]),
    )

    final_response = None
    async for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            if event.content.parts[0].text:
                final_response = event.content.parts[0].text
    return final_response
