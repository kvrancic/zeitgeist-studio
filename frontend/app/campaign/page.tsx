'use client';

import { useRouter } from 'next/navigation';
import { useAppStore } from '@/lib/store';
import { useEffect } from 'react';
import CampaignGenerator from '@/components/CampaignGenerator';
import type { CampaignRequest } from '@/lib/api';

export default function CampaignPage() {
  const router = useRouter();
  const profile = useAppStore((state) => state.profile);
  const selectedTrend = useAppStore((state) => state.selectedTrend);

  useEffect(() => {
    // Redirect if profile or trend not set
    if (!profile) {
      router.push('/profile');
    } else if (!selectedTrend) {
      router.push('/trends');
    }
  }, [profile, selectedTrend, router]);

  if (!profile || !selectedTrend) {
    return null; // Will redirect
  }

  // Build campaign request from store data
  const campaignRequest: CampaignRequest = {
    company_name: profile.company_name,
    company_description: profile.company_description,
    brand_voice: profile.brand_voice,
    trend_name: selectedTrend.trend_name,
    trend_context: selectedTrend.description,
    extracted_docs: profile.extracted_context,
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 py-12">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Zeitgeist Studio</h1>
          <p className="text-lg text-gray-600">Step 3: Generate Marketing Campaign</p>
          <div className="mt-4 flex gap-4 justify-center items-center text-sm">
            <div className="bg-white px-4 py-2 rounded-lg shadow">
              <span className="text-gray-500">Company:</span>{' '}
              <span className="font-semibold text-gray-900">{profile.company_name}</span>
            </div>
            <div className="bg-white px-4 py-2 rounded-lg shadow">
              <span className="text-gray-500">Trend:</span>{' '}
              <span className="font-semibold text-gray-900">{selectedTrend.trend_name}</span>
            </div>
            <button
              onClick={() => router.push('/trends')}
              className="px-4 py-2 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-white transition-colors"
            >
              ← Change Trend
            </button>
          </div>
        </div>

        {/* Campaign Generator */}
        <CampaignGenerator
          request={campaignRequest}
          onComplete={(campaign) => {
            console.log('Campaign generated:', campaign);
            // Could save to store or navigate to results page
          }}
        />
      </div>
    </div>
  );
}
