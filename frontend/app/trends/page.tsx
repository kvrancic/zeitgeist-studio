'use client';

import { useRouter } from 'next/navigation';
import { useAppStore } from '@/lib/store';
import { useEffect } from 'react';

export default function TrendsPage() {
  const router = useRouter();
  const profile = useAppStore((state) => state.profile);

  useEffect(() => {
    // Redirect to profile if not set
    if (!profile) {
      router.push('/profile');
    }
  }, [profile, router]);

  if (!profile) {
    return null; // Will redirect
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Trend Discovery</h1>
            <p className="text-lg text-gray-600">Step 2: Find or input trending topics</p>
            <p className="text-sm text-gray-500 mt-2">Company: {profile.company_name}</p>
          </div>

          {/* Placeholder for TrendSelector component */}
          <div className="bg-white rounded-lg shadow-lg p-12 text-center">
            <div className="text-6xl mb-4">🔍</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Trend Selector Coming Soon</h2>
            <p className="text-gray-600 mb-6">
              This is where you'll be able to search for AI-discovered trends or manually input topics.
            </p>
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => router.push('/profile')}
                className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              >
                ← Edit Profile
              </button>
              <button
                className="px-6 py-3 bg-gray-300 rounded-lg font-medium text-gray-600 cursor-not-allowed"
                disabled
              >
                Next: Generate Campaign →
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
