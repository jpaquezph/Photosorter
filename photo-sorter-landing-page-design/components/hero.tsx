'use client'

import Image from 'next/image'
import { Download, Play, ShieldCheck, Zap, Lock } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'

export function Hero() {
  const { t } = useLanguage()

  const badges = [
    { icon: ShieldCheck, label: t.hero.badgeFree },
    { icon: Zap, label: t.hero.badgeFast },
    { icon: Lock, label: t.hero.badgePrivacy },
  ]

  return (
    <section id="top" className="relative overflow-hidden">
      {/* Ambient glow */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute left-1/2 top-[-10%] h-[500px] w-[900px] -translate-x-1/2 rounded-full bg-[#3B82F6]/20 blur-[140px]"
      />
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,#090D16_75%)]"
      />

      <div className="relative mx-auto max-w-6xl px-4 pb-20 pt-16 sm:px-6 sm:pt-24">
        <div className="mx-auto max-w-3xl text-center">
          <span className="inline-flex items-center gap-2 rounded-full border border-[#1E293B] bg-[#0F172A] px-3.5 py-1.5 text-xs font-medium text-slate-300">
            <span className="h-1.5 w-1.5 rounded-full bg-[#5B8DEF]" />
            {t.hero.badge}
          </span>

          <h1 className="mt-6 text-balance text-4xl font-bold leading-tight tracking-tight text-white sm:text-5xl md:text-6xl">
            {t.hero.headingBefore}{' '}
            <span className="bg-gradient-to-r from-[#5B8DEF] to-[#3B82F6] bg-clip-text text-transparent">
              {t.hero.headingHighlight}
            </span>
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-pretty text-lg leading-relaxed text-slate-400">
            {t.hero.subheading}
          </p>

          <div className="mt-9 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <a
              href="#download"
              className="group inline-flex w-full items-center justify-center gap-3 rounded-xl bg-[#3B82F6] px-6 py-4 text-base font-semibold text-white shadow-xl shadow-[#3B82F6]/25 transition-all hover:-translate-y-0.5 hover:bg-[#5B8DEF] hover:shadow-[#3B82F6]/40 sm:w-auto"
            >
              <Download className="h-5 w-5 transition-transform group-hover:translate-y-0.5" />
              <span className="flex flex-col items-start leading-none">
                {t.hero.downloadCta}
                <span className="mt-1 text-xs font-normal text-blue-100/80">
                  {t.hero.downloadTag}
                </span>
              </span>
            </a>

            <a
              href="#demo"
              className="inline-flex w-full items-center justify-center gap-2 rounded-xl border border-[#1E293B] bg-[#0F172A] px-6 py-4 text-base font-semibold text-slate-200 transition-all hover:border-[#3B82F6]/50 hover:text-white sm:w-auto"
            >
              <Play className="h-4 w-4 fill-current" />
              {t.hero.watchDemo}
            </a>
          </div>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-x-6 gap-y-3">
            {badges.map(({ icon: Icon, label }) => (
              <div
                key={label}
                className="flex items-center gap-2 text-sm text-slate-400"
              >
                <Icon className="h-4 w-4 text-[#5B8DEF]" />
                {label}
              </div>
            ))}
          </div>
        </div>

        {/* Desktop window mockup */}
        <div id="demo" className="mx-auto mt-16 max-w-5xl scroll-mt-24">
          <div className="overflow-hidden rounded-xl border border-[#1E293B] bg-[#0F172A] shadow-2xl shadow-black/50">
            {/* Window title bar */}
            <div className="flex items-center justify-between border-b border-[#1E293B] bg-[#0B1120] px-4 py-2.5">
              <div className="flex items-center gap-2">
                <span className="h-3 w-3 rounded-full bg-[#ff5f57]" />
                <span className="h-3 w-3 rounded-full bg-[#febc2e]" />
                <span className="h-3 w-3 rounded-full bg-[#28c840]" />
              </div>
              <span className="text-xs font-medium text-slate-400">
                {t.hero.windowTitle}
              </span>
              <span className="w-12" />
            </div>
            <div className="relative aspect-[16/10] w-full bg-[#090D16]">
              <Image
                src="/photosorter-app.png"
                alt={t.hero.appAlt}
                fill
                priority
                className="object-cover object-top"
                sizes="(max-width: 1024px) 100vw, 1024px"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
