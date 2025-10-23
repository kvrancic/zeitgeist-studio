'use client';

import { useRouter } from 'next/navigation';
import CompanyProfileForm from '@/components/CompanyProfileForm';

export default function ProfilePage() {
  const router = useRouter();

  const handleSuccess = () => {
    // Navigate to trends page after successful profile creation
    router.push('/trends');
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 py-12">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Zeitgeist Studio</h1>
          <p className="text-lg text-gray-600">Step 1: Set up your company profile</p>
        </div>

        {/* Form */}
        <CompanyProfileForm onSuccess={handleSuccess} />

        {/* Back button */}
        <div className="mt-6 text-center">
          <button
            onClick={() => router.push('/')}
            className="text-blue-600 hover:text-blue-700 font-medium"
          >
            ← Back to Home
          </button>
        </div>
      </div>
    </div>
  );
}
