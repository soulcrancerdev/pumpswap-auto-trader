import { ReactNode } from 'react'

/**
 * Main Layout Component
 * Provides consistent structure across pages
 * Typically includes navigation, header, footer
 */
interface LayoutProps {
  children: ReactNode
}

function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 border-b border-gray-700">
        <nav className="container mx-auto px-4 py-4">
          <h1 className="text-xl font-bold">PumpSwap Auto Trader</h1>
        </nav>
      </header>
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="bg-gray-800 border-t border-gray-700 mt-auto">
        <div className="container mx-auto px-4 py-4 text-center text-gray-400">
          <p>&copy; 2024 PumpSwap Auto Trader</p>
        </div>
      </footer>
    </div>
  )
}

export default Layout

