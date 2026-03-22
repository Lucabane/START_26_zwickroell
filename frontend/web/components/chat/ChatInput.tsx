type ChatInputProps = {
  value: string;
  onChange: (value: string) => void;
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  disabled?: boolean;
};

export default function ChatInput({
  value,
  onChange,
  onSubmit,
  disabled = false,
}: ChatInputProps) {
  return (
    <form onSubmit={onSubmit} className="mx-auto flex w-full max-w-4xl gap-3">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Ask a question about your test data..."
        disabled={disabled}
        className="flex-1 rounded-xl border border-white/10 bg-[#0f1a2d] px-4 py-3 text-sm text-white outline-none transition
        placeholder:text-slate-500
        focus:border-sky-400 focus:ring-1 focus:ring-sky-400/40
        disabled:cursor-not-allowed disabled:opacity-60"
      />

      <button
        type="submit"
        disabled={disabled || !value.trim()}
        className="rounded-xl bg-sky-500 px-5 py-3 text-sm font-medium text-white transition
        hover:bg-sky-400
        disabled:cursor-not-allowed disabled:bg-slate-600"
      >
        {disabled ? "Analyzing..." : "Send"}
      </button>
    </form>
  );
}