type NextStepsCardProps = {
  nextSteps: string[];
  onSelectStep?: (step: string) => void;
};

export function NextStepsCard({
  nextSteps,
  onSelectStep,
}: NextStepsCardProps) {
  if (!nextSteps.length) return null;

  return (
    <div className="glass-card rounded-[24px] p-5 sm:p-6">
      <div className="mb-4">
        <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
          Next steps
        </div>
        <div className="mt-1 text-sm font-medium text-white">
          Suggested follow-up questions
        </div>
      </div>

      <div className="flex flex-wrap gap-2.5">
        {nextSteps.map((step) => (
          <button
            key={step}
            type="button"
            onClick={() => onSelectStep?.(step)}
            className="rounded-full border border-sky-400/20 bg-sky-400/10 px-4 py-2 text-sm text-sky-100 transition hover:border-sky-300/30 hover:bg-sky-400/16"
          >
            {step}
          </button>
        ))}
      </div>
    </div>
  );
}