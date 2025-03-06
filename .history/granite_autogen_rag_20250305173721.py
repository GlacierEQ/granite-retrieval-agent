"""
requirements:  ag2==0.7.5, ag2[ollama]==0.7.05, crewai==0.102.0, crewai-tools==0.33.0, ollama
"""

from typing import List
from crewai import Agent, Task, LLM
from crewai.tools import tool
from fastapi import Request
from ollama import Client as OllamaClient
from open_webui import config as open_webui_config
from pydantic import BaseModel, Field


# Pruning Logic
def prune_model(model):
    # Implement the pruning logic here
    pass


class Pipe:
    class Valves(BaseModel):
        TASK_MODEL_ID: str = Field(default="ollama/granite3.2:8b-instruct-q8_0")
        VISION_MODEL_ID: str = Field(default="ollama/granite3.2-vision:2b")
        OPENAI_API_URL: str = Field(default=open_webui_config.OLLAMA_BASE_URL or "http://localhost:11434")
        OPENAI_API_KEY: str = Field(default="ollama")
        VISION_API_URL: str = Field(default=open_webui_config.OLLAMA_BASE_URL or "http://localhost:11434")
        MODEL_TEMPERATURE: float = Field(default=0)
        MAX_RESEARCH_CATEGORIES: int = Field(default=4)
        MAX_RESEARCH_ITERATIONS: int = Field(default=6)
        INCLUDE_KNOWLEDGE_SEARCH: bool = Field(default=False)
        RUN_PARALLEL_TASKS: bool = Field(default=False)

    def get_provider_models(self):
        return [
            {"id": self.valves.TASK_MODEL_ID, "name": self.valves.TASK_MODEL_ID},
        ]

    def __init__(self):
        self.type = "pipe"
        self.id = "granite_retrieval_agent"
        self.name = "Granite Retrieval Agent"
        self.valves = self.Valves()

    # Additional methods and logic for the Pipe class...

"""
# Additional code and logic for the rest of the file...
"""
