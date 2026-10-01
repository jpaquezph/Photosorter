'use client'

import { Logo } from './logo'
import { useLanguage } from '@/lib/i18n'

export function Footer() {
  const { t } = useLanguage()

  const footerLinks = [
    { label: t.footer.download, href: '#download' },
    { label: t.footer.roadmap, href: '#roadmap' },
    { label: t.footer.features, href: '#features' },
    { label: t.footer.privacy, href: '#' },
    { label: t.footer.contact, href: '#contact' },
  ]

  return (
    <footer className="border-t border-[#1E293B] bg-[#0B1120] px-4 py-10 sm:px-6">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-6 sm:flex-row">
        <div className="flex flex-col items-center gap-3 sm:items-start">
          <Logo />
          <p className="text-sm text-slate-500">{t.footer.tagline}</p>
        </div>

        <nav className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2">
          {footerLinks.map((link) => (
            <a
              key={link.label}
              href={link.href}
              className="text-sm text-slate-400 transition-colors hover:text-white"
            >
              {link.label}
            </a>
          ))}
        </nav>
      </div>

      <div className="mx-auto mt-8 max-w-6xl border-t border-[#1E293B] pt-6 text-center">
        <p className="text-sm text-slate-500">
          © {new Date().getFullYear()} PhotoSorter. {t.footer.rights}
        </p>
      </div>
    </footer>
  )
}
