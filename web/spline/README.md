# Annie Hero · Spline 3D (kit listo para pegar en un proyecto React)

Un README de GitHub no ejecuta React ni WebGL, así que la escena 3D vive aquí como componente
para el sitio (`anahiquinterog.netlify.app`) o cualquier app Next.js/Vite con shadcn + Tailwind + TypeScript.

## Instalación

```bash
# Si el proyecto aún no tiene shadcn/Tailwind/TS:
npx shadcn@latest init            # crea components.json, lib/utils.ts (cn) y la carpeta components/ui
npm i @splinetool/runtime @splinetool/react-spline framer-motion
```

`components/ui` importa: shadcn resuelve `@/components/ui/*` y sus CLI (`npx shadcn add card`) escriben ahí;
si la carpeta no existe, los imports de `demo.tsx` fallan.

Copiar:

| Archivo de este kit | Destino |
|---|---|
| `splite.tsx` | `components/ui/splite.tsx` |
| `spotlight.tsx` | `components/ui/spotlight.tsx` |
| `card.tsx` | `components/ui/card.tsx` (o `npx shadcn add card`) |
| `annie-hero.tsx` | `components/annie-hero.tsx` → úsalo en la página de inicio |

## Cómo se hizo la imagen del perfil

`assets/hero-spline.png` es este mismo componente corriendo en Chrome (Vite + React), capturado a 1568×653: el robot real de la escena de 21st.dev con tinte rosa por CSS (`filter: sepia hue-rotate saturate` + capas `mix-blend-mode: screen / soft-light`), tarjeta `#2B0F20`, banda metálica y spotlight rosa. Para regenerarla: `npm create vite@latest hero -- --template react-ts`, copiar estos archivos, `npm i @splinetool/react-spline @splinetool/runtime framer-motion`, `vite build && vite preview`, abrir en Chrome (con GPU; headless sin GPU deja la cabeza negra) y capturar.

## El robot rosa

La escena `https://prod.spline.design/kZDDjO5HuC9GJUM2/scene.splinecode` trae el robot en su color original;
los materiales están horneados en el archivo y no se cambian desde React. Para tenerlo rosa:

1. Abrir la escena en Spline (community → *Remix*), seleccionar el robot → *Material* → color base `#F3B8D2`,
   metallic 1.0, roughness 0.15, y una luz de ambiente `#FFD9EA`.
2. *Export → Code → React* → copiar la nueva URL `…/scene.splinecode`.
3. Pegarla en `annie-hero.tsx` (`SCENE_URL`).

Mientras tanto, `annie-hero.tsx` aplica un tinte rosa por CSS (`mix-blend-mode` + gradiente metálico encima),
que ya lo acerca mucho al look del tablero.
