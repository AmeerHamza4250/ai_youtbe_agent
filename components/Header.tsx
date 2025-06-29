'use client'

import { useState } from 'react'
import { Search, Settings, Menu, X } from 'lucide-react'

interface HeaderProps {
  onSearchClick: () => void
  onPreferencesClick: () => void
}

export default function Header({ onSearchClick, onPreferencesClick }: HeaderProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  return (
    <>
      {/* Desktop Header */}
      <header className="fixed top-0 left-0 right-0 h-16 bg-gradient-to-r from-background-primary/95 to-background-secondary/95 backdrop-blur-lg border-b-2 border-primary-500/15 shadow-lg z-50">
        <div className="max-w-7xl mx-auto px-4 h-full flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-3 text-primary-500 hover:scale-105 transition-transform duration-300">
            <span className="text-3xl">🎓</span>
            <span className="text-xl font-bold">Video Learning Hub</span>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <button
              onClick={onSearchClick}
              className="flex items-center gap-2 px-4 py-2 bg-primary-500/10 hover:bg-primary-500/20 text-white border border-primary-500/30 hover:border-primary-500 rounded-lg transition-all duration-300 hover:-translate-y-0.5"
            >
              <Search size={18} />
              Search
            </button>
            <button
              onClick={onPreferencesClick}
              className="flex items-center gap-2 px-4 py-2 bg-primary-500/10 hover:bg-primary-500/20 text-white border border-primary-500/30 hover:border-primary-500 rounded-lg transition-all duration-300 hover:-translate-y-0.5"
            >
              <Settings size={18} />
              Preferences
            </button>
          </nav>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden p-2 text-primary-500 hover:bg-primary-500/10 rounded-lg transition-colors"
          >
            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </header>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden fixed top-16 left-0 right-0 bg-background-primary/95 backdrop-blur-lg border-b border-primary-500/15 z-40">
          <div className="px-4 py-4 space-y-3">
            <button
              onClick={() => {
                onSearchClick()
                setIsMobileMenuOpen(false)
              }}
              className="w-full flex items-center gap-2 px-4 py-3 bg-primary-500/10 hover:bg-primary-500/20 text-white border border-primary-500/30 hover:border-primary-500 rounded-lg transition-all duration-300"
            >
              <Search size={18} />
              Search
            </button>
            <button
              onClick={() => {
                onPreferencesClick()
                setIsMobileMenuOpen(false)
              }}
              className="w-full flex items-center gap-2 px-4 py-3 bg-primary-500/10 hover:bg-primary-500/20 text-white border border-primary-500/30 hover:border-primary-500 rounded-lg transition-all duration-300"
            >
              <Settings size={18} />
              Preferences
            </button>
          </div>
        </div>
      )}
    </>
  )
} 