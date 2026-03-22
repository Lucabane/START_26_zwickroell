import type { ToolTraceStep } from "@/types/chat";

type ToolTraceCardProps = {
  steps: ToolTraceStep[];
};

export function ToolTraceCard({ steps }: ToolTraceCardProps) {
  if (!steps.length) return null;

  return (
    <div className="rounded-2xl border bg-white p-5 shadow-sm">
      <div className="mb-4 text-sm font-semibold text-slate-900">
        Tool trace
      </div>

      <div className="space-y-3">
        {steps.map((step) => (
          <div key={step.step} className="rounded-xl border bg-slate-50 p-4">
            <div className="flex items-center gap-2">
              <div className="rounded-full bg-slate-900 px-2 py-0.5 text-xs font-semibold text-white">
                {step.step}
              </div>
              <div className="text-sm font-semibold text-slate-900">
                {step.tool}
              </div>
            </div>

            <div className="mt-2 text-sm text-slate-700">{step.purpose}</div>

            <div className="mt-3 grid gap-3 md:grid-cols-2">
              <div>
                <div className="text-xs font-medium uppercase tracking-wide text-slate-500">
                  Input
                </div>
                <div className="mt-1 rounded-lg bg-white p-3 text-xs text-slate-700">
                  {step.inputSummary}
                </div>
              </div>

              <div>
                <div className="text-xs font-medium uppercase tracking-wide text-slate-500">
                  Output
                </div>
                <div className="mt-1 rounded-lg bg-white p-3 text-xs text-slate-700">
                  {step.outputSummary}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}