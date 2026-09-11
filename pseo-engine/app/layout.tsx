import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  metadataBase: new URL('https://adorisedigital.com'),
  title: 'Adorise Digital | Autonomous AI Systems & Programmatic Inbound Architecture',
  description: 'Enterprise AI agents, programmatic SEO engines, and full-stack software architectures for high-growth digital businesses.',
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-slate-950 text-slate-100 font-sans antialiased selection:bg-cyan-500 selection:text-slate-950">
        {/* Navigation Header */}
        <header className="sticky top-0 z-50 backdrop-blur-md bg-slate-950/80 border-b border-slate-800/60">
          <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <a href="/" className="flex items-center space-x-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-purple-600 p-0.5 shadow-lg shadow-cyan-500/20 group-hover:shadow-cyan-500/40 transition">
                <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                  <span className="font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 text-xl">A</span>
                </div>
              </div>
              <span className="font-extrabold text-xl tracking-tight text-white font-display">
                ADORISE <span className="text-cyan-400 font-light">DIGITAL</span>
              </span>
            </a>

            <nav className="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-300">
              <a href="/solutions/" className="text-cyan-400 hover:text-cyan-300 transition">Solutions</a>
              <a href="/services/" className="hover:text-cyan-400 transition">Storefront</a>
              <a href="https://inboxcalm.adorisedigital.com" className="hover:text-cyan-400 transition">InboxCalm</a>
              <a href="https://clipcalm.adorisedigital.com" className="hover:text-cyan-400 transition">ClipCalm</a>
              <a href="https://whop.com/adorise-digital-usa/" target="_blank" rel="noopener noreferrer" className="hover:text-cyan-400 transition">Whop Store</a>
            </nav>

            <div className="flex items-center space-x-4">
              <a
                href="https://api.leadconnectorhq.com/widget/booking/adorise-digital-consult"
                target="_blank"
                rel="noopener noreferrer"
                className="px-5 py-2.5 rounded-full text-sm font-semibold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 hover:scale-[1.02] transition"
              >
                Book Architecture Call
              </a>
            </div>
          </div>
        </header>

        <main className="min-h-screen">
          {children}
        </main>

        {/* Footer */}
        <footer className="border-t border-slate-800/80 bg-slate-950 py-16 text-slate-400 text-sm">
          <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-10">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <span className="font-extrabold text-lg text-white font-display">ADORISE DIGITAL</span>
              </div>
              <p className="text-slate-400 text-sm leading-relaxed mb-4">
                Level 4 Autonomous AI Engineering & Programmatic Inbound Architecture. Delivering enterprise software reliability at edge speed.
              </p>
              <p className="text-xs text-slate-400">© 2026 Adorise Digital. All rights reserved.</p>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4 font-display">Solutions</h4>
              <ul className="space-y-2">
                <li><a href="/solutions/b2b-saas/pseo-engine/" className="hover:text-cyan-400 transition">B2B SaaS pSEO</a></li>
                <li><a href="/solutions/ecommerce-d2c/ai-agents/" className="hover:text-cyan-400 transition">E-Commerce AI Support</a></li>
                <li><a href="/solutions/fintech/outbound-infrastructure/" className="hover:text-cyan-400 transition">FinTech Outbound</a></li>
                <li><a href="/solutions/proptech-realestate/ai-agents/" className="hover:text-cyan-400 transition">PropTech Voice Agents</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4 font-display">Products & Tools</h4>
              <ul className="space-y-2">
                <li><a href="https://inboxcalm.adorisedigital.com" className="hover:text-cyan-400 transition">InboxCalm Anti-Toxicity</a></li>
                <li><a href="https://clipcalm.adorisedigital.com" className="hover:text-cyan-400 transition">ClipCalm Video Clipping</a></li>
                <li><a href="https://whop.com/adorise-digital-usa/" className="hover:text-cyan-400 transition">Whop Digital Catalog</a></li>
                <li><a href="/services/" className="hover:text-cyan-400 transition">Managed Services Storefront</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4 font-display">Direct Engagement</h4>
              <p className="text-xs text-slate-400 mb-3">Enterprise SLA agreements and custom multi-agent architecture reviews.</p>
              <a
                href="https://api.leadconnectorhq.com/widget/booking/adorise-digital-consult"
                className="inline-block px-4 py-2 rounded-lg bg-slate-900 border border-slate-700 text-cyan-400 text-xs font-semibold hover:border-cyan-500 transition"
              >
                Schedule Engineering Review →
              </a>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
