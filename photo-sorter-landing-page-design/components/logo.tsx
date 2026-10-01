import Image from 'next/image'

export function Logo({ className = '' }: { className?: string }) {
  return (
    <div className={`flex items-center gap-2.5 ${className}`}>
      <div className="relative h-9 w-9 overflow-hidden rounded-lg ring-1 ring-[#1E293B]">
        <Image
          src="/photosorter-icon.png"
          alt="PhotoSorter logo"
          fill
          className="object-cover"
          sizes="36px"
        />
      </div>
      <span className="text-lg font-semibold tracking-tight text-white">
        Photo<span className="text-[#5B8DEF]">Sorter</span>
      </span>
    </div>
  )
}
