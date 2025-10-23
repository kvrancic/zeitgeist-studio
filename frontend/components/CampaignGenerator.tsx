'use client';

import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { generateCampaign, type CampaignRequest } from '@/lib/api';
import { cn } from '@/lib/utils';

interface Agent {
  id: number;
  name: string;
  emoji: string;
  color: string;
  description: string;
}

const AGENTS: Agent[] = [
  {
    id: 1,
    name: 'Zeitgeist Philosopher',
    emoji: '🧙',
    color: 'purple',
    description: 'Analyzing cultural drivers and psychological truths',
  },
  {
    id: 2,
    name: 'Cynical Content Architect',
    emoji: '🎨',
    color: 'blue',
    description: 'Creating viral content and compelling narratives',
  },
  {
    id: 3,
    name: 'Brutalist Optimizer',
    emoji: '⚡',
    color: 'yellow',
    description: 'Optimizing for SEO and conversion metrics',
  },
  {
    id: 4,
    name: 'Final Content Polish',
    emoji: '✨',
    color: 'green',
    description: 'Architect creating final optimized campaign',
  },
];

interface CampaignGeneratorProps {
  request: CampaignRequest;
  onComplete?: (campaign: any) => void;
}

interface ProgressUpdate {
  step?: number;
  agent?: string;
  status: 'started' | 'working' | 'complete' | 'error';
  message: string;
  data?: any;
}

export default function CampaignGenerator({ request, onComplete }: CampaignGeneratorProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState<ProgressUpdate[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [campaign, setCampaign] = useState<any>(null);

  const startGeneration = async () => {
    setIsGenerating(true);
    setError(null);
    setProgress([]);
    setCampaign(null);
    setCurrentStep(0);

    try {
      const eventSource = new EventSource(
        `http://localhost:8000/api/campaign/generate?${new URLSearchParams({
          company_name: request.company_name,
          company_description: request.company_description,
          brand_voice: request.brand_voice,
          trend_name: request.trend_name,
          trend_context: request.trend_context,
          ...(request.extracted_docs && { extracted_docs: request.extracted_docs }),
        })}`
      );

      eventSource.onmessage = (event) => {
        const data: ProgressUpdate = JSON.parse(event.data);

        setProgress((prev) => [...prev, data]);

        if (data.step) {
          setCurrentStep(data.step);
        }

        if (data.status === 'complete' && data.data) {
          setCampaign(data.data);
          setIsGenerating(false);
          eventSource.close();
          if (onComplete) onComplete(data.data);
        }

        if (data.status === 'error') {
          setError(data.message);
          setIsGenerating(false);
          eventSource.close();
        }
      };

      eventSource.onerror = (err) => {
        console.error('SSE Error:', err);
        setError('Connection to server lost. Please try again.');
        setIsGenerating(false);
        eventSource.close();
      };
    } catch (err: any) {
      console.error('Campaign generation error:', err);
      setError(err.message || 'Failed to generate campaign');
      setIsGenerating(false);
    }
  };

  useEffect(() => {
    // Auto-start generation when component mounts
    startGeneration();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const getAgentColor = (colorName: string) => {
    const colors: Record<string, string> = {
      purple: 'bg-purple-100 border-purple-300 text-purple-800',
      blue: 'bg-blue-100 border-blue-300 text-blue-800',
      yellow: 'bg-yellow-100 border-yellow-300 text-yellow-800',
      green: 'bg-green-100 border-green-300 text-green-800',
    };
    return colors[colorName] || colors.blue;
  };

  const parseCampaignOutput = (fullOutput: string) => {
    // Intelligent parsing of campaign output
    const sections: Record<string, string> = {
      narrative: '',
      blog: '',
      social_media: '',
      tshirt_designs: '',
      full: fullOutput,
    };

    // Try to extract sections based on common markers
    const narrativeMatch = fullOutput.match(/## Narrative[\s\S]*?(?=##|$)/i);
    const blogMatch = fullOutput.match(/## Blog[\s\S]*?(?=##|$)/i);
    const socialMatch = fullOutput.match(/## Social Media[\s\S]*?(?=##|$)/i);
    const tshirtMatch = fullOutput.match(/## T-?Shirt[\s\S]*?(?=##|$)/i);

    if (narrativeMatch) sections.narrative = narrativeMatch[0];
    if (blogMatch) sections.blog = blogMatch[0];
    if (socialMatch) sections.social_media = socialMatch[0];
    if (tshirtMatch) sections.tshirt_designs = tshirtMatch[0];

    return sections;
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Agent Pipeline Progress */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          🚀 3-Agent Marketing Pipeline
        </h2>

        <div className="space-y-4">
          {AGENTS.map((agent) => {
            const isActive = currentStep === agent.id;
            const isComplete = currentStep > agent.id;
            const isPending = currentStep < agent.id;

            return (
              <div
                key={agent.id}
                className={cn(
                  'p-4 rounded-lg border-2 transition-all duration-500',
                  isActive && 'border-blue-500 shadow-lg scale-105',
                  isComplete && 'border-green-500 bg-green-50',
                  isPending && 'border-gray-200 bg-gray-50 opacity-60'
                )}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    {/* Agent Emoji/Avatar */}
                    <div
                      className={cn(
                        'w-12 h-12 rounded-full flex items-center justify-center text-2xl border-2 transition-all',
                        isActive && 'animate-pulse shadow-lg',
                        isComplete && 'border-green-500',
                        getAgentColor(agent.color)
                      )}
                    >
                      {agent.emoji}
                    </div>

                    {/* Agent Info */}
                    <div>
                      <h3 className="font-bold text-gray-900">{agent.name}</h3>
                      <p className="text-sm text-gray-600">{agent.description}</p>
                    </div>
                  </div>

                  {/* Status Badge */}
                  <div>
                    {isComplete && (
                      <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                        ✓ Complete
                      </span>
                    )}
                    {isActive && (
                      <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium animate-pulse">
                        ⏳ Working...
                      </span>
                    )}
                    {isPending && (
                      <span className="px-3 py-1 bg-gray-100 text-gray-500 rounded-full text-sm font-medium">
                        ⏸ Pending
                      </span>
                    )}
                  </div>
                </div>

                {/* Progress Bar */}
                {isActive && (
                  <div className="mt-3">
                    <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-blue-500 animate-pulse" style={{ width: '100%' }} />
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Progress Log */}
      {progress.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">📋 Generation Log</h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {progress.map((update, index) => (
              <div
                key={index}
                className={cn(
                  'p-3 rounded-lg text-sm',
                  update.status === 'error' && 'bg-red-50 text-red-800 border border-red-200',
                  update.status === 'complete' && 'bg-green-50 text-green-800 border border-green-200',
                  update.status === 'working' && 'bg-blue-50 text-blue-800 border border-blue-200',
                  update.status === 'started' && 'bg-purple-50 text-purple-800 border border-purple-200'
                )}
              >
                <span className="font-medium">{update.agent || 'System'}:</span> {update.message}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-6">
          <h3 className="text-lg font-bold text-red-900 mb-2">❌ Generation Failed</h3>
          <p className="text-red-800">{error}</p>
          <button
            onClick={startGeneration}
            className="mt-4 px-6 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg transition-colors"
          >
            🔄 Retry
          </button>
        </div>
      )}

      {/* Campaign Results */}
      {campaign && (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-green-50 to-blue-50 border-2 border-green-300 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              🎉 Campaign Generated Successfully!
            </h2>
            <p className="text-gray-700">
              Your complete marketing campaign is ready. Review the content below and download when
              ready.
            </p>
          </div>

          {/* Campaign Content Sections */}
          {(() => {
            const sections = parseCampaignOutput(campaign.full_output || campaign.narrative || '');

            return (
              <>
                {/* Narrative/Overview */}
                {sections.narrative && (
                  <div className="bg-white rounded-lg shadow-lg p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-4">📖 Campaign Narrative</h3>
                    <div className="prose prose-lg max-w-none">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{sections.narrative}</ReactMarkdown>
                    </div>
                  </div>
                )}

                {/* Blog Content */}
                {sections.blog && (
                  <div className="bg-white rounded-lg shadow-lg p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-4">📝 Blog Post</h3>
                    <div className="prose prose-lg max-w-none">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{sections.blog}</ReactMarkdown>
                    </div>
                  </div>
                )}

                {/* Social Media */}
                {sections.social_media && (
                  <div className="bg-white rounded-lg shadow-lg p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-4">📱 Social Media Posts</h3>
                    <div className="prose prose-lg max-w-none">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{sections.social_media}</ReactMarkdown>
                    </div>
                  </div>
                )}

                {/* T-Shirt Designs */}
                {sections.tshirt_designs && (
                  <div className="bg-white rounded-lg shadow-lg p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-4">👕 T-Shirt Designs</h3>
                    <div className="prose prose-lg max-w-none">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{sections.tshirt_designs}</ReactMarkdown>
                    </div>
                  </div>
                )}

                {/* Full Output (Fallback) */}
                {!sections.narrative && !sections.blog && (
                  <div className="bg-white rounded-lg shadow-lg p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-4">📄 Complete Campaign</h3>
                    <div className="prose prose-lg max-w-none">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{sections.full}</ReactMarkdown>
                    </div>
                  </div>
                )}
              </>
            );
          })()}

          {/* Download Actions */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">💾 Download Campaign</h3>
            <div className="flex gap-4">
              <button className="flex-1 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors">
                📄 Download PDF
              </button>
              <button className="flex-1 px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg transition-colors">
                📦 Download ZIP Bundle
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
