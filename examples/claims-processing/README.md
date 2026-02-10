## Example: Claims Processing Agent

The [`examples/claims-processing/`](examples/claims-processing/) example shows a more advanced agent that processes insurance claims with human approval for high-value requests.

The agent uses two tools:
- **`check_eligibility`** - Durably checks claim eligibility against external systems
- **`human_approval`** - Pauses execution and waits for a human reviewer to approve via a simple curl command

### Run it

```bash
cd examples/claims-processing
uv run .
```

Then start Restate and register the agent (same as in main README). Open the Restate UI at `http://localhost:9070`:

1. Click **"Register Deployment"** and enter `http://host.docker.internal:9080`

<img src="doc/registration.png" alt="Registration" width="700px"/>

2. Click on the **"run"** handler of the `ClaimAgent` service, fill in a key (e.g. "customer123"), and send this request:

```json
{
  "message": "Reimburse my hotel for my business trip of 5 nights for 1800USD of 24/04/2025",
  "session_id": "123"
}
```

<img src="doc/playground.png" alt="Send request" width="1000px"/>

The agent processes the claim and pauses, waiting for human approval:

<img src="doc/suspension.png" alt="Waiting for approval" width="1000px"/>

### Test the durability

The curl command to approve is printed in the agent logs:
```bash
curl localhost:8080/restate/awakeables/sign_.../resolve --json 'true'
```

Copy the command but **don't run it yet**. First, try to break the agent:
1. Kill the agent process (Ctrl+C) and restart it
2. Wait for hours or days
3. Restart the Restate container (if you attached a persistent volume to the container)

**The agent state is safely stored in Restate.** Whenever you run the approval curl command, the agent wakes up and finishes processing:

<img src="doc/completed.png" alt="Completed after approval" width="1000px"/>

## How It Works

<img src="doc/overview.png" alt="overview" width="600px"/>

1. **Requests arrive via Restate** - Restate acts as the gateway, routing requests to your agent and managing execution state.
2. **Every step is journaled** - Tool calls, LLM interactions, and side effects are recorded in Restate's durable log.
3. **Failures trigger replay** - If your agent crashes, Restate replays the journal to restore state without re-executing completed steps.
4. **Awakeables enable async workflows** - Agents can pause and wait for external signals (human approval, webhooks, timers) without holding resources.