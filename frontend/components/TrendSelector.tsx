'use client';

import { useState } from 'react';
import { searchTrends, submitManualTrend, Trend } from '@/lib/api';
import { useAppStore } from '@/lib/store';
import { cn } from '@/lib/utils';

type Mode = 'ai' | 'manual';

interface TrendSelectorProps {
  onTrendSelected?: () => void;
}

export default function TrendSelector({ onTrendSelected }: TrendSelectorProps) {
  const profile = useAppStore((state) => state.profile);
  const setSelectedTrend = useAppStore((state) => state.setSelectedTrend);

  const [mode, setMode] = useState<Mode>('ai');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [trends, setTrends] = useState<Trend[]>([]);
  const [manualTopic, setManualTopic] = useState('');
  const [searchContext, setSearchContext] = useState<string>('');

  // AI Trend Search
  const handleAISearch = async () => {
    if (!profile) {
      setError('Profile not found. Please create a profile first.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setTrends([]);

    try {
      const response = await searchTrends(profile);
      setTrends(response.trends);
      setSearchContext(response.search_context);
    } catch (err: any) {
      console.error('AI trend search error:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to discover trends';

      // Check if it's a configuration error (API keys missing)
      if (err.response?.status === 503) {
        setError('⚠️ API keys not configured. AI trend search requires OPENROUTER_API_KEY and SERPER_API_KEY.');
      } else {
        setError(errorMessage);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Manual Trend Input
  const handleManualSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!manualTopic.trim()) {
      setError('Please enter a topic or trend');
      return;
    }

    if (manualTopic.length < 5) {
      setError('Topic must be at least 5 characters');
      return;
    }

    setIsLoading(true);
    setError(null);
    setTrends([]);

    try {
      const response = await submitManualTrend(manualTopic, profile?.company_description);
      setTrends([response.trend]);
      setSearchContext(response.analysis);
    } catch (err: any) {
      console.error('Manual trend submission error:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to analyze trend';

      if (err.response?.status === 503) {
        setError('⚠️ API keys not configured. Trend analysis requires OPENROUTER_API_KEY and SERPER_API_KEY.');
      } else {
        setError(errorMessage);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Select a trend
  const handleSelectTrend = (trend: Trend) => {
    setSelectedTrend(trend);
    if (onTrendSelected) {
      onTrendSelected();
    }
  };

  // Get opportunity badge color
  const getOpportunityColor = (window: string) => {
    if (window.includes('Peak')) return 'bg-red-100 text-red-800 border-red-200';
    if (window.includes('Growing')) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    return 'bg-blue-100 text-blue-800 border-blue-200';
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Mode Toggle */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Discover Trends</h2>
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setMode('ai')}
              className={cn(
                'px-4 py-2 rounded-md font-medium transition-colors',
                mode === 'ai'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              )}
            >
              🤖 AI Search
            </button>
            <button
              onClick={() => setMode('manual')}
              className={cn(
                'px-4 py-2 rounded-md font-medium transition-colors',
                mode === 'manual'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              )}
            >
              ✍️ Manual Input
            </button>
          </div>
        </div>

        {/* AI Search Mode */}
        {mode === 'ai' && (
          <div>
            <p className="text-gray-600 mb-4">
              Let the Philosopher agent discover trending topics relevant to{' '}
              <span className="font-semibold">{profile?.company_name}</span>
            </p>
            <button
              onClick={handleAISearch}
              disabled={isLoading}
              className={cn(
                'w-full px-6 py-3 rounded-lg font-medium text-white transition-colors',
                isLoading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'
              )}
            >
              {isLoading ? '🔍 Discovering Trends...' : '🔍 Discover Trends with AI'}
            </button>
          </div>
        )}

        {/* Manual Input Mode */}
        {mode === 'manual' && (
          <form onSubmit={handleManualSubmit}>
            <p className="text-gray-600 mb-4">
              Enter a topic or trend you want to create a campaign around
            </p>
            <input
              type="text"
              value={manualTopic}
              onChange={(e) => setManualTopic(e.target.value)}
              placeholder="e.g., 'AI anxiety', 'quiet quitting', 'cottage core aesthetics'"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg mb-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading}
              className={cn(
                'w-full px-6 py-3 rounded-lg font-medium text-white transition-colors',
                isLoading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'
              )}
            >
              {isLoading ? '🧠 Analyzing...' : '🧠 Analyze Topic'}
            </button>
          </form>
        )}

        {/* Error Display */}
        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">
            {error}
          </div>
        )}

        {/* Search Context */}
        {searchContext && !error && (
          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-blue-900 text-sm">
            {searchContext}
          </div>
        )}
      </div>

      {/* Trends Display */}
      {trends.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-bold text-gray-900">
            {mode === 'ai' ? 'Discovered Trends' : 'Trend Analysis'}
          </h3>

          {trends.map((trend, index) => (
            <div
              key={index}
              className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer border-2 border-transparent hover:border-blue-300"
              onClick={() => handleSelectTrend(trend)}
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-3">
                <h4 className="text-xl font-bold text-gray-900 flex-1">{trend.trend_name}</h4>
                <div className="flex items-center gap-2 ml-4">
                  <span
                    className={cn(
                      'px-3 py-1 rounded-full text-xs font-medium border',
                      getOpportunityColor(trend.opportunity_window)
                    )}
                  >
                    {trend.opportunity_window}
                  </span>
                  <span className="px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                    {trend.relevance_score}/10
                  </span>
                </div>
              </div>

              {/* Description */}
              <p className="text-gray-700 mb-3">{trend.description}</p>

              {/* Why It's Hot */}
              <div className="bg-gray-50 rounded-lg p-3 mb-3">
                <p className="text-sm font-semibold text-gray-900 mb-1">🔥 Why It's Hot:</p>
                <p className="text-sm text-gray-700">{trend.why_its_hot}</p>
              </div>

              {/* Target Audience */}
              {trend.target_audience && (
                <div className="flex items-center text-sm text-gray-600">
                  <span className="font-semibold mr-2">🎯 Target Audience:</span>
                  <span>{trend.target_audience}</span>
                </div>
              )}

              {/* Select Button */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleSelectTrend(trend);
                }}
                className="mt-4 w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
              >
                Select This Trend →
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!isLoading && trends.length === 0 && !error && (
        <div className="bg-white rounded-lg shadow-lg p-12 text-center">
          <div className="text-6xl mb-4">
            {mode === 'ai' ? '🔍' : '✍️'}
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">
            {mode === 'ai' ? 'Ready to Discover Trends' : 'Ready for Your Topic'}
          </h3>
          <p className="text-gray-600">
            {mode === 'ai'
              ? 'Click "Discover Trends with AI" to let the Philosopher agent find viral opportunities'
              : 'Enter a topic above to get AI-powered analysis and insights'}
          </p>
        </div>
      )}
    </div>
  );
}
