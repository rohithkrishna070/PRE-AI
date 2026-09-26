"""
==============================================================================
PRE-AI Mock AI Provider (providers/mock_provider.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION:
Offline AI simulation driver for fast unit testing, continuous integration, 
and local benchmarking without consuming cloud API quotas or requiring 
local GPU/Ollama setup.
==============================================================================
"""

import time
from typing import Dict, Any, Optional
from app.providers.base import BaseAIProvider


class MockProvider(BaseAIProvider):
    """
    Mock AI Provider used for fast unit testing and offline development.
    Simulates token counting, latency, and context-aware responses.
    """
    def __init__(self, model_name: str = "mock-model"):
        self.model_name = model_name

    def count_tokens(self, text: str) -> int:
        """
        Approximate rule-of-thumb: 1 token ~ 4 characters.
        """
        if not text:
            return 0
        return max(1, len(text.strip()) // 4)

    def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generates simulated model completions with realistic token metrics.
        """
        start = time.time()
        
        # Cleanly summarize or complete prompt based on input context
        if "summarize" in prompt.lower():
            output_text = f"[{self.model_name} Summary]: Core incident and key observations processed concisely."
        elif "optimize" in prompt.lower() or "compress" in prompt.lower() or "refine" in prompt.lower():
            # Return compressed bullet points
            lines = [l.strip() for l in prompt.split("\n") if l.strip() and not l.startswith("Target Model:")]
            output_text = "- Concise directive\n- Clear constraints\n- Preserved {{placeholders}}"
        else:
            output_text = f"[{self.model_name}]: Processed input successfully with simulated response."

        latency_ms = int((time.time() - start) * 1000) + 12
        prompt_tokens = self.count_tokens((system_prompt or "") + "\n" + prompt)
        completion_tokens = self.count_tokens(output_text)

        return {
            "text": output_text,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "latency_ms": latency_ms,
            "model": self.model_name,
            "status": "SUCCESS"
        }
