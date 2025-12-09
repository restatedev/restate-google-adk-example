# Restate + Google ADK Example

**This integration is work-in-progress.**

This project demonstrates how to build resilient AI agents using [Restate](https://docs.restate.dev/ai) and [Google's Agent Development Kit](https://google.github.io/adk-docs/). The example shows a **claims processing agent** that can handle insurance or expense reimbursement requests with human approval workflows.

## What is Restate?

**Restate** is a platform that makes AI agents bulletproof. Think of it as a safety net for your AI workflows.

### The Problem
Traditional AI agents are fragile:
- ❌ Crash and lose all progress when something goes wrong
- ❌ Can't handle long-running tasks that need human input
- ❌ Difficult to debug when they fail
- ❌ No way to pause, resume, or rollback operations

### The Solution: Durable Execution
Restate provides **durable execution** - your AI agents can:
- ✅ **Never lose progress** - if your agent crashes, it picks up exactly where it left off
- ✅ **Wait for human approval** - pause execution for days/weeks until a human approves
- ✅ **Store context safely** - agent memory persists across restarts
- ✅ **Complete observability** - see exactly what your agent did and when
- ✅ **Handle failures gracefully** - automatic retries, timeouts, and error recovery
- ✅ **Run complex workflows** - orchestrate multiple agents, run tasks in parallel


## Prerequisites
- [Docker](https://www.docker.com/get-started/)
- [uv](https://uv.run/getting-started/installation)
- [Google API key](https://aistudio.google.com/app/api-keys)
- Python 3.11+

## Quick Start

Follow these steps to run the claims processing agent:

### 1. Set up your Google API key
Get a free API key from [Google AI Studio](https://aistudio.google.com/app/api-keys), then:
```bash
export GOOGLE_API_KEY=your-api-key
```

### 2. Start the AI agent
```bash
uv run .
```
Your agent is now running on `http://localhost:9080` and ready to process claims!

### 3. Start Restate (the durability engine)
Open a new terminal and run:
```bash
docker run --name restate_dev --rm \
-p 8080:8080 -p 9070:9070 -p 9071:9071 \
--add-host=host.docker.internal:host-gateway \
docker.restate.dev/restatedev/restate:latest
```
This starts Restate's runtime that will cooperate with your agent, to make it durable.

### 4. Register your agent in Restate
1. Open the Restate UI: `http://localhost:9070`
2. Click **"Register Deployment"**
3. Enter your agent URL: `http://host.docker.internal:9080`
4. Click **"Register"**

![Register service](https://raw.githubusercontent.com/restatedev/ai-examples/refs/heads/main/google-adk/example/docs/images/register_deployment.png)

### 5. Try your first claim!
1. Click on the **"run"** function of the `ClaimAgent` service
2. Fill in the `key` field with any customer ID (e.g., "customer123")
3. Click **"Send"** with the default request

This sends a simple reimbursement request to your agent!

<img src="doc/playground.png" alt="Send request" width="1000px"/>

In the invocations tab, you see the execution journal when clicking on the invocation ID:

<img src="doc/journal.png" alt="See journal" width="1000px"/>

## 🚀 See Durable Execution in Action!

Here's where Restate's magic becomes obvious. Let's trigger a workflow that requires human approval:

### Try a High-Value Claim
In the Restate UI, send this request instead of the default one:
```
"Reimburse my hotel for my business trip of 5 nights for 1800USD of 24/04/2025"
```

**What happens:**
1. ✅ Agent processes the request
2. 🛑 Agent detects high value ($1,800 > $1,000 threshold)
3. ⏸️ **Agent PAUSES and waits for human approval**

<img src="doc/suspension.png" alt="Waiting for approval" width="1000px"/>

### Test the Durability
Here's the cool part - **try to break it:**
1. ❌ Kill the agent process (Ctrl+C)
2. ❌ Cut off network access to the LLM
3. ❌ Wait for hours/days

**The agent state is safely stored in Restate!**

### Approve the request
1. Check your agent's terminal output - it printed a curl command like:
   ```bash
   curl localhost:8080/restate/awakeables/sign_.../resolve --json 'true'
   ```
2. Copy and run that curl command
3. 🎉 **The agent wakes up and completes the reimbursement!**

<img src="doc/completed.png" alt="Completed after approval" width="1000px"/>

### What Just Happened?
- ✅ **Durable state**: Agent's memory survived crashes and restarts
- ✅ **Human-in-the-loop**: Workflow paused for real human decision
- ✅ **Automatic resumption**: Agent continued exactly where it left off
- ✅ **Complete audit trail**: Every step is logged and visible

This is the power of durable execution - your AI agents become as reliable as traditional enterprise software!

## Build Your Own Agent
This example shows just the basics. With Restate, you can build:
- **Multi-agent systems** with resilient communication over HTTP
- **Long-running workflows** that span days or weeks
- **Complex approval chains** with multiple stakeholders
- **Fault-tolerant AI pipelines** that handle any failure
- **Distributed AI systems** that scale horizontally

## Next Steps

Now that you've seen durable execution in action, here's how to continue:

- **[Restate AI Documentation](https://docs.restate.dev/ai)** - Learn to build production-ready AI agents
- **[Google ADK Documentation](https://google.github.io/adk-docs/)** - Master Google's Agent Development Kit

