"""
==============================================================================
PRE-AI Ollama Local AI Provider (providers/ollama_provider.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: Local Open-Source AI Execution ($0 Cost)
Ollama runs open-source LLMs (Llama 3, Mistral, Gemma, Phi) locally on your computer.

- Local REST endpoint: `http://localhost:11434/api/generate`
- No cloud API keys required!
- Zero cost ($0 per token).
==============================================================================
"""

import time
import httpx
import logging
from typing import Dict, Any, Optional
from app.providers.base import BaseAIProvider
from app.core.config import settings

logger = logging.getLogger("ollama_provider")


class OllamaProvider(BaseAIProvider):
    """
    Local Ollama AI Provider Client.
    """

    def __init__(self, model_name: str = "llama3:latest"):
        self.model_name = model_name
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")

    def count_tokens(self, text: str) -> int:
        """
        Estimates token count for local models (~4 chars per token).
        """
        if not text:
            return 0
        return max(1, len(text) // 4)

    def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calls local Ollama REST API endpoint to generate response text.
        """
        start_time = time.time()
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt or "",
            "stream": False
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    latency_ms = int((time.time() - start_time) * 1000)
                    output_text = data.get("response", "")
                    
                    return {
                        "text": output_text,
                        "prompt_tokens": data.get("prompt_eval_count", self.count_tokens(prompt)),
                        "completion_tokens": data.get("eval_count", self.count_tokens(output_text)),
                        "latency_ms": latency_ms,
                        "model": self.model_name
                    }
        except Exception as e:
            logger.warning(f"Ollama local server connection failed at {url}: {e}")

        # Fallback response if local Ollama server is offline
        latency_ms = int((time.time() - start_time) * 1000) + 50
        mock_output = f"[Ollama Local Mode ({self.model_name})]: Local Ollama server is offline. Install & run Ollama locally at http://localhost:11434 for free local inference."
        
        return {
            "text": mock_output,
            "prompt_tokens": self.count_tokens(prompt + (system_prompt or "")),
            "completion_tokens": self.count_tokens(mock_output),
            "latency_ms": latency_ms,
            "model": self.model_name
        }
