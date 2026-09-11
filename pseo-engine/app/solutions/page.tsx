import React from 'react';
import type { Metadata } from 'next';
import { getAllNiches, getAllServices } from '../../lib/taxonomy';

export const metadata: Metadata = {
  title: 'Enterprise AI & Automation Solutions Matrix | Adorise Digital',
  description: 'Explore autonomous AI agents, programmatic SEO architecture, and cold outbound systems across 10 commercial enterprise sectors.',
  alternates: {
    canonical: 'https://adorisedigital.com/solutions/',
  },
};

export default function SolutionsDirectoryPage() {
  const niches = getAllNiches();
  const services = getAllServices();

  return (
    <div className="max-w-7xl mx-auto px-6 py-16">
      <div className="text-center max-w-3xl mx-auto mb-16">
        <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs font-semibold text-cyan-400 mb-6">
          <span>Enterprise Systems Matrix</span>
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold text-white font-display mb-6">
          Autonomous AI & Software Solutions by Industry
        </h1>
        <p className="text-slate-400 text-lg leading-relaxed">
          Select your industry vertical to explore tailored AI agent architectures, programmatic SEO engines, and automated revenue pipelines engineered for your operational bottlenecks.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {niches.map((niche) => (
          <div key={niche.id} className="p-8 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-cyan-500/40 transition flex flex-col justify-between">
            <div>
              <div className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2">Vertical Sector</div>
              <h2 className="text-2xl font-bold text-white font-display mb-4">{niche.name}</h2>
              <div className="space-y-2 mb-6">
                <div className="text-xs text-slate-400">Available Engineered Systems:</div>
                <ul className="space-y-1.5">
                  {services.map((svc) => (
                    <li key={svc.id}>
                      <a
                        href={`/solutions/${niche.id}/${svc.id}/`}
                        className="text-sm text-slate-300 hover:text-cyan-400 flex items-center space-x-2 transition"
                      >
                        <span className="text-cyan-500 text-xs">→</span>
                        <span>{svc.short_name}</span>
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-800">
              <a
                href={`/solutions/${niche.id}/`}
                className="text-xs font-bold text-cyan-400 hover:text-cyan-300 transition flex items-center space-x-1"
              >
                <span>View {niche.name} Hub</span>
                <span>→</span>
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
