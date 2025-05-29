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

### Virtual Environment

1.  **Create:**
    ```bash
    python -m venv .venv
    ```
2.  **Activate:**
    *   macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
    *   Windows:
        ```bash
        .venv\Scripts\activate
        ```

### Dependency Installation

Install the package and its dependencies using `uv`:
```bash
uv pip install .
```

### Running the Application

The primary method to execute the default crew behavior is:
```bash
python src/agent_gemini/main.py
```
Alternatively, use the configured script:
```bash
agent_gemini
```

Other available commands (defined in `pyproject.toml` scripts):

*   `run_crew`: Executes the default crew behavior.
    ```bash
    agent_gemini run_crew
    ```
*   `train`: For training the crew.
    ```bash
    agent_gemini train <n_iterations> <filename>
    ```
    Example: `agent_gemini train 5 training_log.json`
*   `replay`: For replaying a specific task.
    ```bash
    agent_gemini replay <task_id>
    ```
    Example: `agent_gemini replay research_task_uuid`
*   `test`: For testing the crew.
    ```bash
    agent_gemini test <n_iterations> <eval_llm>
    ```
    Example: `agent_gemini test 10 gpt-4`

## Output

The example `reporting_task` is configured to save its output to `report.md`.
