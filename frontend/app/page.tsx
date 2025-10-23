export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-gray-900 dark:text-white mb-4">
            🎨 Zeitgeist Studio
          </h1>
          <p className="text-2xl text-gray-600 dark:text-gray-300 mb-8">
            AI Marketing Campaign Generator
          </p>
          <p className="text-lg text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
            Transform trend analysis into complete, ready-to-deploy marketing campaigns
            in minutes, powered by multi-agent AI.
          </p>
        </div>

        {/* Status Section */}
        <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-white">
            Project Status
          </h2>

          <div className="space-y-4">
            <StatusItem status="complete" title="Backend Infrastructure">
              FastAPI server with all endpoints configured
            </StatusItem>
            <StatusItem status="complete" title="AI Agents">
              3 specialized agents (Philosopher, Architect, Optimizer)
            </StatusItem>
            <StatusItem status="complete" title="API Routes">
              Health, Profile, Trends, Campaign, Export endpoints
            </StatusItem>
            <StatusItem status="in-progress" title="Frontend">
              Next.js 14 + TypeScript + TailwindCSS setup complete
            </StatusItem>
            <StatusItem status="pending" title="UI Components">
              Building campaign generation interface
            </StatusItem>
          </div>
        </div>

        {/* Features Grid */}
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <FeatureCard
            icon="👤"
            title="Company Profile"
            description="Upload brand guidelines, define voice, set preferences"
          />
          <FeatureCard
            icon="📈"
            title="AI Trend Discovery"
            description="Philosopher agent analyzes cultural zeitgeist in real-time"
          />
          <FeatureCard
            icon="✍️"
            title="Content Generation"
            description="Multi-agent system creates blog posts, social media, designs"
          />
          <FeatureCard
            icon="📊"
            title="SEO Optimization"
            description="Brutalist Optimizer ensures maximum conversion"
          />
          <FeatureCard
            icon="📄"
            title="Professional Export"
            description="Download campaigns as PDF, Markdown, or complete ZIP"
          />
          <FeatureCard
            icon="⚡"
            title="Real-time Streaming"
            description="Watch agents work in real-time with progress updates"
          />
        </div>

        {/* CTA Section */}
        <div className="max-w-4xl mx-auto mt-16 text-center">
          <button className="bg-primary-600 hover:bg-primary-700 text-white font-bold py-4 px-8 rounded-lg text-lg transition-colors shadow-lg">
            Get Started (Coming Soon)
          </button>
          <p className="mt-4 text-gray-500 dark:text-gray-400">
            Currently in active development. Check back soon!
          </p>
        </div>
      </div>
    </main>
  );
}

function StatusItem({ status, title, children }: {
  status: 'complete' | 'in-progress' | 'pending',
  title: string,
  children: React.ReactNode
}) {
  const statusConfig = {
    complete: { icon: '✅', color: 'text-green-600 dark:text-green-400' },
    'in-progress': { icon: '🔄', color: 'text-blue-600 dark:text-blue-400' },
    pending: { icon: '⏳', color: 'text-gray-500 dark:text-gray-400' },
  };

  const config = statusConfig[status];

  return (
    <div className="flex items-start space-x-3">
      <span className="text-2xl">{config.icon}</span>
      <div className="flex-1">
        <h3 className={`font-semibold ${config.color}`}>{title}</h3>
        <p className="text-gray-600 dark:text-gray-400 text-sm">{children}</p>
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, description }: {
  icon: string,
  title: string,
  description: string
}) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
        {title}
      </h3>
      <p className="text-gray-600 dark:text-gray-400">
        {description}
      </p>
    </div>
  );
}
