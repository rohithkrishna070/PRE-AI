/**
 * ==============================================================================
 * PRE-AI Visual Version Diff Viewer (src/components/DiffViewer.jsx)
 * ------------------------------------------------------------------------------
 * CONCEPT EXPLANATION: "GitHub for Prompts" Visual Diff Engine
 * In Git, a `git diff` shows additions and deletions between two commits.
 * 
 * This component provides:
 * 1. Side-by-side or unified diff comparison between any two prompt versions.
 * 2. Visual green additions and red deletions.
 * 3. Token count differential (exact tokens gained/lost).
 * 4. One-click version rollback and release promotion.
 * ==============================================================================
 */

import React, { useState, useEffect, useMemo } from 'react';
import { 
  GitCompare, 
  GitBranch, 
  GitCommit, 
  History, 
  ArrowLeftRight, 
  RotateCcw, 
  Rocket, 
  Check, 
  FileText 
} from 'lucide-react';
import { fetchPrompts, promoteDeployment } from '../services/api';

// Simple word-level diff algorithm for clean visualization
function computeWordDiff(textA, textB) {
  if (!textA && !textB) return [];
  const wordsA = (textA || '').split(/(\s+)/);
  const wordsB = (textB || '').split(/(\s+)/);

  // Quick word match comparison
  const diff = [];
  let i = 0, j = 0;
  while (i < wordsA.length || j < wordsB.length) {
    if (i < wordsA.length && j < wordsB.length && wordsA[i] === wordsB[j]) {
      diff.push({ type: 'same', text: wordsA[i] });
      i++;
      j++;
    } else if (j < wordsB.length && (!wordsA.includes(wordsB[j]) || wordsB.indexOf(wordsA[i]) === -1)) {
      diff.push({ type: 'added', text: wordsB[j] });
      j++;
    } else if (i < wordsA.length) {
      diff.push({ type: 'removed', text: wordsA[i] });
      i++;
    } else {
      diff.push({ type: 'added', text: wordsB[j] });
      j++;
    }
  }
  return diff;
}

export function DiffViewer() {
  const [prompts, setPrompts] = useState([]);
  const [selectedPromptId, setSelectedPromptId] = useState(null);
  const [versionAId, setVersionAId] = useState(null);
  const [versionBId, setVersionBId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionNotice, setActionNotice] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchPrompts();
        setPrompts(data);
        if (data.length > 0) {
          setSelectedPromptId(data[0].id);
          const versions = data[0].versions || [];
          if (versions.length >= 2) {
            setVersionAId(versions[0].id);
            setVersionBId(versions[versions.length - 1].id);
          } else if (versions.length === 1) {
            setVersionAId(versions[0].id);
            setVersionBId(versions[0].id);
          }
        }
      } catch (err) {
        console.error('Error loading prompts for diff:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const activePrompt = useMemo(() => {
    return prompts.find((p) => p.id === Number(selectedPromptId)) || null;
  }, [prompts, selectedPromptId]);

  const versionA = useMemo(() => {
    if (!activePrompt?.versions) return null;
    return activePrompt.versions.find((v) => v.id === Number(versionAId)) || null;
  }, [activePrompt, versionAId]);

  const versionB = useMemo(() => {
    if (!activePrompt?.versions) return null;
    return activePrompt.versions.find((v) => v.id === Number(versionBId)) || null;
  }, [activePrompt, versionBId]);

  // Compute Word Diff
  const diffElements = useMemo(() => {
    return computeWordDiff(
      versionA?.user_prompt_template || '',
      versionB?.user_prompt_template || ''
    );
  }, [versionA, versionB]);

  // Handle Deployment
  const handleDeploy = async (versionId) => {
    try {
      await promoteDeployment({
        prompt_id: activePrompt.id,
        prompt_version_id: versionId,
        environment: 'PRODUCTION'
      });
      setActionNotice('Promoted to Production successfully!');
      setTimeout(() => setActionNotice(null), 2500);
    } catch (err) {
      console.error('Deploy error:', err);
    }
  };

  if (loading) {
    return <div className="card">Loading Version Control Repositories...</div>;
  }

  if (prompts.length === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
        <GitBranch size={48} color="#64647a" style={{ margin: '0 auto 16px auto' }} />
        <h3>No Prompt Repositories Yet</h3>
        <p style={{ color: 'var(--text-secondary)' }}>
          Create and commit your first prompt version in the <strong>Token Refiner</strong> tab!
        </p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Header & Controls Bar */}
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <GitCompare size={24} color="#818cf8" />
            Visual Version Diff Viewer
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '4px' }}>
            Compare prompt iterations, inspect word-level diffs, and manage commit history.
          </p>
        </div>

        {/* Action Toast */}
        {actionNotice && (
          <span className="badge badge-success">
            <Check size={14} /> {actionNotice}
          </span>
        )}
      </div>

      {/* Selectors Bar */}
      <div className="card" style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr 1fr', gap: '16px' }}>
        <div>
          <label className="input-label">Select Prompt Repository</label>
          <select 
            className="select-field"
            value={selectedPromptId || ''}
            onChange={(e) => {
              const pId = Number(e.target.value);
              setSelectedPromptId(pId);
              const p = prompts.find((item) => item.id === pId);
              if (p?.versions?.length > 0) {
                setVersionAId(p.versions[0].id);
                setVersionBId(p.versions[p.versions.length - 1].id);
              }
            }}
          >
            {prompts.map((p) => (
              <option key={p.id} value={p.id}>{p.title} ({p.versions?.length || 0} versions)</option>
            ))}
          </select>
        </div>

        <div>
          <label className="input-label">Base Version (Left)</label>
          <select 
            className="select-field"
            value={versionAId || ''}
            onChange={(e) => setVersionAId(Number(e.target.value))}
          >
            {activePrompt?.versions?.map((v) => (
              <option key={v.id} value={v.id}>
                v{v.version_number} — {v.commit_note?.substring(0, 25)} ({v.token_count}t)
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="input-label">Compared Version (Right)</label>
          <select 
            className="select-field"
            value={versionBId || ''}
            onChange={(e) => setVersionBId(Number(e.target.value))}
          >
            {activePrompt?.versions?.map((v) => (
              <option key={v.id} value={v.id}>
                v{v.version_number} — {v.commit_note?.substring(0, 25)} ({v.token_count}t)
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Metrics Comparison Banner */}
      {versionA && versionB && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '14px' }}>
          <div className="stat-card">
            <span className="stat-label">Base v{versionA.version_number} Tokens</span>
            <span style={{ fontSize: '1.4rem', fontWeight: 800 }}>{versionA.token_count}</span>
          </div>
          <div className="stat-card">
            <span className="stat-label">Compared v{versionB.version_number} Tokens</span>
            <span style={{ fontSize: '1.4rem', fontWeight: 800 }}>{versionB.token_count}</span>
          </div>
          <div className="stat-card">
            <span className="stat-label">Token Delta</span>
            <span style={{ 
              fontSize: '1.4rem', 
              fontWeight: 800,
              color: versionA.token_count >= versionB.token_count ? '#34d399' : '#fb7185'
            }}>
              {versionB.token_count - versionA.token_count} tokens
            </span>
          </div>
          <div className="stat-card">
            <span className="stat-label">Action</span>
            <button 
              className="btn btn-primary"
              style={{ padding: '6px 12px', fontSize: '0.82rem', marginTop: '4px' }}
              onClick={() => handleDeploy(versionB.id)}
            >
              <Rocket size={14} />
              Deploy v{versionB.version_number}
            </button>
          </div>
        </div>
      )}

      {/* Visual Word Diff Render */}
      <div className="card">
        <div className="card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <FileText size={18} color="#818cf8" />
            <span style={{ fontWeight: 700 }}>Visual Word-by-Word Diff</span>
          </div>
          <div style={{ display: 'flex', gap: '12px', fontSize: '0.82rem' }}>
            <span className="badge badge-danger">- Removed Content</span>
            <span className="badge badge-success">+ Added / Optimized</span>
          </div>
        </div>

        <div style={{
          background: '#0a0a0f',
          border: '1px solid var(--border-subtle)',
          borderRadius: '10px',
          padding: '20px',
          fontFamily: 'JetBrains Mono',
          fontSize: '0.9rem',
          lineHeight: 2,
          minHeight: '140px'
        }}>
          {diffElements.map((item, idx) => {
            if (item.type === 'removed') {
              return (
                <span 
                  key={idx} 
                  style={{ 
                    background: 'var(--diff-del-bg)', 
                    color: 'var(--diff-del-text)', 
                    textDecoration: 'line-through',
                    padding: '2px 4px',
                    borderRadius: '3px'
                  }}
                >
                  {item.text}
                </span>
              );
            } else if (item.type === 'added') {
              return (
                <span 
                  key={idx} 
                  style={{ 
                    background: 'var(--diff-add-bg)', 
                    color: 'var(--diff-add-text)', 
                    fontWeight: 600,
                    padding: '2px 4px',
                    borderRadius: '3px'
                  }}
                >
                  {item.text}
                </span>
              );
            }
            return <span key={idx} style={{ color: '#d4d4d8' }}>{item.text}</span>;
          })}
        </div>
      </div>

      {/* Commit History Timeline */}
      <div className="card">
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <History size={18} color="#818cf8" />
          Commit History Log ({activePrompt?.versions?.length || 0} Versions)
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {activePrompt?.versions?.map((ver) => (
            <div 
              key={ver.id}
              style={{
                background: '#0d0d12',
                border: '1px solid var(--border-subtle)',
                borderRadius: '8px',
                padding: '14px 18px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span className="badge badge-primary">Version {ver.version_number}</span>
                  <strong>{ver.commit_note || 'Snapshot commit'}</strong>
                </div>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: '4px' }}>
                  Target: <code>{ver.target_model}</code> | Token Count: <code>{ver.token_count}</code> tokens
                </div>
              </div>

              <div style={{ display: 'flex', gap: '8px' }}>
                <span className="badge badge-success">{ver.token_reduction_pct}% Saved</span>
                <button 
                  className="btn btn-secondary"
                  style={{ padding: '5px 10px', fontSize: '0.8rem' }}
                  onClick={() => handleDeploy(ver.id)}
                >
                  <Rocket size={13} />
                  Promote
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
