/**
 * ==============================================================================
 * PRE-AI Executive Analytics Dashboard (src/components/Dashboard.jsx)
 * ------------------------------------------------------------------------------
 * CONCEPT EXPLANATION:
 * Executive analytics dashboard providing high-level KPIs:
 * 1. Token Reduction percentages & cumulative cost savings.
 * 2. Total Prompts & Version Commit Snapshots.
 * 3. Interactive workspace projects list with creation modal.
 * 4. Recent audit activity stream.
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  TrendingDown, 
  Layers, 
  GitCommit, 
  Coins, 
  Plus, 
  FolderPlus, 
  CheckCircle,
  Activity
} from 'lucide-react';
import { fetchStats, fetchProjects, createProject } from '../services/api';

export function Dashboard() {
  const [stats, setStats] = useState(null);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  // New Project Modal State
  const [showModal, setShowModal] = useState(false);
  const [projectName, setProjectName] = useState('');
  const [projectDesc, setProjectDesc] = useState('');

  const loadDashboardData = async () => {
    try {
      const statsData = await fetchStats();
      const projectsData = await fetchProjects();
      setStats(statsData);
      setProjects(projectsData);
    } catch (err) {
      console.error('Error loading dashboard stats:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const handleCreateProject = async (e) => {
    e.preventDefault();
    if (!projectName.trim()) return;
    try {
      await createProject({
        name: projectName,
        description: projectDesc,
      });
      setProjectName('');
      setProjectDesc('');
      setShowModal(false);
      loadDashboardData();
    } catch (err) {
      console.error('Error creating project:', err);
    }
  };

  if (loading) {
    return <div className="card">Loading PRE-AI Analytics Engine...</div>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Top Banner */}
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <BarChart3 size={24} color="#818cf8" />
            Executive Analytics & Platform Overview
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '4px' }}>
            Continuous monitoring of prompt optimization metrics, token compression rates, and model speed.
          </p>
        </div>

        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} />
          New Project Workspace
        </button>
      </div>

      {/* KPI Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
        
        <div className="stat-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span className="stat-label">Avg. Token Reduction</span>
            <span className="badge badge-success">
              <TrendingDown size={12} /> Optimization
            </span>
          </div>
          <div className="stat-val" style={{ color: '#34d399' }}>
            {stats?.avg_token_reduction_pct || 0}%
          </div>
          <small style={{ color: 'var(--text-muted)' }}>Average reduction per prompt version</small>
        </div>

        <div className="stat-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span className="stat-label">Prompt Repositories</span>
            <span className="badge badge-primary">Active</span>
          </div>
          <div className="stat-val" style={{ color: '#818cf8' }}>
            {stats?.total_prompts || 0}
          </div>
          <small style={{ color: 'var(--text-muted)' }}>Tracked under version control</small>
        </div>

        <div className="stat-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span className="stat-label">Version Snapshots</span>
            <span className="badge badge-primary">Commits</span>
          </div>
          <div className="stat-val" style={{ color: '#f472b6' }}>
            {stats?.total_versions || 0}
          </div>
          <small style={{ color: 'var(--text-muted)' }}>Immutable snapshot checkpoints</small>
        </div>

        <div className="stat-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span className="stat-label">Tokens Processed</span>
            <span className="badge badge-warning">Throughput</span>
          </div>
          <div className="stat-val" style={{ color: '#fbbf24' }}>
            {stats?.total_tokens_consumed || 0}
          </div>
          <small style={{ color: 'var(--text-muted)' }}>Total input and output tokens</small>
        </div>

      </div>

      {/* Projects Grid */}
      <div className="card">
        <div className="card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Layers size={18} color="#818cf8" />
            <strong style={{ fontSize: '1rem' }}>Project Workspaces ({projects.length})</strong>
          </div>
        </div>

        {projects.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '24px 0' }}>
            <p style={{ color: 'var(--text-secondary)' }}>No workspaces created yet.</p>
            <button className="btn btn-secondary" style={{ marginTop: '8px' }} onClick={() => setShowModal(true)}>
              <FolderPlus size={14} /> Create First Workspace
            </button>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
            {projects.map((proj) => (
              <div 
                key={proj.id}
                style={{
                  background: '#0d0d12',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '10px',
                  padding: '16px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '8px'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <strong style={{ fontSize: '1rem', color: '#f4f4f6' }}>{proj.name}</strong>
                  <span className="badge badge-primary">ID #{proj.id}</span>
                </div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                  {proj.description || 'General prompt engineering workspace.'}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recent Platform Activity */}
      <div className="card">
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <Activity size={18} color="#818cf8" />
          Live Audit Activity Stream
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.88rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', background: '#0d0d12', padding: '12px', borderRadius: '8px' }}>
            <CheckCircle size={16} color="#34d399" />
            <span>Refined Customer Support Prompt: compressed from 48 to 33 tokens (31% reduction).</span>
            <small style={{ color: 'var(--text-muted)', marginLeft: 'auto' }}>12 mins ago</small>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', background: '#0d0d12', padding: '12px', borderRadius: '8px' }}>
            <CheckCircle size={16} color="#818cf8" />
            <span>Promoted Prompt Version 2 to Production Release Endpoint.</span>
            <small style={{ color: 'var(--text-muted)', marginLeft: 'auto' }}>35 mins ago</small>
          </div>
        </div>
      </div>

      {/* Create Project Modal */}
      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3 style={{ marginBottom: '8px' }}>Create Project Workspace</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '18px' }}>
              Organize related prompts, models, and evaluation datasets into isolated project workspaces.
            </p>

            <form onSubmit={handleCreateProject} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div>
                <label className="input-label">Project Name</label>
                <input
                  type="text"
                  className="input-field"
                  placeholder="e.g. Financial Chatbot Prompts"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                  required
                />
              </div>

              <div>
                <label className="input-label">Description (Optional)</label>
                <input
                  type="text"
                  className="input-field"
                  placeholder="e.g. Prompts for customer account summaries and analytics"
                  value={projectDesc}
                  onChange={(e) => setProjectDesc(e.target.value)}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '8px' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Create Workspace
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
