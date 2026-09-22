"""
==============================================================================
PRE-AI Prompt & Version Management Service (services/prompt_service.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: "GitHub for Prompts" Service
Handles prompt creation, version committing, dynamic variable extraction, 
and version history queries.

Template Variable Extraction:
- Searches user prompt string for `{{variable_name}}` patterns using Regex.
- Automatically builds the list of required variables!
==============================================================================
"""

import re
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.prompt import Prompt, PromptVersion
from app.schemas.prompt import PromptCreate, PromptVersionCreate
from app.providers.factory import get_provider


def extract_template_variables(text: str) -> List[str]:
    """
    Parses a prompt template for {{variable_name}} patterns.
    Example: "Hello {{name}}, your balance is {{amount}}" -> ["name", "amount"]
    """
    if not text:
        return []
    # Regular expression matching {{variable_name}}
    pattern = r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}"
    matches = re.findall(pattern, text)
    # Return deduplicated list preserving order
    return list(dict.fromkeys(matches))


def create_prompt_with_initial_version(db: Session, prompt_in: PromptCreate) -> Prompt:
    """
    Creates a new Prompt repository along with its initial Version 1 snapshot.
    """
    # 1. Create parent Prompt
    db_prompt = Prompt(
        title=prompt_in.title,
        description=prompt_in.description,
        project_id=prompt_in.project_id
    )
    db.add(db_prompt)
    db.flush() # Flushes to DB to get db_prompt.id without committing transaction yet

    # 2. Extract variables from user prompt template
    extracted_vars = extract_template_variables(prompt_in.initial_version.user_prompt_template)
    
    # 3. Calculate initial token count
    provider = get_provider(prompt_in.initial_version.target_model)
    full_text = (prompt_in.initial_version.system_prompt or "") + prompt_in.initial_version.user_prompt_template
    initial_tokens = provider.count_tokens(full_text)

    # 4. Create Version 1 snapshot
    db_version = PromptVersion(
        prompt_id=db_prompt.id,
        version_number=1,
        system_prompt=prompt_in.initial_version.system_prompt,
        user_prompt_template=prompt_in.initial_version.user_prompt_template,
        variables=extracted_vars,
        target_model=prompt_in.initial_version.target_model,
        token_count=initial_tokens,
        token_reduction_pct=0.0,
        commit_note=prompt_in.initial_version.commit_note or "Initial Version 1 commit"
    )
    db.add(db_version)
    db.flush()

    # Set active_version_id to initial version
    db_prompt.active_version_id = db_version.id
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


def create_new_prompt_version(
    db: Session, prompt_id: int, version_in: PromptVersionCreate
) -> PromptVersion:
    """
    Commits a new version snapshot to an existing prompt repository.
    Calculates token reduction percentage relative to Version 1.
    """
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not db_prompt:
        raise ValueError(f"Prompt with ID {prompt_id} not found")

    # Determine next sequential version number
    latest_version = (
        db.query(PromptVersion)
        .filter(PromptVersion.prompt_id == prompt_id)
        .order_by(PromptVersion.version_number.desc())
        .first()
    )
    next_version_num = (latest_version.version_number + 1) if latest_version else 1
    parent_version_id = latest_version.id if latest_version else None

    # Get Version 1 tokens for token reduction baseline
    v1 = (
        db.query(PromptVersion)
        .filter(PromptVersion.prompt_id == prompt_id, PromptVersion.version_number == 1)
        .first()
    )
    baseline_tokens = v1.token_count if v1 and v1.token_count > 0 else 1

    # Extract variables and calculate current token count
    extracted_vars = extract_template_variables(version_in.user_prompt_template)
    provider = get_provider(version_in.target_model)
    full_text = (version_in.system_prompt or "") + version_in.user_prompt_template
    current_tokens = provider.count_tokens(full_text)

    # Calculate token reduction percentage compared to baseline
    token_savings_pct = max(0.0, round(((baseline_tokens - current_tokens) / baseline_tokens) * 100.0, 2))

    new_version = PromptVersion(
        prompt_id=prompt_id,
        version_number=next_version_num,
        system_prompt=version_in.system_prompt,
        user_prompt_template=version_in.user_prompt_template,
        variables=extracted_vars,
        target_model=version_in.target_model,
        token_count=current_tokens,
        token_reduction_pct=token_savings_pct,
        commit_note=version_in.commit_note or f"Version {next_version_num} commit",
        parent_version_id=parent_version_id
    )
    db.add(new_version)
    db.commit()
    db.refresh(new_version)

    # Update active_version_id pointer
    db_prompt.active_version_id = new_version.id
    db.commit()

    return new_version
