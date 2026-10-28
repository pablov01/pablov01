#!/usr/bin/env python3
"""Generated banner (dark/light) — static fallback for the GitHub profile README.
The live SELENE visual system lives in portafolio/. This SVG keeps the same lunar feel."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

BANNER_DARK = """<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="280" viewBox="0 0 1180 280" role="img">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#06b6d4"/><stop offset="50%" stop-color="#22d3ee"/><stop offset="100%" stop-color="#8b5cf6"/></linearGradient>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0A101F"/><stop offset="100%" stop-color="#020208"/></linearGradient>
  <filter id="glow"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="1180" height="280" rx="16" fill="url(#bg)" stroke="#1e293b"/>
<!-- grid -->
<g opacity="0.12" stroke="#22d3ee" stroke-width="0.7">
  <path d="M0 210 H1180 M0 70 H1180 M590 0 V280"/>
  <rect x="80" y="40" width="1020" height="200" rx="12" fill="none"/>
</g>
<!-- orbital motif -->
<g transform="translate(1020,70)">
  <ellipse cx="0" cy="0" rx="58" ry="58" fill="none" stroke="url(#g)" stroke-width="3" opacity="0.9" filter="url(#glow)"/>
  <ellipse cx="0" cy="0" rx="38" ry="18" fill="none" stroke="#22d3ee" stroke-width="1.5" opacity="0.5"/>
  <ellipse cx="0" cy="0" rx="22" ry="22" fill="none" stroke="#8b5cf6" stroke-width="1" opacity="0.35"/>
  <circle cx="18" cy="-28" r="3" fill="#22d3ee"><animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/></circle>
</g>
<!-- text -->
<g font-family="JetBrains Mono, ui-monospace, monospace" fill="#E2E8F0">
  <text x="48" y="54" font-size="13" fill="#22d3ee" letter-spacing="0.18em">pablov01@portfolio — zsh — 118×28</text>
  <text x="48" y="108" font-size="32" font-weight="800">Pablo Villalba <tspan fill="#22d3ee">—</tspan> Backend &amp; DevOps</text>
  <text x="48" y="138" font-size="14" fill="#94a3b8">Laravel · PostgreSQL · Docker · RabbitMQ · TypeScript · Next.js · SELENE</text>
  <text x="48" y="170" font-size="13" fill="#64748b">$ profile.sh --live  <tspan fill="#22d3ee">▌</tspan></text>
  <text x="48" y="205" font-size="12" fill="#475569">Building systems that scale — backend, infra &amp; interface — <tspan fill="#22d3ee">portafolio →</tspan></text>
</g>
<g transform="translate(48,228)">
  <rect x="0" y="0" width="132" height="26" rx="13" fill="none" stroke="#22d3ee" opacity="0.9"/>
  <text x="66" y="17" text-anchor="middle" font-family="ui-sans-serif" font-size="11" fill="#22d3ee" font-weight="700">VIEW PORTFOLIO →</text>
</g>
</svg>
"""
BANNER_LIGHT = BANNER_DARK.replace("#0A101F", "#F8FAFC").replace("#020208","#E2E8F0").replace('stroke="#1e293b"','stroke="#CBD5E1"').replace('fill="#E2E8F0"','fill="#0F172A"').replace('fill="#94a3b8"','fill="#334155"').replace('fill="#64748b"','fill="#64748b"')

ASSETS.mkdir(parents=True, exist_ok=True)
(ASSETS / "banner-dark.svg").write_text(BANNER_DARK)
(ASSETS / "banner-light.svg").write_text(BANNER_LIGHT)
print("wrote banner-dark/light.svg")
