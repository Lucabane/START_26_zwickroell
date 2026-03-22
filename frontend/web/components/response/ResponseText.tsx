import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

type ResponseTextProps = {
  answer: string;
};

export function ResponseText({ answer }: ResponseTextProps) {
  if (!answer) return null;

  return (
    <div className="glass-card rounded-[24px] p-5 sm:p-6">
      {/* Header Section */}
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <div className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500">
            Assistant
          </div>
          <div className="mt-0.5 text-sm font-semibold text-white">
            Analysis Summary
          </div>
        </div>

        <div className="flex items-center gap-2 rounded-full border border-sky-400/20 bg-sky-400/10 px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-sky-300">
          <span className="relative flex h-1.5 w-1.5">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-sky-400 opacity-75"></span>
            <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-sky-400"></span>
          </span>
          AI Generated
        </div>
      </div>

      {/* Content Section */}
      <div className="rounded-2xl border border-white/5 bg-black/20 p-4 sm:p-6">
        <div className="prose prose-invert max-w-none 
                        prose-p:text-slate-300 prose-p:leading-relaxed prose-p:text-[15px]
                        prose-headings:text-white prose-headings:mb-4 prose-headings:mt-6 first:prose-headings:mt-0
                        prose-strong:text-sky-300 prose-strong:font-semibold
                        
                        /* Table Styling */
                        prose-table:my-6 prose-table:border-hidden
                        prose-th:bg-white/5 prose-th:text-slate-400 prose-th:font-bold prose-th:text-[11px] prose-th:uppercase prose-th:tracking-widest prose-th:p-3 prose-th:border prose-th:border-white/10
                        prose-td:p-3 prose-td:border prose-td:border-white/10 prose-td:text-slate-300 prose-td:text-sm">
          
          <ReactMarkdown 
            remarkPlugins={[remarkGfm]}
            components={{
              // Force les liens à s'ouvrir dans un nouvel onglet
              a: ({node, ...props}) => <a {...props} target="_blank" rel="noopener noreferrer" className="text-sky-400 hover:underline" />
            }}
          >
            {answer}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
}