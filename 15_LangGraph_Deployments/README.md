<p align = "center" draggable="false" ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719"
     width="200px"
     height="auto"/>
</p>

## <h1 align="center" id="heading">Session 15: Build & Serve Agentic Graphs with LangGraph</h1>

| 📰 Session Sheet                                             | ⏺️ Recording                           | 🖼️ Slides                                  | 👨‍💻 Repo    | 📝 Homework                                      | 📁 Feedback                                          |
| ------------------------------------------------------------ | -------------------------------------- | ------------------------------------------- | ------------- | ------------------------------------------------ | ---------------------------------------------------- |
| [Agent Servers](https://github.com/AI-Maker-Space/AIE9/tree/main/00_Docs/Session_Sheets/15_Agent_Servers) |[Recording!](https://us02web.zoom.us/rec/share/lORjByDju6fv4TdE3r93dorY3aNgmSKL_Qk_cX_AMcCQ6cNfSW77unaA1LMVV60.OcI8uEnfVmRAgjSn) <br> passcode: `Dc@&pv1T`| [Session 15 Slides](https://www.canva.com/design/DAG-EJqkRaM/FR3WG_yMA5_BqbWpQlHR9g/edit?utm_content=DAG-EJqkRaM&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) | You are here! | [Session 15 Assignment: Agent Servers](https://forms.gle/Vb3HNDsyVPQ1jqKX7) | [Feedback 3/3](https://forms.gle/kYmhbVUEMog16mKv8) |

### Prerequisites

Before starting, ensure you have the following:

- **Python 3.11+** installed
- An **OpenAI API Key**
- A **Tavily API Key**
- (Optional) **LangSmith** credentials for tracing

Create a `.env` file in this directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```
2. Run `uv sync` to install dependencies.

# Build 🏗️

Run the repository and complete the following:

- 🤝 Breakout Room Part #1 — Building and serving your LangGraph Agent Graph
  - Task 1: Getting Dependencies & Environment
    - Configure `.env` (OpenAI, Tavily, optional LangSmith)
  - Task 2: Serve the Graph Locally
    - `uv run langgraph dev` (API on http://localhost:2024)
  - Task 3: Call the API from a different terminal
    - `uv run test_served_graph.py` (sync SDK example)
  - Task 4: Explore assistants (from `langgraph.json`)
    - `agent` → `simple_agent` (tool-using agent)
    - `agent_helpful` → `agent_with_helpfulness` (separate helpfulness node)

- 🤝 Breakout Room Part #2 — Using LangSmith Studio to visualize the graph
  - Task 1: Open Studio while the server is running
    - https://smith.langchain.com/studio?baseUrl=http://localhost:2024
  - Task 2: Visualize & Stream
    - Start a run and observe node-by-node updates
  - Task 3: Compare Flows
    - Contrast `agent` vs `agent_helpful` (tool calls vs helpfulness decision)

<details>
<summary>🚧 Advanced Build 🚧 (OPTIONAL - <i>open this section for the requirements</i>)</summary>

>NOTE: This can be done in place of the Main Assignment

- Create and deploy a locally hosted MCP server with FastMCP.
- Extend your tools in `tools.py` to allow your LangGraph to consume the MCP Server.

When submitting, provide:
- Your Loom video link demonstrating the MCP server integration
- The GitHub URL to your completed Advanced Build

Have fun!
</details>

### Questions & Activities

#### Question 1:
What is the key architectural difference between the `simple_agent` and `agent_with_helpfulness` graphs? Specifically, explain how the helpfulness evaluation loop works and what mechanisms are in place to prevent it from running indefinitely.

##### Answer:
The key architectural difference between the `simple_agent` and `agent_with_helpfulness` graphs is the addition of an evaluation loop in the second architecture.
The `simple_agent` follows a straightforward execution flow: the agent receives a user query, optionally calls a tool if needed, generates a response, and then terminates.
The `agent_with_helpfulness` graph introduces a `helpfulness` evaluation node after the agent generates a response. This node evaluates whether the response sufficiently answers the user’s question. In the LangSmith execution trace, this appears as a `helpfulness` step that returns values such as `HELPFULNESS: Y`.
If the response is considered helpful, the graph proceeds to the end state. If the response is not considered helpful, the workflow loops back to the agent so it can attempt to generate a better response.
To prevent the evaluation loop from running indefinitely, a loop limit (maximum retry count) is implemented in the graph logic. Once this retry limit is reached, the workflow terminates even if the helpfulness condition has not been satisfied.

This architecture demonstrates how evaluation-based feedback loops can be integrated into agent workflows to improve response quality while maintaining safe execution boundaries.
By separating answer generation from quality evaluation, the system can iteratively improve responses while maintaining control through retry limits.


#### Question 2:
What is the role of `langgraph.json` in the LangGraph Deployments? Describe each of its key fields and how the platform uses this file to discover and serve your graphs.

##### Answer:
The `langgraph.json` file acts as the configuration file that defines how LangGraph should discover, load, and serve the graphs in a deployment. It provides the platform with the information needed to locate graph definitions, install dependencies, configure the runtime environment, and expose assistants through the LangGraph server.

Several key fields define how the LangGraph platform discovers and serves agent graphs.
The `version` field specifies the configuration schema version used by the LangGraph platform. This allows the platform to interpret the structure of the configuration correctly.
The `dependencies` field lists the Python packages or local project paths that must be installed in order for the graphs to run. In this case `"."` indicates that the current project should be installed as a dependency.
The `env` field specifies the environment file that should be loaded when the server starts. This file typically contains API keys and configuration variables required by the agents, such as OpenAI or Tavily credentials.
The `python_version` field defines the Python runtime version that should be used when running the deployment.
The `graphs` section maps graph identifiers to the Python import paths where the graphs are defined. For example, a graph ID may point to a module and object such as `app.graphs.simple_agent:graph`. The platform imports these objects at runtime to construct the agent workflows.
The `assistants` section defines the assistants that will be exposed through the LangGraph server. Each assistant references a graph through the `graph_id` field and includes metadata such as a name and description. When the server starts, these assistants become available for interaction in LangSmith Studio or through API calls.

Overall, `langgraph.json` acts as the central configuration that enables the LangGraph platform to automatically discover graph definitions, load the necessary environment and dependencies, and expose the configured assistants for execution and debugging.
When the LangGraph server is started using `uv run langgraph dev`, the platform reads the `langgraph.json` file to discover the available graphs and automatically exposes the configured assistants in LangSmith Studio.


#### Activity #1:
Create your own agent graph! Build a new graph in `app/graphs/` with a custom evaluation node (e.g., a vibe checker, a fact verifier, a summarizer — get creative!). Register it in `langgraph.json`, serve it with `uv run langgraph dev`

##### Answer:
### Custom Agent Graph: Clarity Agent

I implemented a custom agent graph called `clarity_agent` that introduces a clarity evaluation step after the agent generates a response.

The graph includes a `clarity` node that evaluates whether the generated answer is clear, well-structured, and easy to understand. If the response is considered clear (`CLARITY:Y`), the workflow terminates. If not, the workflow loops back to the agent to generate an improved answer.

A loop limit is implemented to prevent the evaluation cycle from running indefinitely.

This demonstrates how evaluation-based feedback loops can be integrated into LangGraph agent workflows to improve response quality.
The agent was registered in `langgraph.json` and tested through LangGraph Studio after running the server with `uv run langgraph dev`, where the `clarity` node appears in the execution graph and evaluates the generated response.


# Ship 🚢

- The completed notebook.
- 5min. Loom Video

# Share 🚀

- Walk through your notebook and explain what you've completed in the Loom video
- Make a social media post about your final application and tag @AIMakerspace
- Share 3 lessons learned
- Share 3 lessons not learned

# Submitting Your Homework

### Main Homework Assignment

Follow these steps to prepare and submit your homework:

1. Pull the latest updates from upstream into the main branch of your AIE9 repo:
    - _(You should have completed this process already.)_ For your initial repo setup, see [Initial_Setup](https://github.com/AI-Maker-Space/AIE9/tree/main/00_Docs/Prerequisites/Initial_Setup)
    - To get the latest updates from AI Makerspace into your own AIE9 repo, run the following commands:
    ```
    git checkout main
    git pull upstream main
    git push origin main
    ```
2. **IMPORTANT:** Start Cursor from the `15_LangGraph_Platform` folder (you can also use the _File -> Open Folder_ menu option of an existing Cursor window)
3. Answer Questions 1 - 2 using the `##### Answer:` markdown cell below them in the README
4. Complete Activity #1 in the README
5. Add, commit and push your modified files to your GitHub repository.

When submitting your homework, provide:
- Your Loom video link
- The GitHub URL to the `15_LangGraph_Platform` folder on your assignment branch
