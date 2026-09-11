import React from 'react';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getNicheBySlug, getServiceBySlug, getAllNiches, getAllServices } from '../../../../lib/taxonomy';
import { generatePageData } from '../../../../lib/contentGenerator';

interface PageProps {
  params: {
    niche: string;
    service: string;
  };
}

export async function generateStaticParams() {
  const niches = getAllNiches();
  const services = getAllServices();
  const params: { niche: string; service: string }[] = [];

  // Generate matrix combinations
  for (const n of niches) {
    for (const s of services) {
      params.push({
        niche: n.id,
        service: s.id,
      });
    }
  }

  return params;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const niche = getNicheBySlug(params.niche);
  const service = getServiceBySlug(params.service);

  if (!niche || !service) {
    return {
      title: 'Solution Not Found | Adorise Digital',
    };
  }

  const pageData = generatePageData(service, niche);

  return {
    title: pageData.meta_title,
    description: pageData.meta_description,
    alternates: {
      canonical: pageData.canonical_url,
    },
    openGraph: {
      title: pageData.meta_title,
      description: pageData.meta_description,
      url: pageData.canonical_url,
      siteName: 'Adorise Digital',
      type: 'website',
    },
    twitter: {
      card: 'summary_large_image',
      title: pageData.meta_title,
      description: pageData.meta_description,
    },
  };
}

export default function SolutionPage({ params }: PageProps) {
  const niche = getNicheBySlug(params.niche);
  const service = getServiceBySlug(params.service);

  if (!niche || !service) {
    notFound();
  }

  const data = generatePageData(service, niche);

  return (
    <div className="relative">
      {/* Schema.org Structured Data Injection */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(data.structured_data.service) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(data.structured_data.organization) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(data.structured_data.faq_page) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(data.structured_data.breadcrumb_list) }}
      />

      {/* Breadcrumb Bar */}
      <nav aria-label="Breadcrumb" className="max-w-7xl mx-auto px-6 pt-6 text-xs text-slate-400">
        <ol className="flex items-center space-x-2">
          <li><a href="/" className="hover:text-cyan-400 transition">Home</a></li>
          <li><span className="text-slate-600">/</span></li>
          <li><a href="/solutions/" className="hover:text-cyan-400 transition">Solutions</a></li>
          <li><span className="text-slate-600">/</span></li>
          <li><a href={`/solutions/${data.niche.id}/`} className="hover:text-cyan-400 transition">{data.niche.name}</a></li>
          <li><span className="text-slate-600">/</span></li>
          <li className="text-cyan-400 font-medium truncate">{data.service.short_name}</li>
        </ol>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-12 pb-20 overflow-hidden border-b border-slate-800/60">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(6,182,212,0.12),transparent_50%),radial-gradient(circle_at_bottom_left,rgba(99,102,241,0.1),transparent_50%)] pointer-events-none" />
        <div className="max-w-7xl mx-auto px-6 relative z-10 text-center">
          
          <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full bg-slate-900/90 border border-slate-800 text-xs font-semibold text-cyan-400 mb-6 shadow-inner">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
            <span>{data.hero.badge}</span>
          </div>

          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-white max-w-5xl mx-auto mb-6 font-display leading-tight">
            {data.hero.h1}
          </h1>

          <p className="text-lg md:text-xl text-slate-300 max-w-3xl mx-auto font-light leading-relaxed mb-10">
            {data.hero.subheadline}
          </p>

          {/* Primary Action Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <a
              href="https://api.leadconnectorhq.com/widget/booking/adorise-digital-consult"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-xl font-bold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-xl shadow-cyan-500/25 hover:scale-105 hover:shadow-cyan-500/40 transition text-center"
            >
              Schedule Technical Audit
            </a>
            <a
              href={data.whop_cta.url}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-xl font-semibold bg-slate-900 border border-slate-700 text-white hover:border-cyan-400 hover:bg-slate-800 transition text-center"
            >
              {data.whop_cta.ctaText}
            </a>
          </div>

          {/* Trust Metrics Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-5xl mx-auto">
            {data.hero.trust_metrics.map((tm, idx) => (
              <div key={idx} className="p-5 rounded-xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-sm text-left">
                <div className="text-2xl md:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-indigo-400 font-display">
                  {tm.value}
                </div>
                <div className="text-sm font-semibold text-white mt-1">{tm.label}</div>
                <div className="text-xs text-slate-400 mt-0.5">{tm.subtext}</div>
              </div>
            ))}
          </div>

        </div>
      </section>

      {/* Pain Points Section */}
      <section className="py-20 border-b border-slate-800/60 bg-slate-950/40">
        <div className="max-w-7xl mx-auto px-6">
          <div className="max-w-3xl mb-12">
            <div className="text-xs font-bold uppercase tracking-widest text-cyan-400 mb-2">
              {data.pain_points_section.eyebrow}
            </div>
            <h2 className="text-3xl md:text-4xl font-extrabold text-white font-display mb-4">
              {data.pain_points_section.heading}
            </h2>
            <p className="text-slate-300 text-base leading-relaxed">
              {data.pain_points_section.context_prose}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {data.pain_points_section.pain_points.map((pp, idx) => (
              <div key={idx} className="p-6 rounded-2xl bg-slate-900/50 border border-red-950/40 hover:border-red-500/30 transition flex flex-col justify-between">
                <div>
                  <div className="w-8 h-8 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 flex items-center justify-center font-bold text-sm mb-4">
                    0{idx + 1}
                  </div>
                  <h3 className="text-lg font-bold text-white mb-2 font-display">{pp.title}</h3>
                  <p className="text-sm text-slate-300 leading-relaxed mb-4">{pp.description}</p>
                </div>
                <div className="pt-4 border-t border-slate-800/60">
                  <div className="text-xs font-semibold text-red-400/90 uppercase tracking-wider">Business Impact</div>
                  <div className="text-xs text-slate-400 mt-1">{pp.business_impact}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Solution Architecture Section */}
      <section className="py-20 border-b border-slate-800/60">
        <div className="max-w-7xl mx-auto px-6">
          <div className="max-w-3xl mb-12">
            <div className="text-xs font-bold uppercase tracking-widest text-cyan-400 mb-2">
              {data.solution_section.eyebrow}
            </div>
            <h2 className="text-3xl md:text-4xl font-extrabold text-white font-display mb-4">
              {data.solution_section.heading}
            </h2>
            <p className="text-slate-300 text-base leading-relaxed">
              {data.solution_section.architecture_prose}
            </p>
          </div>

          {/* Core Capabilities */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16">
            {data.solution_section.core_capabilities.map((cap, idx) => (
              <div key={idx} className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 hover:border-cyan-500/40 transition">
                <div className="flex items-center space-x-3 mb-3">
                  <div className="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center font-bold text-xs">
                    {idx + 1}
                  </div>
                  <h3 className="text-lg font-bold text-white font-display">{cap.title}</h3>
                </div>
                <p className="text-sm text-slate-300 leading-relaxed mb-3">
                  {cap.specification}
                </p>
                <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800/60 text-xs text-cyan-300/90 font-mono">
                  Deliverable: {cap.deliverable_output}
                </div>
              </div>
            ))}
          </div>

          {/* Implementation Workflow */}
          <div className="p-8 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800">
            <div className="text-xs font-bold uppercase tracking-widest text-cyan-400 mb-2">Phased Delivery Model</div>
            <h3 className="text-2xl font-bold text-white font-display mb-8">Production Rollout Milestones</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {data.solution_section.workflow_phases.map((wf, idx) => (
                <div key={idx} className="relative">
                  <div className="text-xs font-bold text-cyan-400 mb-1">{wf.timeframe}</div>
                  <div className="text-base font-bold text-white font-display mb-2">{wf.title}</div>
                  <p className="text-xs text-slate-400 leading-relaxed">{wf.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Mika Whop Catalog Dynamic CTA Integration Banner */}
      <section className="py-16 bg-gradient-to-r from-cyan-950/40 via-slate-900 to-indigo-950/40 border-b border-slate-800/80">
        <div className="max-w-7xl mx-auto px-6">
          <div className="p-8 md:p-10 rounded-3xl bg-slate-900/90 border border-cyan-500/30 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-8">
            <div className="max-w-2xl">
              <div className="inline-block px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-bold uppercase tracking-wider mb-3">
                {data.whop_cta.badge}
              </div>
              <h3 className="text-2xl md:text-3xl font-extrabold text-white font-display mb-2">
                Deploy {data.whop_cta.title} for {data.niche.name}
              </h3>
              <p className="text-sm text-slate-300 leading-relaxed mb-4">
                Target Intent: <span className="text-white font-medium">{data.whop_cta.intentCluster}</span>. Available with instant self-service activation through our verified Whop store.
              </p>
              <div className="flex items-center space-x-3 text-sm text-slate-400">
                <span className="text-cyan-400 font-bold text-xl">{data.whop_cta.price}</span>
                <span>•</span>
                <span>Instant Provisioning</span>
                <span>•</span>
                <span>Cancel Anytime</span>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
              <a
                href={data.whop_cta.url}
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3.5 rounded-xl font-bold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/25 hover:scale-105 transition text-center whitespace-nowrap"
              >
                {data.whop_cta.ctaText}
              </a>
              <a
                href="https://api.leadconnectorhq.com/widget/booking/adorise-digital-consult"
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3.5 rounded-xl font-semibold bg-slate-800 border border-slate-700 text-white hover:bg-slate-700 transition text-center whitespace-nowrap"
              >
                Custom Architecture
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Frequently Asked Questions */}
      <section className="py-20 border-b border-slate-800/60">
        <div className="max-w-4xl mx-auto px-6">
          <div className="text-center mb-12">
            <div className="text-xs font-bold uppercase tracking-widest text-cyan-400 mb-2">Technical Validation</div>
            <h2 className="text-3xl md:text-4xl font-extrabold text-white font-display">
              Frequently Asked Questions
            </h2>
          </div>

          <div className="space-y-4">
            {data.faqs.map((faq, idx) => (
              <div key={idx} className="p-6 rounded-xl bg-slate-900/50 border border-slate-800/80">
                <h3 className="text-lg font-bold text-white mb-2 font-display">{faq.question}</h3>
                <p className="text-sm text-slate-300 leading-relaxed">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final Conversion CTA */}
      <section className="py-20 relative overflow-hidden text-center">
        <div className="max-w-4xl mx-auto px-6 relative z-10">
          <h2 className="text-3xl md:text-5xl font-extrabold text-white font-display mb-6">
            Ready to Build Your {data.service.short_name}?
          </h2>
          <p className="text-base md:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed mb-10">
            Book a 30-minute direct technical session with our systems architecture team. We will review your current technical bottlenecks and deliver a concrete operational deployment plan.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a
              href="https://api.leadconnectorhq.com/widget/booking/adorise-digital-consult"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-xl font-bold bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-xl shadow-cyan-500/30 hover:scale-105 transition"
            >
              Schedule Engineering Call
            </a>
            <a
              href="/solutions/"
              className="w-full sm:w-auto px-8 py-4 rounded-xl font-semibold bg-slate-900 border border-slate-700 text-slate-300 hover:text-white hover:bg-slate-800 transition"
            >
              Explore All Solutions Matrix
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
