'use client'

import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from 'react'

export type Lang = 'en' | 'es'

export const translations = {
  en: {
    nav: {
      download: 'Download',
      roadmap: 'Roadmap',
      features: 'Features',
      contact: 'Contact',
      downloadCta: 'Download',
      downloadFull: 'Download PhotoSorter',
      toggleMenu: 'Toggle menu',
    },
    hero: {
      badge: 'v1.0 now available for Windows & macOS',
      headingBefore: 'Fast, smart, and automated',
      headingHighlight: 'photo organization',
      subheading:
        'Effortlessly separate, process, and preview your photo library in seconds. A lightning-fast desktop app that keeps everything on your machine.',
      downloadCta: 'Download PhotoSorter',
      downloadTag: 'v1.0 · Windows 64-bit',
      watchDemo: 'Watch Demo',
      badgeFree: '100% Free & Safe',
      badgeFast: 'Fast Processing',
      badgePrivacy: 'Local Privacy',
      windowTitle: 'PhotoSorter — v1.0',
      appAlt:
        'PhotoSorter desktop application showing folder configuration, live processing status, and gallery preview',
    },
    download: {
      title: 'Download PhotoSorter',
      subtitle:
        'Free forever. No account required. Your photos never leave your computer.',
      badgeFree: '100% Free / Safe Download',
      badgeFast: 'Fast Processing',
      badgePrivacy: 'Local Privacy — No Cloud Required',
      windowsDetail: 'Windows 10 / 11 · 64-bit',
      macDetail: 'macOS 12+ · Intel & Apple Silicon',
      downloadBtn: 'Download',
      quickSpecs: 'Quick Specs',
      specVersion: 'Version',
      specOs: 'OS Compatibility',
      specOsValue: 'Windows 10/11, macOS 12+',
      specSize: 'File Size',
      specUpdated: 'Last Updated',
      specUpdatedValue: 'Sep 2026',
      specReq: 'System Requirements',
      specReqValue: '4 GB RAM · 120 MB disk',
    },
    roadmap: {
      eyebrow: 'Roadmap',
      title: "What's coming next",
      subtitle:
        "PhotoSorter is actively developed. Here's a look at the features shipping in upcoming releases.",
      statusInDev: 'In Development',
      statusPlanned: 'Planned',
      statusConsidering: 'Under Consideration',
      item1Title: 'AI Auto-Tagging & Face Recognition',
      item1Desc:
        'Automatically tag photos by content and group them by the people they contain, all processed locally.',
      item2Title: 'RAW Support & EXIF Editor',
      item2Desc:
        'Native RAW format handling plus a built-in metadata and EXIF editor for full control over your library.',
      item3Title: 'Batch Rename & Duplicate Finder',
      item3Desc:
        'Rename thousands of files with smart patterns and reclaim space by finding exact and near-duplicate photos.',
      item4Title: 'Cloud Backup & Sync',
      item4Desc:
        'Optional, opt-in encrypted cloud backup and multi-device sync — while keeping local-first privacy the default.',
    },
    features: {
      eyebrow: 'Features & Workflow',
      title: 'Built for speed and clarity',
      subtitle:
        'Every part of the workflow is designed to move fast while keeping you in full control.',
      item1Title: 'Smart Folder Selection',
      item1Desc:
        'Point PhotoSorter at any folder and let it recursively scan subfolders. Choose exactly what to include before you process a single file.',
      item2Title: 'Live Processing Status',
      item2Desc:
        'Watch real-time progress with counts of photos found, processed, and errors — plus an accurate estimated time remaining.',
      item3Title: 'Instant Preview & Gallery',
      item3Desc:
        'See each photo as it is processed and browse your results in an interactive gallery view with quick navigation.',
    },
    contact: {
      eyebrow: 'Contact & Feedback',
      title: "We'd love to hear from you",
      subtitle:
        'Found a bug or have an idea? Send us a message or reach out through the community.',
      sentTitle: 'Message sent!',
      sentDesc: "Thanks for the feedback — we'll get back to you soon.",
      sendAnother: 'Send another',
      name: 'Name',
      namePlaceholder: 'Jane Doe',
      email: 'Email',
      emailPlaceholder: 'jane@example.com',
      subject: 'Subject',
      subjectBug: 'Bug Report',
      subjectFeature: 'Feature Request',
      subjectGeneral: 'General Inquiry',
      message: 'Message',
      messagePlaceholder: "Tell us what's on your mind...",
      sendMessage: 'Send Message',
      githubLabel: 'GitHub Repository',
      githubDetail: 'Report issues & contribute',
      discordLabel: 'Community Discord',
      discordDetail: 'Join the conversation',
      emailLabel: 'Support Email',
      emailDetail: 'support@photosorter.app',
    },
    footer: {
      tagline: 'Fast, smart, local photo organization.',
      download: 'Download',
      roadmap: 'Roadmap',
      features: 'Features',
      privacy: 'Privacy Policy',
      contact: 'Contact',
      rights: 'All rights reserved.',
    },
  },
  es: {
    nav: {
      download: 'Descargar',
      roadmap: 'Próximamente',
      features: 'Funciones',
      contact: 'Contacto',
      downloadCta: 'Descargar',
      downloadFull: 'Descargar PhotoSorter',
      toggleMenu: 'Abrir menú',
    },
    hero: {
      badge: 'v1.0 ya disponible para Windows y macOS',
      headingBefore: 'Organización de fotos rápida,',
      headingHighlight: 'inteligente y automática',
      subheading:
        'Separa, procesa y previsualiza tu biblioteca de fotos en segundos, sin esfuerzo. Una app de escritorio ultrarrápida que mantiene todo en tu equipo.',
      downloadCta: 'Descargar PhotoSorter',
      downloadTag: 'v1.0 · Windows 64-bit',
      watchDemo: 'Ver Demo',
      badgeFree: '100% Gratis y Seguro',
      badgeFast: 'Procesamiento Rápido',
      badgePrivacy: 'Privacidad Local',
      windowTitle: 'PhotoSorter — v1.0',
      appAlt:
        'Aplicación de escritorio PhotoSorter mostrando la configuración de carpetas, el estado de procesamiento en vivo y la vista previa de la galería',
    },
    download: {
      title: 'Descargar PhotoSorter',
      subtitle:
        'Gratis. Sin cuenta requerida. Tus fotos nunca salen de tu computadora.',
      badgeFree: '100% Gratis / Descarga Segura',
      badgeFast: 'Procesamiento Rápido',
      badgePrivacy: 'Privacidad Local — Sin Nube Requerida',
      windowsDetail: 'Windows 10 / 11 · 64-bit',
      macDetail: 'macOS 12+ · Intel y Apple Silicon',
      downloadBtn: 'Descargar',
      quickSpecs: 'Especificaciones',
      specVersion: 'Versión',
      specOs: 'Compatibilidad',
      specOsValue: 'Windows 10/11, macOS 12+',
      specSize: 'Tamaño del Archivo',
      specUpdated: 'Última Actualización',
      specUpdatedValue: 'Sep 2026',
      specReq: 'Requisitos del Sistema',
      specReqValue: '4 GB RAM · 120 MB disco',
    },
    roadmap: {
      eyebrow: 'Próximamente',
      title: 'Lo que viene',
      subtitle:
        'PhotoSorter está en desarrollo activo. Aquí tienes un vistazo a las funciones que llegarán en las próximas versiones.',
      statusInDev: 'En Desarrollo',
      statusPlanned: 'Planeado',
      statusConsidering: 'En Consideración',
      item1Title: 'Clasificador por fecha, renombrado, mover',
      item1Desc:
        'Etiqueta fotos automáticamente por contenido y agrúpalas según las personas que aparecen, todo procesado localmente.',
      item2Title: 'Ampliación de formatos',
      item2Desc:
        'Aumento de la cantidad de formatos compatibles. Actualmente PhotoSorter procesa 13 formatos de imagen diferentes, 5 estándar y 8 RAW\'s.',
      item3Title: 'Renombrado por Lotes y Buscador de Duplicados',
      item3Desc:
        'Renombra miles de archivos con patrones inteligentes y recupera espacio encontrando fotos duplicadas exactas y similares.',
      item4Title: 'Copia de Seguridad y Sincronización en la Nube',
      item4Desc:
        'Copia de seguridad cifrada opcional y sincronización entre dispositivos, manteniendo la privacidad local como predeterminada.',
    },
    features: {
      eyebrow: 'Funciones y Flujo de Trabajo',
      title: 'Diseñado para velocidad y claridad',
      subtitle:
        'Cada parte del flujo de trabajo está diseñada para ir rápido mientras mantienes el control total.',
      item1Title: 'Selección Inteligente de Carpetas',
      item1Desc:
        'Apunta PhotoSorter a cualquier carpeta y deja que escanee las subcarpetas de forma recursiva. Elige exactamente qué incluir antes de procesar un solo archivo.',
      item2Title: 'Estado de Procesamiento en Vivo',
      item2Desc:
        'Observa el progreso en tiempo real con el conteo de fotos encontradas, procesadas y errores, además de un tiempo restante estimado preciso.',
      item3Title: 'Vista Previa Instantánea y Galería',
      item3Desc:
        'Ve cada foto mientras se procesa y explora tus resultados en una vista de galería interactiva con navegación rápida.',
    },
    contact: {
      eyebrow: 'Contacto y Comentarios',
      title: 'Nos encantaría saber de ti',
      subtitle:
        '¿Encontraste un error o tienes una idea? Envíanos un mensaje o contáctanos a través de la comunidad.',
      sentTitle: '¡Mensaje enviado!',
      sentDesc: 'Gracias por tus comentarios — te responderemos pronto.',
      sendAnother: 'Enviar otro',
      name: 'Nombre',
      namePlaceholder: 'Juan Pérez',
      email: 'Correo',
      emailPlaceholder: 'juan@ejemplo.com',
      subject: 'Asunto',
      subjectBug: 'Reporte de Error',
      subjectFeature: 'Solicitud de Función',
      subjectGeneral: 'Consulta General',
      message: 'Mensaje',
      messagePlaceholder: 'Cuéntanos qué tienes en mente...',
      sendMessage: 'Enviar Mensaje',
      githubLabel: 'Repositorio de GitHub',
      githubDetail: 'Reporta problemas y contribuye',
      discordLabel: 'Comunidad de Discord',
      discordDetail: 'Únete a la conversación',
      emailLabel: 'Correo de Soporte',
      emailDetail: 'support@photosorter.app',
    },
    footer: {
      tagline: 'Organización de fotos rápida, inteligente y local.',
      download: 'Descargar',
      roadmap: 'Próximamente',
      features: 'Funciones',
      privacy: 'Política de Privacidad',
      contact: 'Contacto',
      rights: 'Todos los derechos reservados.',
    },
  },
} as const

type Translation = (typeof translations)['en']

type LanguageContextValue = {
  lang: Lang
  setLang: (lang: Lang) => void
  t: Translation
}

const LanguageContext = createContext<LanguageContextValue | null>(null)

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>('en')

  useEffect(() => {
    const stored = window.localStorage.getItem('photosorter-lang')
    if (stored === 'en' || stored === 'es') {
      setLangState(stored)
    } else if (navigator.language.toLowerCase().startsWith('es')) {
      setLangState('es')
    }
  }, [])

  useEffect(() => {
    document.documentElement.lang = lang
  }, [lang])

  function setLang(next: Lang) {
    setLangState(next)
    window.localStorage.setItem('photosorter-lang', next)
  }

  return (
    <LanguageContext.Provider value={{ lang, setLang, t: translations[lang] }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const ctx = useContext(LanguageContext)
  if (!ctx) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return ctx
}
