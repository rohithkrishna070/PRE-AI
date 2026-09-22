"""
==============================================================================
PRE-AI Prompt Auto-Refinement Engine (services/refinement_service.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: AI-Powered Token Reduction & Prompt Optimization
This engine uses a Meta-Prompt technique:
1. It sends the user's draft prompt to an AI model (Gemini or Ollama).
2. It instructs the AI model to compress instructions, eliminate fluff/redundancy, 
   format rules concisely using markdown, and preserve variable placeholders (`{{var}}`).
3. It counts tokens before vs after refinement and returns the exact % tokens saved!
==============================================================================
"""

import logging
from app.schemas.refine import RefinePromptRequest, RefinePromptResponse
from app.providers.factory import get_provider

logger = logging.getLogger("refinement_service")


def refine_prompt(request: RefinePromptRequest) -> RefinePromptResponse:
    """
    Executes AI-powered prompt optimization for token reduction and clarity.
    """
    provider = get_provider(request.target_model)

    # Calculate original token count
    original_combined = (request.system_prompt or "") + "\n" + request.user_prompt
    orig_token_count = provider.count_tokens(original_combined)

    # Formulate Meta-Prompt for the AI Optimizer
    meta_system_prompt = (
        "You are an expert AI Prompt Engineer and Token Optimization Engine.\n"
        "Your task: Refine and compress the given prompt for maximum instruction adherence "
        "with MINIMAL token count.\n"
        "Rules:\n"
        "1. Remove redundant words, conversational fluff, and unnecessary explanations.\n"
        "2. Format rules into concise, bulleted markdown points.\n"
        "3. Preserve all variable placeholders in {{variable_name}} format.\n"
        "4. Output ONLY the optimized prompt content."
    )

    meta_user_prompt = f"Target Model: {request.target_model}\nOriginal Prompt:\n{request.user_prompt}"

    # Call AI Provider to optimize the prompt
    ai_response = provider.generate(
        prompt=meta_user_prompt,
        system_prompt=meta_system_prompt
    )

    refined_user_prompt = ai_response.get("text", request.user_prompt).strip()
    
    # Calculate refined token count
    refined_token_count = provider.count_tokens(refined_user_prompt)
    
    # Calculate token savings metrics
    tokens_saved = max(0, orig_token_count - refined_token_count)
    reduction_pct = 0.0
    if orig_token_count > 0:
        reduction_pct = round((tokens_saved / orig_token_count) * 100.0, 2)

    # Extract template variables from refined prompt
    from app.services.prompt_service import extract_template_variables
    vars_list = extract_template_variables(refined_user_prompt)

    explanation = (
        f"Optimized prompt for '{request.target_model}'. Reduced word redundancy "
        f"and structured constraints into concise bullet points, saving {tokens_saved} tokens ({reduction_pct}% reduction)."
    )

    return RefinePromptResponse(
        original_system_prompt=request.system_prompt,
        original_user_prompt=request.user_prompt,
        refined_system_prompt=request.system_prompt,
        refined_user_prompt=refined_user_prompt,
        original_token_count=orig_token_count,
        refined_token_count=refined_token_count,
        tokens_saved=tokens_saved,
        token_reduction_pct=reduction_pct,
        explanation=explanation,
        extracted_variables=vars_list
    )
