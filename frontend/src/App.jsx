/**
 * ==============================================================================
 * PRE-AI Main Application Shell (src/App.jsx)
 * ------------------------------------------------------------------------------
 * CONCEPT EXPLANATION:
 * Root application component assembling:
 * 1. Global Navbar with tab state.
 * 2. Five dedicated feature views:
 *    - Analytics Dashboard
 *    - Token Refiner Playground
 *    - Visual Version Diff Viewer ("GitHub for Prompts")
 *    - Multi-Model A/B Experiment Arena
 *    - Production Deployment & API Serving Manager
 * ==============================================================================
 */

import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Dashboard } from './components/Dashboard';
import { PromptRefiner } from './components/PromptRefiner';
import { DiffViewer } from './components/DiffViewer';
import { ExperimentArena } from './components/ExperimentArena';
import { DeploymentManager } from './components/DeploymentManager';

export default function App() {
  const [activeTab, setActiveTab] = useState('refine');

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-main)' }}>
      {/* Sticky Top Header */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <main style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 24px 60px 24px' }}>
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'refine' && <PromptRefiner />}
        {activeTab === 'diff' && <DiffViewer />}
        {activeTab === 'experiments' && <ExperimentArena />}
        {activeTab === 'deployments' && <DeploymentManager />}
      </main>
    </div>
  );
}
