/**
 * ==============================================================================
 * PRE-AI Interactive Token Refiner Playground (src/components/PromptRefiner.jsx)
 * ------------------------------------------------------------------------------
 * CONCEPT EXPLANATION:
 * The flagship playground for Prompt Engineering & Token Optimization:
 * 1. Automatically parses and highlights {{variable}} placeholders.
 * 2. Live token estimation meter.
 * 3. AI Token Compression engine tailored for selected target models.
 * 4. In-place "Commit as Version" modal to record immutable versions.
 * ==============================================================================
 */

import React, { useState, useMemo } from 'react';
import { 
  Sparkles, 
  Cpu, 
  Sliders, 
  GitCommit, 
  ArrowRight, 
  Check, 
  Copy, 
  Eye, 
  Code2,
  TrendingDown
} from 'lucide-react';
import { refinePrompt, commitPromptVersion, fetchProjects, createPrompt } from '../services/api';

export function PromptRefiner() {
  const [userPrompt, setUserPrompt] = useState(
    'Please act as a professional and polite customer support assistant for Acme Corp. ' +
    'Whenever a user submits a refund request for {{order_id}}, please thoroughly verify ' +
    'their purchase date and explain our 30-day refund policy in a very kind and clear manner.'
  );
  const [targetModel, setTargetModel] = useState('gemini-1.5-flash');
  const [optimizationGoal, setOptimizationGoal] = useState('TOKEN_REDUCTION');
  const [loading, setLoading] = useState(false);
  const [refineResult, setRefineResult] = useState(null);
  const [copied, setCopied] = useState(false);

  // Dynamic Variable Values
  const [variableValues, setVariableValues] = useState({ order_id: 'ORD-98421' });

  // Commit Modal State
  const [showCommitModal, setShowCommitModal] = useState(false);
  const [commitTitle, setCommitTitle] = useState('Customer Support Prompt');
  const [commitNote, setCommitNote] = useState('Refined prompt: 30% fewer tokens');
  const [commitSuccess, setCommitSuccess] = useState(false);

  // Extract variables automatically using regex
  const detectedVariables = useMemo(() => {
    const matches = userPrompt.match(/\{\{\s*([a-zA-Z0-9_]+)\s*\}\}/g) || [];
    return Array.from(new Set(matches.map((m) => m.replace(/[{}]/g, '').trim())));
  }, [userPrompt]);

  // Live Interpolated Preview
  const livePreview = useMemo(() => {
    let text = userPrompt;
    detectedVariables.forEach((v) => {
      const val = variableValues[v] !== undefined ? variableValues[v] : `{{${v}}}`;
      text = text.replaceAll(`{{${v}}}`, val);
    });
    return text;
  }, [userPrompt, variableValues, detectedVariables]);

  // Estimated Tokens (Rule of thumb: ~4 characters per token)
  const estimatedInputTokens = useMemo(() => {
    return Math.max(1, Math.round(userPrompt.length / 4));
  }, [userPrompt]);

  // Handle Refinement Trigger
  const handleRefine = async (e) => {
    e.preventDefault();
    if (!userPrompt.trim()) return;

    setLoading(true);
    setRefineResult(null);
    try {
      const data = await refinePrompt({
        user_prompt: userPrompt,
        target_model: targetModel,
        optimization_goal: optimizationGoal,
      });
      setRefineResult(data);
    } catch (err) {
      console.error('Refinement error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Copy to Clipboard
  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Commit to Version Control
  const handleCommit = async (e) => {
    e.preventDefault();
    try {
      // Create new prompt repository or commit version
      const promptData = {
        title: commitTitle,
        description: `Model: ${targetModel} | Goal: ${optimizationGoal}`,
        project_id: 1, // Default workspace
        initial_version: {
          user_prompt_template: refineResult ? refineResult.refined_user_prompt : userPrompt,
          target_model: targetModel,
          commit_note: commitNote,
          variables: detectedVariables
        }
      };
      await createPrompt(promptData);
      setCommitSuccess(true);
      setTimeout(() => {
        setCommitSuccess(false);
        setShowCommitModal(false);
      }, 1800);
    } catch (err) {
      console.error('Commit error:', err);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Top Header Card */}
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Sparkles size={24} color="#818cf8" />
            AI Prompt Auto-Refinement Studio
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '4px' }}>
            Compress prompt instructions, eliminate token waste, and optimize formatting for specific LLM architectures.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button 
            className="btn btn-secondary"
            onClick={() => setShowCommitModal(true)}
          >
            <GitCommit size={16} />
            Commit Version
          </button>
        </div>
      </div>

      {/* Main Two-Column Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.1fr 0.9fr', gap: '24px' }}>
        
        {/* Left Column: Prompt Input & Configurations */}
        <div className="card">
          <form onSubmit={handleRefine} style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
            
            {/* Model & Goal Controls */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div>
                <label className="input-label">
                  <Cpu size={14} style={{ verticalAlign: 'middle', marginRight: '4px' }} />
                  Target AI Model Family
                </label>
                <select 
                  className="select-field"
                  value={targetModel}
                  onChange={(e) => setTargetModel(e.target.value)}
                >
                  <option value="gemini-1.5-flash">Google Gemini 1.5 Flash (Free Tier)</option>
                  <option value="gemini-1.5-pro">Google Gemini 1.5 Pro (Cloud)</option>
                  <option value="llama3:latest">Ollama Llama 3 (Local $0)</option>
                  <option value="mistral:latest">Ollama Mistral (Local $0)</option>
                </select>
              </div>

              <div>
                <label className="input-label">
                  <Sliders size={14} style={{ verticalAlign: 'middle', marginRight: '4px' }} />
                  Optimization Goal
                </label>
                <select 
                  className="select-field"
                  value={optimizationGoal}
                  onChange={(e) => setOptimizationGoal(e.target.value)}
                >
                  <option value="TOKEN_REDUCTION">⚡ Maximum Token Reduction</option>
                  <option value="CLARITY">🎯 Precision & Clarity</option>
                  <option value="FEW_SHOT">📚 Structured Instructions</option>
                </select>
              </div>
            </div>

            {/* Prompt Textarea with Character & Token Meter */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <label className="input-label" style={{ margin: 0 }}>Draft Prompt Template</label>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <span className="badge badge-primary">
                    ~{estimatedInputTokens} Tokens
                  </span>
                  <span className="badge" style={{ background: '#272732', color: '#a1a1aa' }}>
                    {userPrompt.length} Characters
                  </span>
                </div>
              </div>

              <textarea
                className="textarea-field"
                rows={9}
                value={userPrompt}
                onChange={(e) => setUserPrompt(e.target.value)}
                placeholder="Enter prompt draft... Use {{variable_name}} for dynamic inputs."
                required
              />
            </div>

            {/* Dynamic Variable Detected Section */}
            {detectedVariables.length > 0 && (
              <div style={{ 
                background: '#0d0d12', 
                border: '1px solid var(--border-subtle)', 
                borderRadius: '10px', 
                padding: '14px' 
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '10px' }}>
                  <Code2 size={16} color="#818cf8" />
                  <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>
                    Detected Variables ({detectedVariables.length})
                  </span>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px' }}>
                  {detectedVariables.map((v) => (
                    <div key={v}>
                      <small style={{ color: 'var(--text-muted)', fontFamily: 'JetBrains Mono' }}>{`{{${v}}}`}</small>
                      <input
                        type="text"
                        className="input-field"
                        style={{ padding: '6px 10px', fontSize: '0.82rem', marginTop: '4px' }}
                        value={variableValues[v] || ''}
                        onChange={(e) => setVariableValues({ ...variableValues, [v]: e.target.value })}
                        placeholder={`Value for ${v}...`}
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Submit Button */}
            <button 
              type="submit" 
              className="btn btn-primary" 
              style={{ width: '100%', padding: '12px' }}
              disabled={loading || !userPrompt.trim()}
            >
              {loading ? (
                <>✨ Optimizing & Compressing Tokens...</>
              ) : (
                <>
                  <Sparkles size={18} />
                  Execute Auto-Refinement Engine
                </>
              )}
            </button>
          </form>
        </div>

        {/* Right Column: Live Preview or Optimization Results */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          {/* Optimization Results Card */}
          {refineResult ? (
            <div className="card" style={{ border: '1px solid var(--success-border)' }}>
              <div className="card-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="badge badge-success">
                    <TrendingDown size={14} />
                    -{refineResult.tokens_saved} Tokens ({refineResult.token_reduction_pct}% Saved)
                  </span>
                </div>
                <button 
                  className="btn btn-secondary" 
                  style={{ padding: '4px 10px', fontSize: '0.8rem' }}
                  onClick={() => handleCopy(refineResult.refined_user_prompt)}
                >
                  {copied ? <Check size={14} color="#34d399" /> : <Copy size={14} />}
                  {copied ? 'Copied' : 'Copy'}
                </button>
              </div>

              <div style={{ marginBottom: '16px' }}>
                <span className="input-label">Optimized Output ({refineResult.refined_token_count} Tokens):</span>
                <div className="code-container" style={{ color: '#a7f3d0' }}>
                  {refineResult.refined_user_prompt}
                </div>
              </div>

              <div style={{ background: '#0d0d12', padding: '12px', borderRadius: '8px', fontSize: '0.84rem' }}>
                <strong style={{ color: '#818cf8' }}>Engine Optimization Summary:</strong>
                <p style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>
                  {refineResult.explanation}
                </p>
              </div>

              <button 
                className="btn btn-primary" 
                style={{ width: '100%', marginTop: '16px' }}
                onClick={() => setShowCommitModal(true)}
              >
                <GitCommit size={16} />
                Save as New Version Snapshot
              </button>
            </div>
          ) : (
            /* Live Interpolated Preview Card */
            <div className="card">
              <div className="card-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Eye size={16} color="#a5b4fc" />
                  <span style={{ fontWeight: 600, fontSize: '0.95rem' }}>Live Interpolated Preview</span>
                </div>
                <span className="badge" style={{ background: '#272732', color: '#a1a1aa' }}>
                  Interpolated Preview
                </span>
              </div>

              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
                This is how the final prompt text will appear when sent to the AI model with your dynamic values:
              </p>

              <div className="code-container" style={{ minHeight: '160px', color: '#cbd5e1' }}>
                {livePreview}
              </div>
            </div>
          )}

          {/* Quick Metrics Bar */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
            <div className="stat-card">
              <span className="stat-label">Model Architecture</span>
              <span style={{ fontSize: '1.1rem', fontWeight: 700, color: '#a5b4fc' }}>
                {targetModel}
              </span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Estimated Savings</span>
              <span style={{ fontSize: '1.1rem', fontWeight: 700, color: '#34d399' }}>
                ~25% - 40% Tokens
              </span>
            </div>
          </div>

        </div>
      </div>

      {/* Commit Version Modal */}
      {showCommitModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <GitCommit size={22} color="#818cf8" />
              Commit Prompt Version
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '20px' }}>
              Snapshot this prompt iteration into version control (like a Git commit).
            </p>

            {commitSuccess ? (
              <div style={{ textAlign: 'center', padding: '24px 0' }}>
                <Check size={48} color="#34d399" style={{ margin: '0 auto 12px auto' }} />
                <h4 style={{ color: '#34d399' }}>Version Committed Successfully!</h4>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                  Recorded snapshot into GitHub for Prompts history.
                </p>
              </div>
            ) : (
              <form onSubmit={handleCommit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div>
                  <label className="input-label">Prompt Repository Title</label>
                  <input
                    type="text"
                    className="input-field"
                    value={commitTitle}
                    onChange={(e) => setCommitTitle(e.target.value)}
                    required
                  />
                </div>

                <div>
                  <label className="input-label">Commit Message / Optimization Notes</label>
                  <input
                    type="text"
                    className="input-field"
                    value={commitNote}
                    onChange={(e) => setCommitNote(e.target.value)}
                    placeholder="e.g. Compressed instructions, removed conversational fluff"
                    required
                  />
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '10px' }}>
                  <button 
                    type="button" 
                    className="btn btn-secondary"
                    onClick={() => setShowCommitModal(false)}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Confirm Commit
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
