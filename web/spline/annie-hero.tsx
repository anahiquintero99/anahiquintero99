import { SplineScene } from '@/components/ui/splite'
import { Card } from '@/components/ui/card'
import { Spotlight } from '@/components/ui/spotlight'

// Réplica fiel del demo de 21st.dev (SplineSceneBasic), con la paleta rosa de Annie.
export function AnnieHero() {
  return (
    <Card className="w-full h-[500px] relative overflow-hidden" style={{
      background: '#2B0F20',
      borderColor: 'rgba(255,182,217,.25)', borderRadius: 12 }}>
      {/* banda metálica rosa (encima del canvas) */}
      <div style={{ position: 'absolute', inset: 0, zIndex: 15, pointerEvents: 'none', background: 'linear-gradient(115deg, transparent 38%, rgba(255,214,234,.22) 46%, rgba(232,139,190,.35) 50%, rgba(255,214,234,.18) 54%, transparent 62%)' }} />
      
      <div style={{ position: 'absolute', zIndex: 20 }}><Spotlight className="-top-40 left-0 md:left-60 md:-top-20" fill="#FFD6EA" /></div>
      <div className="flex h-full">
        <div className="flex-1 p-8 relative flex flex-col justify-center" style={{ padding: 48, zIndex: 30, maxWidth: 600 }}>
          <p style={{ fontFamily: 'SF Mono, Menlo, monospace', fontSize: 11, letterSpacing: 3, color: '#E9A8C9' }}>AQ—001 · AI-NATIVE BUILDER · SCIENCE · MX · 2026</p>
          <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent" style={{
            fontFamily: 'Avenir Next, Futura, Helvetica Neue, Arial, sans-serif', fontWeight: 500, fontSize: 84, letterSpacing: 6, lineHeight: 1, marginTop: 24,
            backgroundImage: 'linear-gradient(180deg,#FFF4F9 0%,#F7C6DC 40%,#FFFFFF 52%,#E894BF 72%,#B8578A 100%)', WebkitBackgroundClip: 'text', color: 'transparent' }}>ANAHÍ</h1>
          <p style={{ fontFamily: 'Avenir Next, Futura, Helvetica Neue, Arial, sans-serif', fontWeight: 300, fontSize: 24, letterSpacing: 12, color: '#FFE3F0', marginTop: 6 }}>QUINTERO</p>
          <p className="mt-4 max-w-lg" style={{ fontFamily: 'Cormorant Garamond, Georgia, serif', fontStyle: 'italic', fontSize: 30, color: '#FFD6EA', marginTop: 22 }}>Building what comes next.</p>
          <p className="mt-4 max-w-lg" style={{ color: '#D9A6C0', fontSize: 15, marginTop: 14, maxWidth: 470, fontFamily: 'Avenir Next, Helvetica Neue, Arial, sans-serif' }}>
            Fundadora, científica y arquitecta de tecnología. Diseño y construyo productos digitales con equipos de agentes de IA —web, mobile y sistemas que mueven dinero— de la idea a producción en días.
          </p>
        </div>
        <div className="flex-1 relative" style={{ width: 600, height: 500 }}>
          <SplineScene scene="https://prod.spline.design/kZDDjO5HuC9GJUM2/scene.splinecode" className="w-full h-full"
            style={{ filter: 'sepia(1) hue-rotate(285deg) saturate(2.6) brightness(1.05)' }} />
          {/* tinte rosa sobre la cabeza negra del robot (screen aclara el negro hacia rosa) */}
          <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', mixBlendMode: 'screen',
            background: 'radial-gradient(ellipse 34% 42% at 46% 40%, rgba(214,90,150,.85), rgba(170,60,120,.45) 45%, transparent 72%)' }} />
          <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', mixBlendMode: 'soft-light',
            background: 'linear-gradient(135deg, rgba(255,255,255,.35), transparent 45%, rgba(255,182,217,.3))' }} />
          {/* funde el borde izquierdo del canvas con la tarjeta */}
          <div style={{ position: 'absolute', top: 0, bottom: 0, left: 0, width: 220, pointerEvents: 'none',
            background: 'linear-gradient(90deg, #2B0F20 0%, rgba(43,15,32,.7) 45%, transparent 100%)' }} />

        </div>
      </div>
    </Card>
  )
}
