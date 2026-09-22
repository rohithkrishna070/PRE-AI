/**
 * ==============================================================================
 * PRE-AI Version History Component (src/components/VersionHistory.jsx)
 * ------------------------------------------------------------------------------
 * CONCEPT EXPLANATION: "GitHub for Prompts" Commit History View
 * Displays prompt repositories, version history logs (Version 1, Version 2...), 
 * commit notes, target models, and token reduction metrics.
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { fetchPrompts } from '../services/api';

export function VersionHistory() {
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadPrompts() {
      try {
        const data = await fetchPrompts();
        setPrompts(data);
      } catch (err) {
        console.error('Error fetching prompts:', err);
      } finally {
        setLoading(false);
      }
    }
    loadPrompts();
  }, []);

  if (loading) {
    return <div aria-busy="true">Loading Prompt Version Repositories...</div>;
  }

  return (
    <div>
      <h2>📜 GitHub for Prompts - Version Control History</h2>
      <p style={{ color: '#94a3b8' }}>
        Track commits, review version changes, compare token savings, and inspect prompt history.
      </p>

      {prompts.length === 0 ? (
        <article>
          <p>No prompt repositories found. Use the Token Refiner Playground to generate and commit prompts!</p>
        </article>
      ) : (
        prompts.map((prompt) => (
          <article key={prompt.id} style={{ marginBottom: '2rem' }}>
            <header>
              <h3 style={{ margin: 0, color: '#818cf8' }}>📦 {prompt.title}</h3>
              <small>{prompt.description || 'Prompt Repository'}</small>
            </header>

            <h4>Commit History ({prompt.versions?.length || 0} Versions):</h4>
            {prompt.versions && prompt.versions.map((ver) => (
              <div key={ver.id} style={{ background: '#181825', padding: '12px', borderRadius: '6px', marginBottom: '10px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <strong>🔖 Version {ver.version_number} — {ver.commit_note}</strong>
                  <span className="badge badge-success">{ver.token_reduction_pct}% Token Savings</span>
                </div>

                <div style={{ margin: '8px 0', fontSize: '0.9rem', color: '#a6adc8' }}>
                  Target Model: <code>{ver.target_model}</code> | Token Count: <code>{ver.token_count}</code> tokens
                </div>

                <div className="code-block" style={{ fontSize: '0.85rem' }}>
                  {ver.user_prompt_template}
                </div>
              </div>
            ))}
          </article>
        ))
      )}
    </div>
  );
}
