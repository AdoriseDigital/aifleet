import React from 'react';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getNicheBySlug, getAllNiches, getAllServices } from '../../../lib/taxonomy';

interface NichePageProps {
  params: {
    niche: string;
  };
}

export async function generateStaticParams() {
  const niches = getAllNiches();
  return niches.map((n) => ({
    niche: n.id,
  }));
}

export async function generateMetadata({ params }: NichePageProps): Promise<Metadata> {
  const niche = getNicheBySlug(params.niche);
  if (!niche) {
    return { title: 'Industry Not Found | Adorise Digital' };
  }

  return {
    title: `${niche.name} AI & Automation Solutions | Adorise Digital`,
    description: `Deploy custom autonomous AI agents, programmatic SEO systems, and automated revenue engines for ${niche.name}.`,
    alternates: {
      canonical: `https://adorisedigital.com/solutions/${niche.id}/`,
    },
  };
}

export default function NicheHubPage({ params }: NichePageProps) {
  const niche = getNicheBySlug(params.niche);
  if (!niche) {
    notFound();
  }

  const services = getAllServices();

  return (
    <div className="max-w-7xl mx-auto px-6 py-16">
      {/* Breadcrumbs */}
      <nav aria-label="Breadcrumb" className="text-xs text-slate-400 mb-8">
        <ol className="flex items-center space-x-2">
          <li><a href="/" className="hover:text-cyan-400 transition">Home</a></li>
          <li><span className="text-slate-600">/</span></li>
          <li><a href="/solutions/" className="hover:text-cyan-400 transition">Solutions</a></li>
          <li><span className="text-slate-600">/</span></li>
          <li className="text-cyan-400 font-medium">{niche.name}</li>
        </ol>
      </nav>

      <div className="max-w-4xl mb-16">
        <div className="inline-block px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 text-xs font-semibold mb-4 border border-cyan-500/20">
          Industry Solutions Hub
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold text-white font-display mb-6">
          Autonomous Systems Engineered for {niche.name}
        </h1>
        <p className="text-slate-300 text-lg leading-relaxed mb-6">
          High-performance digital architectures designed to solve fundamental operational bottlenecks across {niche.name}. Explore our specialized system implementations below.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {services.map((svc) => (
          <div key={svc.id} className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 hover:border-cyan-500/40 transition flex flex-col justify-between">
            <div>
              <div className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2">Capability</div>
              <h2 className="text-xl font-bold text-white font-display mb-3">{svc.short_name}</h2>
              <p className="text-sm text-slate-400 leading-relaxed mb-6">{svc.description}</p>
            </div>
            <div>
              <a
                href={`/solutions/${niche.id}/${svc.id}/`}
                className="w-full inline-block text-center py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-cyan-600 hover:text-white text-cyan-400 text-xs font-bold transition"
              >
                Explore {svc.short_name} →
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
