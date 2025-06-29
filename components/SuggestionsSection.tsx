'use client'

interface SuggestionsSectionProps {
  onSuggestionClick: (suggestion: string) => void
}

export default function SuggestionsSection({ onSuggestionClick }: SuggestionsSectionProps) {
  const suggestions = {
    'Science & Math': ['Quantum Physics', 'Calculus Basics', 'Chemistry Lab'],
    'Technology': ['Python Programming', 'Web Development', 'AI & Machine Learning'],
    'General Education': ['World History', 'Literature', 'Study Skills']
  }

  return (
    <section className="py-12">
      <div className="max-w-7xl mx-auto px-4">
        <div className="card p-8">
          <h3 className="text-2xl font-bold text-primary-500 mb-6 text-center">
            Popular Topics
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {Object.entries(suggestions).map(([category, topics]) => (
              <div key={category}>
                <h4 className="text-lg font-semibold text-primary-400 mb-4">
                  {category}
                </h4>
                <div className="space-y-3">
                  {topics.map((topic) => (
                    <button
                      key={topic}
                      onClick={() => onSuggestionClick(topic)}
                      className="w-full text-left px-4 py-3 bg-primary-500/10 hover:bg-primary-500/20 text-white border border-primary-500/20 hover:border-primary-500/40 rounded-xl transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-primary-500/20"
                    >
                      {topic}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
} 