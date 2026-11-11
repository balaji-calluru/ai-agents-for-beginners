"""One place to choose the model provider for all my labs and the capstone.

Every provider here speaks the OpenAI-compatible Chat Completions API, so Microsoft Agent
Framework's OpenAIChatCompletionClient works with all of them. (OpenAIChatClient targets the
newer Responses API, which these providers may not offer.)

Set ONE provider's variables in the repo-root .env (never commit it). To switch providers,
change .env only; no notebook edits needed.

    MiniMax: MINIMAX_API_KEY  [MINIMAX_BASE_URL] [MINIMAX_MODEL_ID]
    Novita:  NOVITA_API_KEY   [NOVITA_BASE_URL]  [NOVITA_MODEL_ID]
"""

import os

from agent_framework.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

# Defaults come from 00-course-setup/README.md. Model names change over time,
# so override the *_MODEL_ID variable in .env if your account has different ones.
_PROVIDERS = {
    "minimax": {
        "key": "MINIMAX_API_KEY",
        "base_url": ("MINIMAX_BASE_URL", "https://api.minimax.io/v1"),
        "model": ("MINIMAX_MODEL_ID", "MiniMax-M3"),
    },
    "novita": {
        "key": "NOVITA_API_KEY",
        "base_url": ("NOVITA_BASE_URL", "https://api.novita.ai/openai/v1"),
        "model": ("NOVITA_MODEL_ID", "deepseek/deepseek-v4-flash-0731"),
    },
}


def get_chat_client() -> OpenAIChatCompletionClient:
    """Build a chat client from whichever provider has an API key in .env."""
    load_dotenv()
    for name, cfg in _PROVIDERS.items():
        api_key = os.getenv(cfg["key"])
        if api_key:
            env_url, default_url = cfg["base_url"]
            env_model, default_model = cfg["model"]
            client = OpenAIChatCompletionClient(
                base_url=os.getenv(env_url, default_url),
                api_key=api_key,
                model=os.getenv(env_model, default_model),
            )
            print(f"Using provider: {name}")
            return client
    raise RuntimeError(
        "No provider configured. Add MINIMAX_API_KEY or NOVITA_API_KEY to your .env file."
    )


# --- Output helpers -------------------------------------------------------------------------
# MiniMax-style reasoning models emit <think>...</think> inline, and `response_format` (structured
# output) is not honored by these providers. These helpers make the output safe to show or parse.

import re

from pydantic import BaseModel

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


def strip_think(text: str) -> str:
    """Remove <think>...</think> reasoning blocks so they never reach a customer."""
    return _THINK_RE.sub("", str(text)).strip()


def parse_json_response[T: BaseModel](text: str, model: type[T]) -> T:
    """Parse a model's reply into a Pydantic model.

    Use instead of `response_format`: tell the agent to "reply with JSON only" matching the
    schema, then call this. It strips <think> blocks and takes the outermost {...} object.
    """
    cleaned = strip_think(text)
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"No JSON object found in model reply: {cleaned[:200]!r}")
    return model.model_validate_json(cleaned[start : end + 1])
