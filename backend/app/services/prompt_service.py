"""
==============================================================================
PRE-AI Prompt & Version Management Service (services/prompt_service.py)
------------------------------------------------------------------------------
CONCEPT EXPLANATION: "GitHub for Prompts" Service
Handles prompt creation, version committing, dynamic variable extraction, 
and version history queries.

Syntax & Mechanics:
- `re.findall`: Regular expression pattern matching for {{variable}} syntax.
- `dict.fromkeys()`: Deduplicates list elements while preserving order.
- `db.flush()` vs `db.commit()`: Flushes pending objects to SQL to generate 
  auto-increment IDs before creating child records, then commits atomically.
==============================================================================
"""

import re
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.prompt import Prompt, PromptVersion
from app.schemas.prompt import PromptCreate, PromptVersionCreate
from app.providers.factory import get_provider


def extract_template_variables(text: str) -> List[str]:
    r"""
    Functionality:
    Parses a prompt template for {{variable_name}} patterns.
    Example: "Hello {{name}}, order is {{order_id}}" -> ["name", "order_id"]

    Syntax Breakdown:
    - `r"..."`: Raw string (avoids backslash escape issues).
    - `\{\{`: Escaped literal double curly braces '{{'.
    - `\s*`: Matches zero or more whitespace characters.
    - `([a-zA-Z0-9_]+)`: Capturing group matching letters, digits, and underscores.
    - `dict.fromkeys(matches)`: Modern Python trick to remove duplicates while preserving order.
    """
    if not text:
        return []
    pattern = r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}"
    matches = re.findall(pattern, text)
    return list(dict.fromkeys(matches))


def create_prompt_with_initial_version(db: Session, prompt_in: PromptCreate) -> Prompt:
    """
    Functionality:
    Creates a new Prompt repository along with its initial Version 1 snapshot.

    Syntax Breakdown:
    - `db.add()`: Schedules the new Prompt model to be inserted into PostgreSQL.
    - `db.flush()`: Executes the SQL INSERT within the active transaction so that
      PostgreSQL assigns `db_prompt.id`, without committing the transaction yet.
    - `db.commit()`: Commits both the Prompt and its Version 1 snapshot atomically.
    """
    # 1. Create parent Prompt repository
    db_prompt = Prompt(
        title=prompt_in.title,
        description=prompt_in.description,
        project_id=prompt_in.project_id
    )
    db.add(db_prompt)
    db.flush() # Syntax: Generates db_prompt.id needed for the child PromptVersion record

    # 2. Extract dynamic template variables
    extracted_vars = extract_template_variables(prompt_in.initial_version.user_prompt_template)
    
    # 3. Calculate initial token count baseline
    provider = get_provider(prompt_in.initial_version.target_model)
    full_text = (prompt_in.initial_version.system_prompt or "") + prompt_in.initial_version.user_prompt_template
    initial_tokens = provider.count_tokens(full_text)

    # 4. Create Version 1 snapshot record
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

    # Syntax: Pin active_version_id to initial version
    db_prompt.active_version_id = db_version.id
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


def create_new_prompt_version(
    db: Session, prompt_id: int, version_in: PromptVersionCreate
) -> PromptVersion:
    """
    Functionality:
    Commits a new version snapshot to an existing prompt repository.
    Calculates token reduction percentage relative to Version 1.

    Syntax Breakdown:
    - `.order_by(PromptVersion.version_number.desc()).first()`: 
      Fetches highest existing version number to increment sequentially (1 -> 2 -> 3).
    - `parent_version_id`: Stores the predecessor version ID for Git-like parent tracking.
    """
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not db_prompt:
        raise ValueError(f"Prompt with ID {prompt_id} not found")

    # Syntax: Query highest version number for sequential incrementing
    latest_version = (
        db.query(PromptVersion)
        .filter(PromptVersion.prompt_id == prompt_id)
        .order_by(PromptVersion.version_number.desc())
        .first()
    )
    next_version_num = (latest_version.version_number + 1) if latest_version else 1
    parent_version_id = latest_version.id if latest_version else None

    # Fetch Version 1 baseline tokens to compute % savings
    v1 = (
        db.query(PromptVersion)
        .filter(PromptVersion.prompt_id == prompt_id, PromptVersion.version_number == 1)
        .first()
    )
    baseline_tokens = v1.token_count if v1 and v1.token_count > 0 else 1

    # Extract template variables and compute current token count
    extracted_vars = extract_template_variables(version_in.user_prompt_template)
    provider = get_provider(version_in.target_model)
    full_text = (version_in.system_prompt or "") + version_in.user_prompt_template
    current_tokens = provider.count_tokens(full_text)

    # Syntax: Token savings formula: ((Original - Current) / Original) * 100
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

    # Syntax: Update active pointer so production queries resolve to the latest commit
    db_prompt.active_version_id = new_version.id
    db.commit()

    return new_version
