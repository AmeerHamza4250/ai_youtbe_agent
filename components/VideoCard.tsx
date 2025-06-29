'use client'

import Image from 'next/image'
import { ExternalLink, Play } from 'lucide-react'

interface Video {
  title: string
  video_id: string
  channel: string
  description: string
  url: string
}

interface VideoCardProps {
  video: Video
}

export default function VideoCard({ video }: VideoCardProps) {
  const shortDescription = video.description.length > 120 
    ? video.description.substring(0, 120) + '...' 
    : video.description

  const copyEmbedCode = () => {
    const embedCode = `<iframe width="100%" height="315" src="https://www.youtube.com/embed/${video.video_id}" frameborder="0" allowfullscreen></iframe>`
    navigator.clipboard.writeText(embedCode).then(() => {
      alert('Embed code copied to clipboard!')
    }).catch(() => {
      // Fallback for older browsers
      const textArea = document.createElement('textarea')
      textArea.value = embedCode
      document.body.appendChild(textArea)
      textArea.select()
      document.execCommand('copy')
      document.body.removeChild(textArea)
      alert('Embed code copied to clipboard!')
    })
  }

  return (
    <div className="card group hover:scale-105 transition-all duration-300">
      {/* Thumbnail */}
      <div className="relative overflow-hidden rounded-t-2xl">
        <Image
          src={`https://img.youtube.com/vi/${video.video_id}/hqdefault.jpg`}
          alt={video.title}
          width={400}
          height={225}
          className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-300"
          onError={(e) => {
            const target = e.target as HTMLImageElement
            target.src = 'https://via.placeholder.com/400x225/0a192f/00ffcc?text=Video+Thumbnail'
          }}
        />
        <div className="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-colors duration-300" />
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Title */}
        <h3 className="text-lg font-bold text-primary-500 mb-3 line-clamp-2 group-hover:text-primary-400 transition-colors">
          {video.title}
        </h3>

        {/* Channel */}
        <div className="flex items-center gap-2 text-white/80 mb-3">
          <span className="text-sm">📺</span>
          <span className="text-sm font-medium">{video.channel}</span>
        </div>

        {/* Description */}
        <p className="text-white/70 text-sm mb-4 line-clamp-3 leading-relaxed">
          {shortDescription}
        </p>

        {/* Actions */}
        <div className="flex gap-3">
          <a
            href={video.url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary flex-1 flex items-center justify-center gap-2 text-sm"
          >
            <ExternalLink size={16} />
            Watch on YouTube
          </a>
          <button
            onClick={copyEmbedCode}
            className="btn-secondary flex items-center justify-center gap-2 text-sm min-w-[80px]"
          >
            <Play size={16} />
            Embed
          </button>
        </div>
      </div>
    </div>
  )
} 