import type { ReactNode } from "react";

type ChatShellProps = {
  header: ReactNode;
  messages: ReactNode;
  input: ReactNode;
};

export default function ChatShell({
  header,
  messages,
  input,
}: ChatShellProps) {
  return (
    <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col gap-6">
      <header>{header}</header>

      <main className="glass-panel flex min-h-[calc(100vh-220px)] flex-1 flex-col overflow-hidden rounded-[28px]">
        <div className="border-b border-white/10 px-4 py-3 sm:px-6">
          <div className="flex items-center justify-between gap-3">
            <div>
              <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Workspace
              </div>
              <div className="mt-1 text-sm text-slate-300">
                Ask questions in English and explore your lab data visually.
              </div>
            </div>

            <div className="hidden items-center gap-2 md:flex">
              <div className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs font-medium text-emerald-200">
                Backend connected
              </div>
            </div>
          </div>
        </div>

        <div className="flex min-h-0 flex-1 flex-col">
          <div className="scrollbar-thin min-h-0 flex-1 overflow-y-auto px-4 py-5 sm:px-6 sm:py-6">
            {messages}
          </div>

          <div className="border-t border-white/10 bg-white/[0.02] px-4 py-4 sm:px-6">
            {input}
          </div>
        </div>
      </main>
    </div>
  );
}