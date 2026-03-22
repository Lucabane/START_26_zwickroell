type UserMessageProps = {
  content: string;
};

export default function UserMessage({ content }: UserMessageProps) {
  return (
    <div className="flex justify-end">
      <div className="max-w-2xl rounded-2xl bg-slate-900 px-4 py-3 text-sm text-white shadow">
        {content}
      </div>
    </div>
  );
}