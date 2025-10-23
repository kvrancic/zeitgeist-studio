'use client';

import { useRouter } from 'next/navigation';
import { useAppStore } from '@/lib/store';
import { useEffect } from 'react';
import TrendSelector from '@/components/TrendSelector';

export default function TrendsPage() {
  const router = useRouter();
  const profile = useAppStore((state) => state.profile);
  const selectedTrend = useAppStore((state) => state.selectedTrend);

  useEffect(() => {
    // Redirect to profile if not set
    if (!profile) {
      router.push('/profile');
    }
  }, [profile, router]);

  if (!profile) {
    return null; // Will redirect
  }

  const handleTrendSelected = () => {
    // Navigate to campaign generation after a brief delay
    setTimeout(() => {
      router.push('/campaign');
    }, 500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 py-12">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Zeitgeist Studio</h1>
          <p className="text-lg text-gray-600">Step 2: Discover Trending Topics</p>
          <p className="text-sm text-gray-500 mt-2">Company: {profile.company_name}</p>
        </div>

        {/* Trend Selector */}
        <TrendSelector onTrendSelected={handleTrendSelected} />

        {/* Navigation */}
        <div className="mt-8 flex gap-4 justify-center">
          <button
            onClick={() => router.push('/profile')}
            className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 transition-colors"
          >
            ← Edit Profile
          </button>
          {selectedTrend && (
            <button
              onClick={() => router.push('/campaign')}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
            >
              Next: Generate Campaign →
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
