/**
 * Zustand store for application state management
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface CompanyProfile {
  company_name: string;
  company_description: string;
  brand_voice: string;
  brand_voice_custom?: string;
  extracted_context?: string;
}

export interface Trend {
  trend_name: string;
  description: string;
  why_its_hot: string;
  relevance_score: number;
  opportunity_window: string;
  target_audience?: string;
}

export interface Campaign {
  id: string;
  narrative: string;
  blog: string;
  social_media: {
    twitter: string[];
    instagram: string[];
    tiktok: string[];
  };
  tshirt_designs: string[];
  generated_at: string;
}

interface AppState {
  // Profile
  profile: CompanyProfile | null;
  setProfile: (profile: CompanyProfile) => void;
  clearProfile: () => void;

  // Trends
  selectedTrend: Trend | null;
  setSelectedTrend: (trend: Trend) => void;
  clearSelectedTrend: () => void;

  // Campaign
  currentCampaign: Campaign | null;
  setCurrentCampaign: (campaign: Campaign) => void;
  clearCurrentCampaign: () => void;

  // UI State
  isGenerating: boolean;
  setIsGenerating: (isGenerating: boolean) => void;
  generationStep: number;
  setGenerationStep: (step: number) => void;

  // Clear all
  reset: () => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      // Profile
      profile: null,
      setProfile: (profile) => set({ profile }),
      clearProfile: () => set({ profile: null }),

      // Trends
      selectedTrend: null,
      setSelectedTrend: (trend) => set({ selectedTrend: trend }),
      clearSelectedTrend: () => set({ selectedTrend: null }),

      // Campaign
      currentCampaign: null,
      setCurrentCampaign: (campaign) => set({ currentCampaign: campaign }),
      clearCurrentCampaign: () => set({ currentCampaign: null }),

      // UI State
      isGenerating: false,
      setIsGenerating: (isGenerating) => set({ isGenerating }),
      generationStep: 0,
      setGenerationStep: (step) => set({ generationStep: step }),

      // Clear all
      reset: () => set({
        profile: null,
        selectedTrend: null,
        currentCampaign: null,
        isGenerating: false,
        generationStep: 0,
      }),
    }),
    {
      name: 'zeitgeist-studio-storage',
      partialize: (state) => ({
        profile: state.profile,
        selectedTrend: state.selectedTrend,
        // Don't persist currentCampaign to avoid stale data
      }),
    }
  )
);
