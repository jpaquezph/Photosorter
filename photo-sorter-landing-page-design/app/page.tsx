import { Navbar } from '@/components/navbar'
import { Hero } from '@/components/hero'
import { DownloadSection } from '@/components/download-section'
import { Roadmap } from '@/components/roadmap'
import { Features } from '@/components/features'
import { Contact } from '@/components/contact'
import { Footer } from '@/components/footer'

export default function Page() {
  return (
    <div className="min-h-screen bg-[#090D16]">
      <Navbar />
      <main>
        <Hero />
        <DownloadSection />
        <Roadmap />
        <Features />
        <Contact />
      </main>
      <Footer />
    </div>
  )
}
