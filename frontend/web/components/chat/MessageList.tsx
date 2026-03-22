"use client";

import { useEffect, useRef } from "react";
import type { ChatMessage } from "@/types/message";
import AssistantMessage from "@/components/chat/AssistantMessage";
import UserMessage from "@/components/chat/UserMessage";

type MessageListProps = {
  messages: ChatMessage[];
  onSelectStep?: (step: string) => void;
  scrollToMessageId?: string | null;
};

export default function MessageList({
  messages,
  onSelectStep,
  scrollToMessageId,
}: MessageListProps) {
  const messageRefs = useRef<Record<string, HTMLDivElement | null>>({});

  useEffect(() => {
    if (!scrollToMessageId) return;

    const target = messageRefs.current[scrollToMessageId];
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, [scrollToMessageId, messages]);

  if (messages.length === 0) {
    return (
      <div className="glass-card rounded-2xl border border-dashed border-white/10 p-6 text-sm text-slate-400">
        <div>No messages yet. Try asking something like:</div>

        <div className="mt-4 rounded-xl border border-white/10 bg-white/[0.04] p-4 font-medium text-slate-200">
          Show me 3 tests for steel.
        </div>
      </div>
    );
  }

  return (
    <>
      {messages.map((message) => (
        <div
          key={message.id}
          ref={(el) => {
            messageRefs.current[message.id] = el;
          }}
        >
          {message.role === "user" ? (
            <UserMessage content={message.content} />
          ) : (
            <AssistantMessage
              content={message.content}
              isLoading={message.isLoading}
              onSelectStep={onSelectStep}
            />
          )}
        </div>
      ))}
    </>
  );
}