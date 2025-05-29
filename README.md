# agent_gemini

## Introduction

`agent_gemini` is an application leveraging the crewAI framework to orchestrate AI agents for automated task execution. Its core capability is to define and run multi-agent crews to accomplish complex goals specified via configuration.

## Architecture Overview

The system is built upon the crewAI library, employing a configuration-driven approach to define agents, their roles, and the tasks they perform. It supports sequential task processing by default.

## Core Components

*   `src/agent_gemini/`: Primary module containing the application logic.
    *   `main.py`: Serves as the application's main entry point, providing CLI commands for running, training, replaying, and testing agent crews.
    *   `crew.py`: Defines the `AgentGemini` crew, including agent definitions (e.g., `researcher`, `reporting_analyst`) and task specifications (e.g., `research_task`, `reporting_task`) which are loaded from YAML configurations.
    *   `config/agents.yaml` & `config/tasks.yaml`: Externalized YAML configuration files that define the properties, roles, goals of agents, and the description and expected outputs for tasks. These configurations support dynamic variable interpolation.
    *   `tools/`: Designated directory for custom tools that can be integrated with agents to extend their capabilities. (Refer to `crewAI` documentation for tool integration).
*   `knowledge/`: Intended for storing persistent information or knowledge bases that agents can utilize. (Refer to `crewAI` documentation for connecting knowledge sources).

## Dependency Management and Build System

*   `pyproject.toml`: Standard Python project definition file, specifying metadata, dependencies (primarily `crewai[tools]`), and project scripts. It utilizes `hatchling` as the build backend.
*   `uv` & `uv.lock`: The project employs `uv`, a high-performance Python package installer and resolver, for dependency management. The `uv.lock` file ensures deterministic and reproducible builds.

## Setup and Execution

### Prerequisites

*   Python 3.10-3.12
*   `uv` (Python package installer, assumed to be installed for `uv venv`)
*   `crewai` (Python package, assumed to be installed or bootstrapped for `crewai` commands)

### 1. Create Virtual Environment

It is recommended to create a dedicated virtual environment for this project. Using `uv`, you can create an environment named `myenv` (or your preferred name) as follows:

```bash
uv venv myenv
```

### 2. Activate Virtual Environment

Activate the newly created environment:

*   **On macOS/Linux:**
    ```bash
    source myenv/bin/activate
    ```
*   **On Windows:**
    ```bash
    myenv\Scripts\activate
    ```
    *(Note: If you chose a different environment name, replace `myenv` with your chosen name in the activation command.)*

### 3. Install Dependencies

Once the environment is activated, install the project dependencies using the `crewai` CLI:

```bash
crewai install
```
This command should handle the installation of all necessary packages defined in the `pyproject.toml` file.

### 4. Run the Application

To execute the main crew and start the agent tasks, use the `crewai` CLI:

```bash
crewai run
```
This command will initiate the configured crew process. Check the console for output and progress. The example `reporting_task` is configured to save its output to `report.md`.
