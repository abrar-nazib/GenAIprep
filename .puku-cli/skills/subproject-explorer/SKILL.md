---
name: subproject-explorer
description: Use when the user asks which subdirectory covers a GenAI/LangChain/LangGraph topic before making edits, or when orienting to this repo's layout. Maps each sibling subproject to its one-line purpose.
---

This repo is a flat collection of ~20 sibling subprojects (not a monorepo with shared code). Each is an independent scratch experiment. Use this map to find the right one before suggesting edits or refactors.

## Index

**LangChain — building blocks**
- `langchain_models/` — wrappers around LLM providers. Subfolders: `openai/`, `openrouter/`, `huggingface/`, `document_similarity/`. Each has its own `.env` and quick-start script.
- `langchain_prompts/` — `prompt_generator.py`, `chain_ui.py`, `ui.py`, `chatbot/`. Prompt templating and small chat UIs.
- `langchain_output_parsers/` — `jsonoutputparser.py`, `pydanticoutputparser.py`, `stringoutputparser.py`. Parsing LLM output into typed structures.
- `langchain_structured_output/` — `typed_dict/` and `pydantic/` subfolders. Structured-output patterns (the newer alternative to output parsers).
- `langchain_document_loader/` — `text_loader.py`, `py_pdf_loader.py`. Loading docs for RAG.
- `langhcain_chains/` — **note the typo in the directory name** (missing 'n'). `simple_chains.py`, `sequential_chain.py`, `parallel_chain.py`, `conditional_chains.py`. Legacy LCEL-style chain composition.
- `langchain_runnables/` — `runnable_sequence.py`, `runnable_parallel.py`, `runnable_branch.py`, `runnable_lambda.py`, `runnable_passthrough.py`, plus `multi_chain_runnable.py`, `standardized_components.py`, `non_standard_components.py`. Modern Runnable primitives (the successor to chains).
- `langchain_tools/` — large sandbox: `basics.py`, `tool_binding.py`, `structured_tool.py`, `enforced_schema.py`, `currency_conversion.py`, `refund_assistant.py`, `stateful_tool.py`, `stateless_tool.py`, `state_update_tool.py`, `streaming.py`, `error_handling.py`, `shell_tool.py`, `context.py`, `context_toolcall.py`, `store.py`. Tool calling patterns.
- `langchain_agents/` — `simple_agent.py`. Minimal agent example.

**LangGraph — workflows**
- `langgraph_hello_world/` — `simple_example.py`, `calculator_agent.py`, `conditional_edge.py`. Minimal introductions to graphs.
- `langgraph-basic-chatbot/` — `main.py`. Smallest chat-bot graph (no memory).
- `langgraph_chatbot_persistance/` — `main.py`, `langgraph_backend.py`, `time_travel.py`, `ui.py`. Chatbot with checkpointing (SQLite via `chatbot.db`), includes time-travel debugging.
- `langgraph_sequential_workflow/` — `bmi_calculator.py`, `llm_workflow.py`. Linear node pipelines.
- `langgraph_parallel_workflow/` — `main.py`, `paragraph_validator.py`. Fan-out / fan-in.
- `langgraph_conditional_workflow/` — `non_llm.py`, `llm_impl.py`. Routing nodes by state.
- `langgraph_iterative_workflow/` — `main.py`. Loops until a condition is met.
- `langgraph_endtoend/` — `customer_support_email_agent.py`. Larger real-ish example tying several patterns together.

**Other**
- `langsmith/` — `simple_llm_call.py`, `sequential_chain.py`. Tracing/observability examples (LangSmith).
- `template/` — `main.py`. Blank starter template for new subprojects.

**Top-level**
- `main.py` — placeholder `print("Hello from genai!")`. Not used.
- `pyproject.toml`, `uv.lock`, `.python-version` — root `uv` project; the subprojects reuse this venv.

## Gotchas

- `langhcain_chains/` is misspelled (missing 'n'). Always reference it by this exact path.
- `.env` files exist inside many subprojects. Per `PUKU.local.md`, only read `.env.example` — never the real `.env`.
- The repo's `.venv/` is shared across all subprojects via `uv`. Use `uv run` from the repo root (or any subdir — `uv` walks up to find `pyproject.toml`).
- `.claude/skills/youtube-tutorial-to-notes/` already exists for the user's tutorial-to-notes workflow. Don't duplicate it.