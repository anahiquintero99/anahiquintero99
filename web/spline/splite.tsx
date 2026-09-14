import { Suspense, lazy } from 'react'
const Spline = lazy(() => import('@splinetool/react-spline'))
interface SplineSceneProps { scene: string; className?: string; style?: React.CSSProperties }
export function SplineScene({ scene, className, style }: SplineSceneProps) {
  return (
    <Suspense fallback={<div className="w-full h-full flex items-center justify-center"><span className="loader"></span></div>}>
      <Spline scene={scene} className={className} style={style} onLoad={() => { (window as any).__splineLoaded = true }} />
    </Suspense>
  )
}
