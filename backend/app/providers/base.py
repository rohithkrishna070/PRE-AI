"""
==============================================================================
PRE-AI Abstract Base AI Provider (providers/base.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Interface Abstraction Pattern
In Python, an Abstract Base Class (ABC) defines a blueprint or standard interface 
that all AI Providers (Gemini, Ollama, OpenAI, Mock) MUST implement.

Benefits:
- Decouples business logic from specific vendor SDKs.
- Allows switching between Google Gemini and local Ollama without changing service code!

Methods required:
1. `generate(prompt, system_prompt, variables)` -> returns generated string response.
2. `count_tokens(text)` -> calculates exact token count.
==============================================================================
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseAIProvider(ABC):
    """
    Abstract Interface for all AI Model Providers.
    """

    @abstractmethod
    def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes a prompt generation request.
        Returns dictionary:
        {
            "text": "Generated response string",
            "prompt_tokens": 120,
            "completion_tokens": 45,
            "latency_ms": 320
        }
        """
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        Calculates exact or estimated token count for a text string.
        """
        pass
