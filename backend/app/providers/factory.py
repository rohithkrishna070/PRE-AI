"""
==============================================================================
PRE-AI Mock Provider & Provider Factory (providers/mock_provider.py & factory.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Factory Design Pattern
The Provider Factory (`get_provider(model_name)`) receives a target model string 
(e.g., "gemini-1.5-flash", "llama3:latest", "mock") and returns the appropriate 
Provider object.

This isolates model creation logic in ONE place, making the application 
extensible to new AI models without modifying service logic!
==============================================================================
"""

import time
from typing import Dict, Any, Optional
from app.providers.base import BaseAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.ollama_provider import OllamaProvider


class MockProvider(BaseAIProvider):
    """
    Mock AI Provider used for fast unit testing and offline development.
    """
    def __init__(self, model_name: str = "mock-model"):
        self.model_name = model_name

    def count_tokens(self, text: str) -> int:
        if not text:
            return 0
        return max(1, len(text) // 4)

    def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        start = time.time()
        output_text = f"[Mock Output for '{self.model_name}']: Processed prompt successfully."
        latency_ms = int((time.time() - start) * 1000) + 15
        
        return {
            "text": output_text,
            "prompt_tokens": self.count_tokens(prompt + (system_prompt or "")),
            "completion_tokens": self.count_tokens(output_text),
            "latency_ms": latency_ms,
            "model": self.model_name
        }


def get_provider(model_name: str) -> BaseAIProvider:
    """
    Factory function returning the appropriate AI Provider based on model name.
    
    Examples:
    - "gemini-1.5-flash" -> GeminiProvider
    - "llama3:latest", "mistral" -> OllamaProvider
    - "mock" -> MockProvider
    """
    model_lower = model_name.lower()
    
    if "gemini" in model_lower:
        return GeminiProvider(model_name=model_name)
    elif any(k in model_lower for k in ["llama", "mistral", "ollama", "phi", "gemma", "qwen"]):
        return OllamaProvider(model_name=model_name)
    else:
        # Default fallback provider
        return GeminiProvider(model_name=model_name)
