'use client'

import { useState } from 'react'
import { Search, Loader2 } from 'lucide-react'
import VideoCard from './VideoCard'

interface Video {
  title: string
  video_id: string
  channel: string
  description: string
  url: string
}

interface SearchSectionProps {
  maxResults: number
}

export default function SearchSection({ maxResults }: SearchSectionProps) {
  const [query, setQuery] = useState('')
  const [videos, setVideos] = useState<Video[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSearch = async () => {
    if (!query.trim()) return

    setIsLoading(true)
    setError('')

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query.trim(),
          maxResults,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to search videos')
      }

      setVideos(data.videos || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setVideos([])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <section id="search-section" className="pt-20 pb-12">
      <div className="max-w-7xl mx-auto px-4">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="text-6xl mb-4">🎓</div>
          <h1 className="text-4xl md:text-5xl font-bold text-primary-500 mb-6">
            Video Learning Hub
          </h1>
          <p className="text-xl text-white/80 max-w-2xl mx-auto">
            Discover and learn from the best educational content on YouTube
          </p>
        </div>

        {/* Search Form */}
        <div className="max-w-4xl mx-auto mb-12">
          <div className="flex gap-4">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter any topic, question, or skill you want to learn..."
              className="input-field flex-1"
            />
            <button
              onClick={handleSearch}
              disabled={isLoading || !query.trim()}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed min-w-[120px]"
            >
              {isLoading ? (
                <Loader2 className="animate-spin" size={20} />
              ) : (
                <>
                  <Search size={20} />
                  Explore
                </>
              )}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="max-w-4xl mx-auto mb-8 p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400">
            {error}
          </div>
        )}

        {/* Search Results */}
        {videos.length > 0 && (
          <div className="max-w-7xl mx-auto">
            <h2 className="section-header">
              📺 Learning Resources ({videos.length} videos)
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {videos.map((video, index) => (
                <VideoCard key={index} video={video} />
              ))}
            </div>
          </div>
        )}

        {/* No Results */}
        {!isLoading && videos.length === 0 && query && !error && (
          <div className="text-center py-12">
            <p className="text-white/60 text-lg">
              No videos found for "{query}". Try different keywords.
            </p>
          </div>
        )}
      </div>
    </section>
  )
} 