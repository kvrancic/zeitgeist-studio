'use client';

import { useRouter } from 'next/navigation';
import { useAppStore } from '@/lib/store';
import { useEffect } from 'react';

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

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8 text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Zeitgeist Studio</h1>
            <p className="text-lg text-gray-600">Step 3: Generate Marketing Campaign</p>
            <div className="mt-2 text-sm text-gray-500">
              <p>Company: {profile.company_name}</p>
              <p>Trend: {selectedTrend.trend_name}</p>
            </div>
          </div>

          {/* Placeholder */}
          <div className="bg-white rounded-lg shadow-lg p-12 text-center">
            <div className="text-6xl mb-4">🎨</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Campaign Generator Coming Soon</h2>
            <p className="text-gray-600 mb-6">
              This is where the 3-agent pipeline will create your complete marketing campaign
              with real-time progress updates.
            </p>
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => router.push('/trends')}
                className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              >
                ← Change Trend
              </button>
              <button
                className="px-6 py-3 bg-gray-300 rounded-lg font-medium text-gray-600 cursor-not-allowed"
                disabled
              >
                Generate Campaign (Coming Soon)
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
