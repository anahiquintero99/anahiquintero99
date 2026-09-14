# Kit web de Annie (React + Tailwind v4 + shadcn)

Componentes de 21st.dev adaptados al sistema rosa de Annie. Cada imagen del perfil de GitHub que viene de aquí
es el componente real corriendo en Chrome y capturado (GitHub no ejecuta React).

| Carpeta | Qué |
|---|---|
| `components/blocks/features-8.tsx` | «Cómo desarrollo · sectores · habilidades» (features-8 de 21st.dev con los datos de Annie) → `assets/features-aq.png` |
| `components/ui/card.tsx` | Card shadcn con borde `#F3B8CE`, cristal y sombra rosa |
| `theme.css` | Tokens Tailwind v4 (`@theme`) en rosa: primary `#E84393`, border `#F3B8CE`, muted `#FFD6EA`, tinta `#2B1A24` |
| `spline/` | Hero con el robot 3D (Spline) → `assets/hero-spline.png` |

## Uso en un proyecto
```bash
npx shadcn@latest init          # crea components/ui y lib/utils.ts (cn)
npm i tailwindcss @tailwindcss/vite lucide-react
```
Copiar `theme.css` al CSS global (`@import "tailwindcss"` + el bloque `@theme`), y los componentes a sus carpetas.
Las fichas de habilidades usan los iconos 3D rosas de `assets/3d/160/` (servirlos desde `public/3d/`).

## Regenerar la imagen
`npm create vite@latest hero -- --template react-ts`, copiar estos archivos, `vite build && vite preview`, y capturar con
Chrome headless a 2x: `--force-device-scale-factor=2 --window-size=1200,760 --screenshot`, recortando el grid.
