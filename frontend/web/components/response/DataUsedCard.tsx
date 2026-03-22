import type { DataUsed } from "@/types/chat";

type DataUsedCardProps = {
  dataUsed: DataUsed;
};

export function DataUsedCard({ dataUsed }: DataUsedCardProps) {
  return (
    <div className="space-y-4">
      <div className="grid gap-3">
        <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
          <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
            Tests count
          </div>
          <div className="mt-2 text-2xl font-semibold tracking-tight text-white">
            {dataUsed.testsCount}
          </div>
        </div>

        {dataUsed.timeRange ? (
          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
            <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
              Time range
            </div>
            <div className="mt-2 text-sm leading-6 text-slate-200">
              {dataUsed.timeRange.start} → {dataUsed.timeRange.end}
            </div>
          </div>
        ) : null}
      </div>

      {dataUsed.filters.length > 0 ? (
        <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
          <div className="mb-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
            Filters
          </div>

          <div className="flex flex-wrap gap-2">
            {dataUsed.filters.map((filter) => (
              <div
                key={`${filter.key}-${filter.value}`}
                className="rounded-full border border-sky-400/15 bg-sky-400/10 px-3 py-1.5 text-xs text-slate-100"
              >
                <span className="font-semibold text-sky-200">{filter.key}:</span>{" "}
                <span className="text-slate-200">{filter.value}</span>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {dataUsed.parameters.length > 0 ? (
        <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
          <div className="mb-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
            Parameters
          </div>

          <div className="flex flex-wrap gap-2">
            {dataUsed.parameters.map((parameter) => (
              <div
                key={parameter}
                className="rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-xs text-slate-200"
              >
                {parameter}
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {dataUsed.resultTypes.length > 0 ? (
        <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
          <div className="mb-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
            Result types
          </div>

          <div className="flex flex-wrap gap-2">
            {dataUsed.resultTypes.map((resultType) => (
              <div
                key={resultType}
                className="rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-xs text-slate-200"
              >
                {resultType}
              </div>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}