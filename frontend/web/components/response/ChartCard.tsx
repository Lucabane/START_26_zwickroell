import type { ReactNode } from "react";

type ChartCardProps = {
  title: string;
  interpretation?: string;
  children: ReactNode;
};

export function ChartCard({
  title,
  interpretation,
  children,
}: ChartCardProps) {
  return (
    <div className="glass-card rounded-[24px] p-5 sm:p-6">
      <div className="mb-4 flex items-start justify-between gap-3">
        <div>
          <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
            Chart
          </div>
          <div className="mt-1 text-base font-semibold text-white">{title}</div>
        </div>
      </div>

      <div className="rounded-[20px] border border-white/10 bg-white p-3 sm:p-4">
        <div className="h-72 w-full rounded-[12px] bg-white">
          {children}
        </div>
      </div>

      {interpretation ? (
        <div className="mt-4 rounded-2xl border border-white/10 bg-white/[0.03] p-4">
          <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
            Interpretation
          </div>
          <div className="mt-2 text-sm leading-6 text-slate-300">
            {interpretation}
          </div>
        </div>
      ) : null}
    </div>
  );
}