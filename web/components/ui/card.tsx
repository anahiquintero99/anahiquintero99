import * as React from 'react'
import { cn } from '@/lib/utils'
const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('rounded-[1.25rem] border border-[#F3B8CE] bg-card text-card-foreground shadow-[0_10px_30px_rgba(216,52,127,.10)] backdrop-blur', className)} {...props} />
))
Card.displayName = 'Card'
const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
))
CardContent.displayName = 'CardContent'
export { Card, CardContent }
