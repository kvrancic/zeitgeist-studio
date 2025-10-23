/**
 * TypeScript type definitions
 */

export enum BrandVoice {
  PROFESSIONAL = 'professional',
  CASUAL = 'casual',
  EDGY = 'edgy',
  INSPIRATIONAL = 'inspirational',
  HUMOROUS = 'humorous',
  CUSTOM = 'custom',
}

export enum OpportunityWindow {
  PEAK_NOW = 'Peak: Now',
  GROWING = 'Growing',
  EARLY = 'Early',
}

export enum AgentStep {
  PHILOSOPHER = 1,
  ARCHITECT = 2,
  OPTIMIZER = 3,
  ARCHITECT_FINAL = 4,
}

export const AGENT_NAMES = {
  [AgentStep.PHILOSOPHER]: 'Zeitgeist Philosopher',
  [AgentStep.ARCHITECT]: 'Cynical Content Architect',
  [AgentStep.OPTIMIZER]: 'Brutalist Optimizer',
  [AgentStep.ARCHITECT_FINAL]: 'Final Content Polish',
};

export const AGENT_DESCRIPTIONS = {
  [AgentStep.PHILOSOPHER]: 'Analyzing cultural trends and psychological drivers...',
  [AgentStep.ARCHITECT]: 'Creating viral content and compelling narratives...',
  [AgentStep.OPTIMIZER]: 'Optimizing for SEO and conversion metrics...',
  [AgentStep.ARCHITECT_FINAL]: 'Polishing final campaign content...',
};

export interface StreamingProgress {
  step: number;
  agent: string;
  status: 'working' | 'complete' | 'error';
  message: string;
  data?: any;
}
