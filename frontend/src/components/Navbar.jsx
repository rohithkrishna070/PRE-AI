/**
 * ==============================================================================
 * PRE-AI Modern Developer Header (src/components/Navbar.jsx)
 * ------------------------------------------------------------------------------
 * CONCEPT EXPLANATION:
 * Top navigation bar featuring brand identity, Lucide React icons, live system 
 * status badge, and tab switching between the 5 core platform features.
 * ==============================================================================
 */

import React from 'react';
import { 
  Sparkles, 
  GitCompare, 
  FlaskConical, 
  Rocket, 
  BarChart3, 
  Zap, 
  Layers 
} from 'lucide-react';

export function Navbar({ activeTab, setActiveTab }) {
  const navTabs = [
    { id: 'dashboard', label: 'Analytics', icon: BarChart3 },
    { id: 'refine', label: 'Token Refiner', icon: Sparkles },
    { id: 'diff', label: 'GitHub for Prompts', icon: GitCompare },
    { id: 'experiments', label: 'A/B Model Arena', icon: FlaskConical },
    { id: 'deployments', label: 'Deployments & API', icon: Rocket },
  ];

  return (
    <header style={{
      background: 'rgba(18, 18, 22, 0.85)',
      backdropFilter: 'blur(12px)',
      borderBottom: '1px solid var(--border-subtle)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      padding: '12px 28px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: '28px'
    }}>
      {/* Brand Identity */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <div style={{
          background: 'var(--accent-gradient)',
          padding: '8px',
          borderRadius: '10px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 0 16px rgba(99, 102, 241, 0.4)'
        }}>
          <Zap size={20} color="#ffffff" />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '1.2rem', fontWeight: 800, letterSpacing: '-0.02em', color: '#ffffff' }}>
              PRE-AI
            </span>
            <span className="badge badge-primary">v1.0.0</span>
          </div>
          <small style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>
            Prompt Engineering & Token Optimization Studio
          </small>
        </div>
      </div>

      {/* Navigation Tabs */}
      <nav style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
        {navTabs.map((tab) => {
          const IconComponent = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              className={`tab-btn ${isActive ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <IconComponent size={16} />
              {tab.label}
            </button>
          );
        })}
      </nav>

      {/* Status Pill */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <span className="badge badge-success" style={{ gap: '6px' }}>
          <span style={{
            width: '6px',
            height: '6px',
            borderRadius: '50%',
            background: '#34d399',
            boxShadow: '0 0 8px #34d399'
          }} />
          Engine Online
        </span>
      </div>
    </header>
  );
}
