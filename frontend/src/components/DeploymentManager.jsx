/**
 * ==============================================================================
 * PRE-AI Production Deployment & API Snippet Manager (src/components/DeploymentManager.jsx)
 * ------------------------------------------------------------------------------
 * CONCEPT EXPLANATION:
 * Production Release Management:
 * 1. Decouples frontend applications from prompt drafts.
 * 2. Provides immutable deployment endpoints (STAGING vs PRODUCTION).
 * 3. Generates ready-to-copy code snippets (cURL, Python, JS) for external teams.
 * 4. Enables instant 1-click rollbacks with zero downtime.
 * ==============================================================================
 */

import React, { useState } from 'react';
import { 
  Rocket, 
  ShieldCheck, 
  Terminal, 
  Copy, 
  Check, 
  RotateCcw, 
  Globe, 
  KeyRound 
} from 'lucide-react';

export function DeploymentManager() {
  const [activeSnippetTab, setActiveSnippetTab] = useState('curl');
  const [copied, setCopied] = useState(false);

  // Active production deployment state
  const deploymentInfo = {
    environment: 'PRODUCTION',
    deploymentKey: 'dep_prod_84fa19b2',
    promptTitle: 'Customer Support Agent',
    activeVersion: 'v2 (Refined for 31% token savings)',
    endpointUrl: 'http://localhost:8000/api/v1/deployments/dep_prod_84fa19b2/execute',
    lastDeployed: 'Just now'
  };

  const codeSnippets = {
    curl: `curl -X POST "${deploymentInfo.endpointUrl}" \\
  -H "Content-Type: application/json" \\
  -d '{
    "variables": {
      "order_id": "ORD-98421"
    }
  }'`,
    python: `import requests

url = "${deploymentInfo.endpointUrl}"
payload = {
    "variables": {
        "order_id": "ORD-98421"
    }
}

response = requests.post(url, json=payload)
print(response.json())`,
    javascript: `const response = await fetch("${deploymentInfo.endpointUrl}", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    variables: { order_id: "ORD-98421" }
  })
});

const data = await response.json();
console.log(data);`
  };

  const handleCopySnippet = () => {
    navigator.clipboard.writeText(codeSnippets[activeSnippetTab]);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Header */}
      <div className="card">
        <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Rocket size={24} color="#818cf8" />
          Production Deployments & API Serving
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '4px' }}>
          Serve production-ready prompt versions to downstream web applications via immutable API keys.
        </p>
      </div>

      {/* Deployment Status Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        
        {/* Production Environment Card */}
        <div className="card" style={{ border: '1px solid var(--success-border)' }}>
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ShieldCheck size={18} color="#34d399" />
              <strong style={{ fontSize: '1.1rem' }}>Production Environment</strong>
            </div>
            <span className="badge badge-success">Active & Serving</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.9rem' }}>
            <div>
              <span className="input-label">Pinned Prompt Version:</span>
              <strong style={{ color: '#a5b4fc' }}>{deploymentInfo.activeVersion}</strong>
            </div>

            <div>
              <span className="input-label">Deployment Secret Key:</span>
              <code style={{ background: '#0d0d12', padding: '4px 8px', borderRadius: '4px' }}>
                {deploymentInfo.deploymentKey}
              </code>
            </div>

            <div>
              <span className="input-label">Last Deployed:</span>
              <span style={{ color: 'var(--text-muted)' }}>{deploymentInfo.lastDeployed}</span>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '10px', marginTop: '18px' }}>
            <button className="btn btn-secondary" style={{ flex: 1 }}>
              <RotateCcw size={14} />
              Instant Rollback to v1
            </button>
            <button className="btn btn-primary" style={{ flex: 1 }}>
              <Rocket size={14} />
              Promote Staging to Prod
            </button>
          </div>
        </div>

        {/* Staging Environment Card */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Globe size={18} color="#fbbf24" />
              <strong style={{ fontSize: '1.1rem' }}>Staging Environment</strong>
            </div>
            <span className="badge badge-warning">Testing v3</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.9rem' }}>
            <div>
              <span className="input-label">Pinned Prompt Version:</span>
              <strong style={{ color: '#fbbf24' }}>v3 (Experimental Ollama compression)</strong>
            </div>

            <div>
              <span className="input-label">Deployment Secret Key:</span>
              <code style={{ background: '#0d0d12', padding: '4px 8px', borderRadius: '4px' }}>
                dep_stage_412e091
              </code>
            </div>

            <div>
              <span className="input-label">Status:</span>
              <span style={{ color: '#34d399' }}>Passed 100% Evaluation Suite</span>
            </div>
          </div>

          <button className="btn btn-secondary" style={{ width: '100%', marginTop: '18px' }}>
            Run Staging Integration Tests
          </button>
        </div>

      </div>

      {/* Interactive Code Snippet Generator */}
      <div className="card">
        <div className="card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Terminal size={18} color="#818cf8" />
            <strong style={{ fontSize: '1rem' }}>Production API Code Integration Snippet</strong>
          </div>

          <button className="btn btn-secondary" style={{ padding: '6px 12px' }} onClick={handleCopySnippet}>
            {copied ? <Check size={14} color="#34d399" /> : <Copy size={14} />}
            {copied ? 'Copied' : 'Copy Snippet'}
          </button>
        </div>

        {/* Language Tabs */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '14px' }}>
          {['curl', 'python', 'javascript'].map((lang) => (
            <button
              key={lang}
              className={`tab-btn ${activeSnippetTab === lang ? 'active' : ''}`}
              style={{ padding: '6px 14px', fontSize: '0.82rem' }}
              onClick={() => setActiveSnippetTab(lang)}
            >
              {lang.toUpperCase()}
            </button>
          ))}
        </div>

        {/* Code Container */}
        <div className="code-container" style={{ minHeight: '130px', color: '#67e8f9' }}>
          {codeSnippets[activeSnippetTab]}
        </div>
      </div>

    </div>
  );
}
