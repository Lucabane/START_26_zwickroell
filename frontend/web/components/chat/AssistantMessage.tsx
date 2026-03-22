import type { AssistantResponse } from "@/types/chat";
import { ResponseText } from "@/components/response/ResponseText";
import { StatsGrid } from "@/components/response/StatsGrid";
import { DataUsedCard } from "@/components/response/DataUsedCard";
import { LimitationsCard } from "@/components/response/LimitationsCard";
import { NextStepsCard } from "@/components/response/NextStepsCard";
import { ChartCard } from "@/components/response/ChartCard";
import { ChartRenderer } from "@/components/response/ChartRenderer";

type AssistantMessageProps = {
  content: AssistantResponse;
  isLoading?: boolean;
  onSelectStep?: (step: string) => void;
};

export default function AssistantMessage({
  content,
  isLoading = false,
  onSelectStep,
}: AssistantMessageProps) {
  if (isLoading) {
    return (
      <div className="flex justify-start">
        <div className="w-full max-w-6xl">
          <div className="mb-3 px-1 text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
            Assistant
          </div>

          <div className="glass-card rounded-[24px] p-5 sm:p-6">
            <div className="flex items-center gap-3 text-sm text-slate-300">
              <div className="h-2.5 w-2.5 animate-pulse rounded-full bg-sky-300" />
              <span>Analysis in progress...</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const hasTools = Boolean(content.toolTrace && content.toolTrace.length > 0);
  const hasData = Boolean(content.dataUsed);
  const hasSidePanel = hasTools || hasData;

  return (
    <div className="flex justify-start">
      <div className="w-full max-w-6xl">
        <div className="mb-3 px-1 text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
          Assistant
        </div>

        <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_320px]">
          <div className="space-y-4">
            <ResponseText answer={content.answer} />

            {content.stats && content.stats.length > 0 ? (
              <StatsGrid stats={content.stats} />
            ) : null}

            {content.charts && content.charts.length > 0 ? (
              <div className="space-y-4">
                {content.charts.map((chart) => (
                  <ChartCard
                    key={chart.title}
                    title={chart.title}
                    interpretation={chart.interpretation}
                  >
                    <ChartRenderer chart={chart} />
                  </ChartCard>
                ))}
              </div>
            ) : null}

            {content.limitations && content.limitations.length > 0 ? (
              <LimitationsCard limitations={content.limitations} />
            ) : null}

            {content.nextSteps && content.nextSteps.length > 0 ? (
              <NextStepsCard
                nextSteps={content.nextSteps}
                onSelectStep={onSelectStep}
              />
            ) : null}
          </div>

          {hasSidePanel ? (
            <aside className="xl:sticky xl:top-6 xl:self-start">
              <div className="glass-card rounded-[24px] p-3 sm:p-4">
                <div className="mb-3 px-2">
                  <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                    Analysis details
                  </div>
                  <p className="mt-1 text-xs leading-5 text-slate-500">
                    Expand the sections to inspect the tool chain and the data sources used for this answer.
                  </p>
                </div>

                <div className="space-y-3">
                  {hasTools ? (
                    <details
                      className="group overflow-hidden rounded-2xl border border-white/10 bg-white/[0.03]"
                    >
                      <summary className="flex cursor-pointer list-none items-center justify-between gap-3 px-4 py-3">
                        <div>
                          <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                            Tools used
                          </div>
                          <div className="mt-1 text-sm text-white">
                            Execution flow
                          </div>
                        </div>

                        <div className="text-slate-400 transition-transform duration-200 group-open:rotate-180">
                          ▾
                        </div>
                      </summary>

                      <div className="border-t border-white/10 px-3 py-3">
                        <div className="flex flex-col items-center gap-1 py-1">
                          {content.toolTrace?.map((step, index) => (
                            <div
                              key={`${step.tool}-${index}`}
                              className="flex w-full flex-col items-center"
                            >
                              <details className="w-full overflow-hidden rounded-2xl border border-sky-400/15 bg-sky-400/8">
                                <summary
                                  className="cursor-pointer list-none px-3 py-2"
                                  title={`${step.purpose}\n\nInput: ${step.inputSummary}\n\nOutput: ${step.outputSummary}`}
                                >
                                  <div className="text-[11px] font-semibold uppercase tracking-[0.16em] text-sky-200">
                                    Step {index + 1}
                                  </div>
                                  <div className="mt-1 text-sm font-medium text-white">
                                    {step.tool}
                                  </div>
                                  <div className="mt-1 text-xs text-slate-300">
                                    {step.purpose}
                                  </div>
                                </summary>

                                <div className="border-t border-white/10 bg-black/10 px-3 py-3">
                                  <div className="grid gap-3">
                                    <div>
                                      <div className="text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-400">
                                        Input
                                      </div>
                                      <div className="mt-1 rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2 text-xs leading-5 text-slate-200">
                                        {step.inputSummary}
                                      </div>
                                    </div>

                                    <div>
                                      <div className="text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-400">
                                        Output
                                      </div>
                                      <div className="mt-1 rounded-xl border border-white/10 bg-white/[0.03] px-3 py-2 text-xs leading-5 text-slate-200">
                                        {step.outputSummary}
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </details>

                              {index < (content.toolTrace?.length ?? 0) - 1 ? (
                                <div className="flex h-8 items-center justify-center text-slate-500">
                                  ↓
                                </div>
                              ) : null}
                            </div>
                          ))}
                        </div>
                      </div>
                    </details>
                  ) : null}

                  {hasData ? (
                    <details className="group overflow-hidden rounded-2xl border border-white/10 bg-white/[0.03]">
                      <summary className="flex cursor-pointer list-none items-center justify-between gap-3 px-4 py-3">
                        <div>
                          <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                            Data used
                          </div>
                          <div className="mt-1 text-sm text-white">
                            Referenced records
                          </div>
                        </div>

                        <div className="text-slate-400 transition-transform duration-200 group-open:rotate-180">
                          ▾
                        </div>
                      </summary>

                      <div className="border-t border-white/10 px-3 py-3">
                        {content.dataUsed ? (
                          <DataUsedCard dataUsed={content.dataUsed} />
                        ) : null}
                      </div>
                    </details>
                  ) : null}
                </div>
              </div>
            </aside>
          ) : null}
        </div>
      </div>
    </div>
  );
}