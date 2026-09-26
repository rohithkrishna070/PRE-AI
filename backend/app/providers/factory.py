"""
==============================================================================
PRE-AI AI Provider Factory (providers/factory.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Factory Design Pattern
The Provider Factory (`get_provider(model_name)`) receives a target model string 
(e.g., "gemini-1.5-flash", "llama3:latest", "mock") and returns the appropriate 
Provider object.

This isolates model creation logic in ONE place, making the application 
extensible to new AI models without modifying service logic!
==============================================================================
"""

from typing import Dict, Any, Optional
from app.providers.base import BaseAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.ollama_provider import OllamaProvider
from app.providers.mock_provider import MockProvider


def get_provider(model_name: str) -> BaseAIProvider:
    """
    Factory function returning the appropriate AI Provider based on model name.
    
    Examples:
    - "gemini-1.5-flash" -> GeminiProvider
    - "llama3:latest", "mistral" -> OllamaProvider
    - "mock", "mock-model" -> MockProvider
    """
    model_lower = (model_name or "").lower()
    
    if "mock" in model_lower or "test" in model_lower:
        return MockProvider(model_name=model_name)
    elif "gemini" in model_lower:
        return GeminiProvider(model_name=model_name)
    elif any(k in model_lower for k in ["llama", "mistral", "ollama", "phi", "gemma", "qwen"]):
        return OllamaProvider(model_name=model_name)
    else:
        # Default fallback provider
        return GeminiProvider(model_name=model_name)
