type LimitationsCardProps = {
  limitations: string[];
};

export function LimitationsCard({ limitations }: LimitationsCardProps) {
  if (!limitations.length) return null;

  return (
    <div className="glass-card rounded-[24px] p-5 sm:p-6">
      <div className="mb-4">
        <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
          Limitations
        </div>
        <div className="mt-1 text-sm font-medium text-white">
          Things to keep in mind
        </div>
      </div>

      <div className="space-y-3">
        {limitations.map((limitation, index) => (
          <div
            key={`${index}-${limitation}`}
            className="rounded-2xl border border-amber-300/10 bg-amber-300/8 p-4"
          >
            <div className="flex items-start gap-3">
              <div className="mt-0.5 rounded-full border border-amber-300/20 bg-amber-300/10 px-2 py-0.5 text-[11px] font-semibold uppercase tracking-[0.14em] text-amber-200">
                Note
              </div>

              <div className="text-sm leading-6 text-slate-200">
                {limitation}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}