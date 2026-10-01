'use client'

import { Sparkles, FileImage, Copy, CloudUpload } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'

export function Roadmap() {
  const { t } = useLanguage()

  const statusStyles = {
    inDev: 'border-[#3B82F6]/40 bg-[#3B82F6]/10 text-[#5B8DEF]',
    planned: 'border-amber-500/30 bg-amber-500/10 text-amber-300',
    considering: 'border-slate-600/40 bg-slate-500/10 text-slate-300',
  }

  const roadmap = [
    {
      version: 'v1.1',
      status: t.roadmap.statusInDev,
      statusStyle: statusStyles.inDev,
      icon: Sparkles,
      title: t.roadmap.item1Title,
      description: t.roadmap.item1Desc,
    },
    {
      version: 'v1.2',
      status: t.roadmap.statusPlanned,
      statusStyle: statusStyles.planned,
      icon: FileImage,
      title: t.roadmap.item2Title,
      description: t.roadmap.item2Desc,
    },
    {
      version: 'v1.3',
      status: t.roadmap.statusPlanned,
      statusStyle: statusStyles.planned,
      icon: Copy,
      title: t.roadmap.item3Title,
      description: t.roadmap.item3Desc,
    },
    {
      version: 'v2.0',
      status: t.roadmap.statusConsidering,
      statusStyle: statusStyles.considering,
      icon: CloudUpload,
      title: t.roadmap.item4Title,
      description: t.roadmap.item4Desc,
    },
  ]

  return (
    <section id="roadmap" className="scroll-mt-20 px-4 py-20 sm:px-6">
      <div className="mx-auto max-w-6xl">
        <div className="mx-auto max-w-2xl text-center">
          <span className="text-sm font-semibold uppercase tracking-wide text-[#5B8DEF]">
            {t.roadmap.eyebrow}
          </span>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            {t.roadmap.title}
          </h2>
          <p className="mt-3 text-slate-400">{t.roadmap.subtitle}</p>
        </div>

        <div className="mt-12 grid gap-6 sm:grid-cols-2">
          {roadmap.map(
            ({ version, status, statusStyle, icon: Icon, title, description }) => (
              <article
                key={version}
                className="group rounded-xl border border-[#1E293B] bg-[#0F172A] p-6 transition-all hover:-translate-y-1 hover:border-[#3B82F6]/40 hover:shadow-xl hover:shadow-[#3B82F6]/5"
              >
                <div className="flex items-center justify-between">
                  <div className="flex h-11 w-11 items-center justify-center rounded-lg border border-[#1E293B] bg-[#090D16] text-[#5B8DEF] transition-colors group-hover:border-[#3B82F6]/40">
                    <Icon className="h-5 w-5" />
                  </div>
                  <span
                    className={`rounded-full border px-3 py-1 text-xs font-medium ${statusStyle}`}
                  >
                    {status}
                  </span>
                </div>

                <div className="mt-5 flex items-center gap-2">
                  <span className="rounded-md bg-[#090D16] px-2 py-0.5 font-mono text-xs font-semibold text-slate-300">
                    {version}
                  </span>
                </div>
                <h3 className="mt-2 text-lg font-semibold text-white">{title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-400">
                  {description}
                </p>
              </article>
            ),
          )}
        </div>
      </div>
    </section>
  )
}
