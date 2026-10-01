'use client'

import { useState } from 'react'
import { Download, Menu, X } from 'lucide-react'
import { Logo } from './logo'
import { useLanguage } from '@/lib/i18n'

function LanguageToggle() {
  const { lang, setLang } = useLanguage()

  return (
    <div
      role="group"
      aria-label="Language"
      className="inline-flex items-center rounded-lg border border-[#1E293B] bg-[#0F172A] p-0.5"
    >
      {(['en', 'es'] as const).map((code) => (
        <button
          key={code}
          type="button"
          onClick={() => setLang(code)}
          aria-pressed={lang === code}
          className={`rounded-md px-2.5 py-1 text-xs font-semibold uppercase transition-colors ${
            lang === code
              ? 'bg-[#3B82F6] text-white'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          {code}
        </button>
      ))}
    </div>
  )
}

export function Navbar() {
  const [open, setOpen] = useState(false)
  const { t } = useLanguage()

  const links = [
    { label: t.nav.download, href: '#download' },
    { label: t.nav.roadmap, href: '#roadmap' },
    { label: t.nav.features, href: '#features' },
    { label: t.nav.contact, href: '#contact' },
  ]

  return (
    <header className="sticky top-0 z-50 border-b border-[#1E293B] bg-[#090D16]/80 backdrop-blur-md">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3.5 sm:px-6">
        <a href="#top" aria-label="PhotoSorter home">
          <Logo />
        </a>

        <div className="hidden items-center gap-8 md:flex">
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-sm font-medium text-slate-300 transition-colors hover:text-white"
            >
              {link.label}
            </a>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <LanguageToggle />

          <a
            href="#download"
            className="hidden items-center gap-2 rounded-lg bg-[#3B82F6] px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-[#3B82F6]/20 transition-all hover:bg-[#5B8DEF] hover:shadow-[#3B82F6]/40 md:inline-flex"
          >
            <Download className="h-4 w-4" />
            {t.nav.downloadCta}
          </a>

          <button
            type="button"
            onClick={() => setOpen((v) => !v)}
            className="inline-flex items-center justify-center rounded-lg border border-[#1E293B] p-2 text-slate-300 md:hidden"
            aria-label={t.nav.toggleMenu}
            aria-expanded={open}
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </nav>

      {open && (
        <div className="border-t border-[#1E293B] bg-[#0F172A] px-4 py-4 md:hidden">
          <div className="flex flex-col gap-1">
            {links.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-2.5 text-sm font-medium text-slate-300 transition-colors hover:bg-[#090D16] hover:text-white"
              >
                {link.label}
              </a>
            ))}
            <a
              href="#download"
              onClick={() => setOpen(false)}
              className="mt-2 inline-flex items-center justify-center gap-2 rounded-lg bg-[#3B82F6] px-4 py-2.5 text-sm font-semibold text-white"
            >
              <Download className="h-4 w-4" />
              {t.nav.downloadFull}
            </a>
          </div>
        </div>
      )}
    </header>
  )
}
