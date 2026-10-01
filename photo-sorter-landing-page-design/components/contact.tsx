'use client'

import { useState, type FormEvent, type SVGProps } from 'react'
import { MessageCircle, Mail, Send, CheckCircle2 } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'

function GithubIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden="true"
      {...props}
    >
      <path d="M12 .5C5.37.5 0 5.87 0 12.5c0 5.3 3.44 9.8 8.21 11.39.6.11.82-.26.82-.58v-2.03c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.09-.75.08-.73.08-.73 1.21.09 1.84 1.24 1.84 1.24 1.07 1.84 2.81 1.31 3.5 1 .11-.78.42-1.31.76-1.61-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.13-.3-.54-1.52.11-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 3-.4c1.02 0 2.05.14 3 .4 2.29-1.55 3.3-1.23 3.3-1.23.65 1.66.24 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.62-5.49 5.92.43.37.81 1.1.81 2.22v3.29c0 .32.22.7.83.58A12 12 0 0 0 24 12.5C24 5.87 18.63.5 12 .5Z" />
    </svg>
  )
}

export function Contact() {
  const [submitted, setSubmitted] = useState(false)
  const { t } = useLanguage()

  const supportLinks = [
    {
      icon: GithubIcon,
      label: t.contact.githubLabel,
      detail: t.contact.githubDetail,
      href: '#',
    },
    {
      icon: MessageCircle,
      label: t.contact.discordLabel,
      detail: t.contact.discordDetail,
      href: '#',
    },
    {
      icon: Mail,
      label: t.contact.emailLabel,
      detail: t.contact.emailDetail,
      href: 'mailto:support@photosorter.app',
    },
  ]

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setSubmitted(true)
  }

  return (
    <section id="contact" className="scroll-mt-20 px-4 py-20 sm:px-6">
      <div className="mx-auto max-w-6xl">
        <div className="mx-auto max-w-2xl text-center">
          <span className="text-sm font-semibold uppercase tracking-wide text-[#5B8DEF]">
            {t.contact.eyebrow}
          </span>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            {t.contact.title}
          </h2>
          <p className="mt-3 text-slate-400">{t.contact.subtitle}</p>
        </div>

        <div className="mt-12 grid gap-8 lg:grid-cols-5">
          {/* Form */}
          <div className="lg:col-span-3">
            <div className="rounded-2xl border border-[#1E293B] bg-[#0F172A] p-6 sm:p-8">
              {submitted ? (
                <div className="flex flex-col items-center justify-center py-12 text-center">
                  <CheckCircle2 className="h-12 w-12 text-[#5B8DEF]" />
                  <h3 className="mt-4 text-xl font-semibold text-white">
                    {t.contact.sentTitle}
                  </h3>
                  <p className="mt-2 text-sm text-slate-400">
                    {t.contact.sentDesc}
                  </p>
                  <button
                    type="button"
                    onClick={() => setSubmitted(false)}
                    className="mt-6 rounded-lg border border-[#1E293B] bg-[#090D16] px-4 py-2 text-sm font-medium text-slate-200 transition-colors hover:border-[#3B82F6]/50 hover:text-white"
                  >
                    {t.contact.sendAnother}
                  </button>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-5">
                  <div className="grid gap-5 sm:grid-cols-2">
                    <div>
                      <label
                        htmlFor="name"
                        className="mb-2 block text-sm font-medium text-slate-300"
                      >
                        {t.contact.name}
                      </label>
                      <input
                        id="name"
                        name="name"
                        type="text"
                        required
                        placeholder={t.contact.namePlaceholder}
                        className="w-full rounded-lg border border-[#1E293B] bg-[#090D16] px-3.5 py-2.5 text-sm text-white placeholder:text-slate-500 outline-none transition-colors focus:border-[#3B82F6] focus:ring-2 focus:ring-[#3B82F6]/30"
                      />
                    </div>
                    <div>
                      <label
                        htmlFor="email"
                        className="mb-2 block text-sm font-medium text-slate-300"
                      >
                        {t.contact.email}
                      </label>
                      <input
                        id="email"
                        name="email"
                        type="email"
                        required
                        placeholder={t.contact.emailPlaceholder}
                        className="w-full rounded-lg border border-[#1E293B] bg-[#090D16] px-3.5 py-2.5 text-sm text-white placeholder:text-slate-500 outline-none transition-colors focus:border-[#3B82F6] focus:ring-2 focus:ring-[#3B82F6]/30"
                      />
                    </div>
                  </div>

                  <div>
                    <label
                      htmlFor="subject"
                      className="mb-2 block text-sm font-medium text-slate-300"
                    >
                      {t.contact.subject}
                    </label>
                    <select
                      id="subject"
                      name="subject"
                      className="w-full rounded-lg border border-[#1E293B] bg-[#090D16] px-3.5 py-2.5 text-sm text-white outline-none transition-colors focus:border-[#3B82F6] focus:ring-2 focus:ring-[#3B82F6]/30"
                    >
                      <option>{t.contact.subjectBug}</option>
                      <option>{t.contact.subjectFeature}</option>
                      <option>{t.contact.subjectGeneral}</option>
                    </select>
                  </div>

                  <div>
                    <label
                      htmlFor="message"
                      className="mb-2 block text-sm font-medium text-slate-300"
                    >
                      {t.contact.message}
                    </label>
                    <textarea
                      id="message"
                      name="message"
                      required
                      rows={5}
                      placeholder={t.contact.messagePlaceholder}
                      className="w-full resize-none rounded-lg border border-[#1E293B] bg-[#090D16] px-3.5 py-2.5 text-sm text-white placeholder:text-slate-500 outline-none transition-colors focus:border-[#3B82F6] focus:ring-2 focus:ring-[#3B82F6]/30"
                    />
                  </div>

                  <button
                    type="submit"
                    className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-[#3B82F6] px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-[#3B82F6]/20 transition-all hover:bg-[#5B8DEF] hover:shadow-[#3B82F6]/40 sm:w-auto"
                  >
                    <Send className="h-4 w-4" />
                    {t.contact.sendMessage}
                  </button>
                </form>
              )}
            </div>
          </div>

          {/* Support links */}
          <div className="lg:col-span-2">
            <div className="flex h-full flex-col gap-4">
              {supportLinks.map(({ icon: Icon, label, detail, href }) => (
                <a
                  key={label}
                  href={href}
                  className="group flex items-center gap-4 rounded-xl border border-[#1E293B] bg-[#0F172A] p-5 transition-all hover:-translate-y-0.5 hover:border-[#3B82F6]/40"
                >
                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border border-[#1E293B] bg-[#090D16] text-[#5B8DEF] transition-colors group-hover:border-[#3B82F6]/40">
                    <Icon className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="font-semibold text-white">{label}</p>
                    <p className="text-sm text-slate-400">{detail}</p>
                  </div>
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
