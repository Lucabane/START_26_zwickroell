import type { AssistantStat } from "@/types/chat";

type StatsGridProps = {
  stats: AssistantStat[];
};

export function StatsGrid({ stats }: StatsGridProps) {
  if (!stats.length) return null;

  return (
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="glass-card rounded-[22px] p-4 transition hover:border-white/20"
        >
          <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
            {stat.label}
          </div>

          <div className="mt-2 text-2xl font-semibold tracking-tight text-white">
            {stat.value}
          </div>

          {stat.description ? (
            <div className="mt-2 text-xs leading-5 text-slate-400">
              {stat.description}
            </div>
          ) : null}
        </div>
      ))}
    </div>
  );
}