/**
 * API client for Zeitgeist Studio backend
 */

import axios, { AxiosInstance } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutes for long-running campaign generation
});

// Health Check
export const healthCheck = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

// Profile Management
export interface CompanyProfile {
  company_name: string;
  company_description: string;
  brand_voice: string;
  brand_voice_custom?: string;
  extracted_context?: string;
}

export const createProfile = async (profile: CompanyProfile, files?: File[]) => {
  const formData = new FormData();
  formData.append('company_name', profile.company_name);
  formData.append('company_description', profile.company_description);
  formData.append('brand_voice', profile.brand_voice);

  if (profile.brand_voice_custom) {
    formData.append('brand_voice_custom', profile.brand_voice_custom);
  }

  if (files) {
    files.forEach(file => {
      formData.append('files', file);
    });
  }

  const response = await api.post('/api/profile/create', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

// Trend Discovery
export interface Trend {
  trend_name: string;
  description: string;
  why_its_hot: string;
  relevance_score: number;
  opportunity_window: string;
  target_audience?: string;
}

export const searchTrends = async (companyProfile: CompanyProfile) => {
  const response = await api.post('/api/trends/search', {
    company_name: companyProfile.company_name,
    company_description: companyProfile.company_description,
    industry: '', // Can be added later
  });
  return response.data;
};

export const submitManualTrend = async (topic: string, companyContext?: string) => {
  const response = await api.post('/api/trends/manual', {
    topic,
    company_context: companyContext,
  });
  return response.data;
};

// Campaign Generation (with SSE streaming)
export interface CampaignRequest {
  company_name: string;
  company_description: string;
  brand_voice: string;
  trend_name: string;
  trend_context: string;
  extracted_docs?: string;
}

export const generateCampaign = (
  request: CampaignRequest,
  onProgress: (data: any) => void,
  onComplete: (data: any) => void,
  onError: (error: any) => void
) => {
  const eventSource = new EventSource(
    `${API_URL}/api/campaign/generate?` + new URLSearchParams({
      company_name: request.company_name,
      company_description: request.company_description,
      brand_voice: request.brand_voice,
      trend_name: request.trend_name,
      trend_context: request.trend_context,
    })
  );

  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);

      if (data.status === 'complete') {
        onComplete(data);
        eventSource.close();
      } else if (data.status === 'error') {
        onError(new Error(data.message));
        eventSource.close();
      } else {
        onProgress(data);
      }
    } catch (error) {
      console.error('SSE parsing error:', error);
    }
  };

  eventSource.onerror = (error) => {
    onError(error);
    eventSource.close();
  };

  return eventSource;
};

// Export
export const exportPDF = async (campaignId: string, narrative: string, companyName: string) => {
  const response = await api.post('/api/export/pdf', {
    campaign_id: campaignId,
    narrative,
    company_name: companyName,
  }, {
    responseType: 'blob',
  });

  return response.data;
};

export const exportZIP = async (campaignData: any) => {
  const response = await api.post('/api/export/zip', campaignData, {
    responseType: 'blob',
  });

  return response.data;
};
