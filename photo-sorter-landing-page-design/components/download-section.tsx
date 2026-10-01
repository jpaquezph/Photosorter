'use client'

import { Download, Apple, Monitor, ShieldCheck, Zap, Lock } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'

export function DownloadSection() {
  const { t } = useLanguage()

  const platforms = [
    {
      icon: Monitor,
      os: 'Windows',
      detail: t.download.windowsDetail,
      file: 'PhotoSorter-1.0-setup.exe',
      primary: true,
    },
    {
      icon: Apple,
      os: 'macOS',
      detail: t.download.macDetail,
      file: 'PhotoSorter-1.0.zip',
      primary: false,
    },
  ]

  const specs = [
    { label: t.download.specVersion, value: 'v1.0.0' },
    { label: t.download.specOs, value: t.download.specOsValue },
    { label: t.download.specSize, value: '48 MB' },
    { label: t.download.specUpdated, value: t.download.specUpdatedValue },
    { label: t.download.specReq, value: t.download.specReqValue },
  ]

  const badges = [
    { icon: ShieldCheck, label: t.download.badgeFree },
    { icon: Zap, label: t.download.badgeFast },
    { icon: Lock, label: t.download.badgePrivacy },
  ]

  return (
    <section id="download" className="scroll-mt-20 px-4 py-20 sm:px-6">
      <div className="mx-auto max-w-6xl">
        <div className="relative overflow-hidden rounded-2xl border border-[#1E293B] bg-[#0F172A] p-6 shadow-xl sm:p-10">
          <div
            aria-hidden="true"
            className="pointer-events-none absolute right-[-10%] top-[-30%] h-72 w-72 rounded-full bg-[#3B82F6]/15 blur-[100px]"
          />

          <div className="relative">
            <div className="text-center">
              <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                {t.download.title}
              </h2>
              <p className="mx-auto mt-3 max-w-xl text-slate-400">
                {t.download.subtitle}
              </p>
            </div>

            {/* Badges */}
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              {badges.map(({ icon: Icon, label }) => (
                <span
                  key={label}
                  className="inline-flex items-center gap-2 rounded-full border border-[#1E293B] bg-[#090D16] px-4 py-2 text-sm font-medium text-slate-200"
                >
                  <Icon className="h-4 w-4 text-[#5B8DEF]" />
                  {label}
                </span>
              ))}
            </div>

            <div className="mt-10 grid gap-8 lg:grid-cols-2">
              {/* Platform buttons */}
              <div className="flex flex-col gap-4">
                {platforms.map(({ icon: Icon, os, detail, file, primary }) => (
                  <div
                    key={os}
                    className="flex items-center justify-between gap-4 rounded-xl border border-[#1E293B] bg-[#090D16] p-5 transition-colors hover:border-[#3B82F6]/40"
                  >
                    <div className="flex items-center gap-4">
                      <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg border border-[#1E293B] bg-[#0F172A] text-[#5B8DEF]">
                        <Icon className="h-6 w-6" />
                      </div>
                      <div>
                        <p className="font-semibold text-white">{os}</p>
                        <p className="text-sm text-slate-400">{detail}</p>
                        <p className="mt-0.5 font-mono text-xs text-slate-500">
                          {file}
                        </p>
                      </div>
                    </div>
                    <a
                      href="#"
                      className={`inline-flex shrink-0 items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-semibold transition-all ${
                        primary
                          ? 'bg-[#3B82F6] text-white shadow-lg shadow-[#3B82F6]/20 hover:bg-[#5B8DEF]'
                          : 'border border-[#1E293B] bg-[#0F172A] text-slate-200 hover:border-[#3B82F6]/50 hover:text-white'
                      }`}
                    >
                      <Download className="h-4 w-4" />
                      <span className="hidden sm:inline">
                        {t.download.downloadBtn}
                      </span>
                    </a>
                  </div>
                ))}
              </div>

              {/* Specs table */}
              <div className="overflow-hidden rounded-xl border border-[#1E293B] bg-[#090D16]">
                <div className="border-b border-[#1E293B] px-5 py-3">
                  <h3 className="text-sm font-semibold uppercase tracking-wide text-[#5B8DEF]">
                    {t.download.quickSpecs}
                  </h3>
                </div>
                <dl className="divide-y divide-[#1E293B]">
                  {specs.map(({ label, value }) => (
                    <div
                      key={label}
                      className="flex items-center justify-between gap-4 px-5 py-3.5"
                    >
                      <dt className="text-sm text-slate-400">{label}</dt>
                      <dd className="text-right text-sm font-medium text-white">
                        {value}
                      </dd>
                    </div>
                  ))}
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
