'use client'

import { FolderTree, Activity, GalleryHorizontalEnd } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'

export function Features() {
  const { t } = useLanguage()

  const features = [
    {
      icon: FolderTree,
      title: t.features.item1Title,
      description: t.features.item1Desc,
    },
    {
      icon: Activity,
      title: t.features.item2Title,
      description: t.features.item2Desc,
    },
    {
      icon: GalleryHorizontalEnd,
      title: t.features.item3Title,
      description: t.features.item3Desc,
    },
  ]

  return (
    <section id="features" className="scroll-mt-20 px-4 py-20 sm:px-6">
      <div className="mx-auto max-w-6xl">
        <div className="mx-auto max-w-2xl text-center">
          <span className="text-sm font-semibold uppercase tracking-wide text-[#5B8DEF]">
            {t.features.eyebrow}
          </span>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            {t.features.title}
          </h2>
          <p className="mt-3 text-slate-400">{t.features.subtitle}</p>
        </div>

        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {features.map(({ icon: Icon, title, description }) => (
            <article
              key={title}
              className="group relative overflow-hidden rounded-xl border border-[#1E293B] bg-[#0F172A] p-7 transition-all hover:-translate-y-1 hover:border-[#3B82F6]/40 hover:shadow-xl hover:shadow-[#3B82F6]/5"
            >
              <div
                aria-hidden="true"
                className="pointer-events-none absolute right-0 top-0 h-24 w-24 -translate-y-1/2 translate-x-1/2 rounded-full bg-[#3B82F6]/10 blur-2xl transition-opacity opacity-0 group-hover:opacity-100"
              />
              <div className="relative">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-[#3B82F6] to-[#5B8DEF] text-white shadow-lg shadow-[#3B82F6]/25">
                  <Icon className="h-6 w-6" />
                </div>
                <h3 className="mt-5 text-lg font-semibold text-white">
                  {title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-400">
                  {description}
                </p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
