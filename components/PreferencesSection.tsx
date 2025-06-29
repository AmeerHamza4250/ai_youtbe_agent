'use client'

interface PreferencesSectionProps {
  maxResults: number
  onMaxResultsChange: (value: number) => void
  autoPlay: boolean
  onAutoPlayChange: (value: boolean) => void
  showDescriptions: boolean
  onShowDescriptionsChange: (value: boolean) => void
}

export default function PreferencesSection({
  maxResults,
  onMaxResultsChange,
  autoPlay,
  onAutoPlayChange,
  showDescriptions,
  onShowDescriptionsChange
}: PreferencesSectionProps) {
  return (
    <section id="preferences-section" className="py-12">
      <div className="max-w-4xl mx-auto px-4">
        <div className="card p-8">
          <h3 className="text-2xl font-bold text-primary-500 mb-8 text-center">
            Search Preferences
          </h3>
          
          <div className="space-y-8">
            {/* Number of Results */}
            <div className="space-y-4">
              <label className="block text-lg font-semibold text-primary-400">
                Number of Results: {maxResults}
              </label>
              <input
                type="range"
                min="2"
                max="8"
                value={maxResults}
                onChange={(e) => onMaxResultsChange(parseInt(e.target.value))}
                className="w-full h-2 bg-dark-700 rounded-lg appearance-none cursor-pointer slider"
              />
              <div className="flex justify-between text-sm text-white/60">
                <span>2</span>
                <span>8</span>
              </div>
            </div>

            {/* Playback Options */}
            <div className="space-y-4">
              <h4 className="text-lg font-semibold text-primary-400">
                Playback Options
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <label className="flex items-center space-x-3 cursor-pointer p-4 bg-primary-500/10 hover:bg-primary-500/20 border border-primary-500/20 hover:border-primary-500/40 rounded-xl transition-all duration-300">
                  <input
                    type="checkbox"
                    checked={autoPlay}
                    onChange={(e) => onAutoPlayChange(e.target.checked)}
                    className="w-5 h-5 text-primary-500 bg-dark-800 border-primary-500/30 rounded focus:ring-primary-500 focus:ring-2"
                  />
                  <span className="text-white font-medium">Enable Autoplay</span>
                </label>
                
                <label className="flex items-center space-x-3 cursor-pointer p-4 bg-primary-500/10 hover:bg-primary-500/20 border border-primary-500/20 hover:border-primary-500/40 rounded-xl transition-all duration-300">
                  <input
                    type="checkbox"
                    checked={showDescriptions}
                    onChange={(e) => onShowDescriptionsChange(e.target.checked)}
                    className="w-5 h-5 text-primary-500 bg-dark-800 border-primary-500/30 rounded focus:ring-primary-500 focus:ring-2"
                  />
                  <span className="text-white font-medium">Show Full Descriptions</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
} 