/**
 * ==============================================================================
 * PRE-AI Centralized API Client (src/services/api.js)
 * ------------------------------------------------------------------------------
 * CONCEPT EXPLANATION:
 * Central API Service wrapping Axios to communicate with all FastAPI REST endpoints.
 * Handles Projects, Prompts, Versioning, Token Refinement, Experiments, and Deployments.
 * ==============================================================================
 */

import axios from 'axios';

// Base API URL pointing to FastAPI backend v1 prefix
const API_BASE = 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ------------------------------------------------------------------------------
// 1. Platform Analytics & Stats
// ------------------------------------------------------------------------------
export const fetchStats = async () => {
  const response = await apiClient.get('/audit/stats');
  return response.data;
};

// ------------------------------------------------------------------------------
// 2. AI Prompt Auto-Refinement (Token Reduction Engine)
// ------------------------------------------------------------------------------
export const refinePrompt = async (payload) => {
  // payload: { user_prompt, system_prompt, target_model, optimization_goal }
  const response = await apiClient.post('/refine/', payload);
  return response.data;
};

// ------------------------------------------------------------------------------
// 3. Project Workspaces CRUD
// ------------------------------------------------------------------------------
export const fetchProjects = async () => {
  const response = await apiClient.get('/projects/');
  return response.data;
};

export const createProject = async (data) => {
  const response = await apiClient.post('/projects/', data);
  return response.data;
};

// ------------------------------------------------------------------------------
// 4. Prompts & Version History ("GitHub for Prompts")
// ------------------------------------------------------------------------------
export const fetchPrompts = async (projectId) => {
  const url = projectId ? `/prompts/?project_id=${projectId}` : '/prompts/';
  const response = await apiClient.get(url);
  return response.data;
};

export const getPrompt = async (promptId) => {
  const response = await apiClient.get(`/prompts/${promptId}`);
  return response.data;
};

export const createPrompt = async (data) => {
  const response = await apiClient.post('/prompts/', data);
  return response.data;
};

export const commitPromptVersion = async (promptId, versionData) => {
  const response = await apiClient.post(`/prompts/${promptId}/versions`, versionData);
  return response.data;
};

// ------------------------------------------------------------------------------
// 5. Multi-Model A/B Experiments
// ------------------------------------------------------------------------------
export const runExperiment = async (experimentData) => {
  // experimentData: { name, project_id, prompt_version_id, target_models }
  const response = await apiClient.post('/experiments/', experimentData);
  return response.data;
};

// ------------------------------------------------------------------------------
// 6. Staging & Production Deployments
// ------------------------------------------------------------------------------
export const promoteDeployment = async (deploymentData) => {
  // deploymentData: { prompt_id, prompt_version_id, environment }
  const response = await apiClient.post('/deployments/', deploymentData);
  return response.data;
};

export default apiClient;
