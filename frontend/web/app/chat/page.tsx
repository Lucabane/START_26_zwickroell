"use client";

import { FormEvent, useState } from "react";
import ChatShell from "@/components/chat/ChatShell";
import MessageList from "@/components/chat/MessageList";
import ChatInput from "@/components/chat/ChatInput";
import { sendChatMessage } from "@/lib/api/chat";
import type { ChatMessage } from "@/types/message";
import type { AssistantResponse } from "@/types/chat";

function createLoadingResponse(): AssistantResponse {
  return {
    answer: "",
  };
}

export default function ChatPage() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [scrollToMessageId, setScrollToMessageId] = useState<string | null>(null);

  async function submitMessage(text: string) {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    const userMessageId = crypto.randomUUID();

    const userMessage: ChatMessage = {
      id: userMessageId,
      role: "user",
      content: trimmed,
    };

    const loadingMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: createLoadingResponse(),
      isLoading: true,
    };

    setMessages((prev) => [...prev, userMessage, loadingMessage]);
    setScrollToMessageId(userMessageId);
    setInput("");
    setIsLoading(true);

    try {
      const assistantResponse = await sendChatMessage(trimmed);

      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: assistantResponse,
      };

      setMessages((prev) => {
        const withoutLoading = prev.filter(
          (message) => !(message.role === "assistant" && message.isLoading)
        );

        return [...withoutLoading, assistantMessage];
      });
    } catch (error) {
      console.error("Failed to send chat message:", error);

      const errorMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: {
          answer: "An error occurred while retrieving the analysis.",
          limitations: [
            "The backend did not respond correctly.",
            "Make sure the FastAPI API is running and reachable.",
          ],
          nextSteps: [
            "Retry the same request",
            "Show me the tensile tests performed on steel during the last month",
          ],
        },
      };

      setMessages((prev) => {
        const withoutLoading = prev.filter(
          (message) => !(message.role === "assistant" && message.isLoading)
        );

        return [...withoutLoading, errorMessage];
      });
    } finally {
      setIsLoading(false);
    }
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    await submitMessage(input);
  }

  async function handleSelectStep(step: string) {
    await submitMessage(step);
  }

  return (
    <div className="app-shell">
      <ChatShell
        header={
          <div className="glass-panel overflow-hidden rounded-[28px] p-6 sm:p-8">
            <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
              <div className="max-w-3xl">
                <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-sky-400/20 bg-sky-400/10 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.22em] text-sky-200">
                  AI Copilot for Materials Testing
                </div>

                <h1 className="max-w-3xl text-3xl font-semibold tracking-tight text-white sm:text-4xl lg:text-5xl">
                  Chat with Your Test Data
                </h1>

                <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-300 sm:text-base">
                  Ask questions about tensile, compression, quality, trends, and
                  cross-machine comparisons in plain English.
                </p>
              </div>

              <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
                <div className="glass-card-soft rounded-2xl px-4 py-3">
                  <div className="text-[11px] uppercase tracking-[0.18em] text-slate-400">
                    Mode
                  </div>
                  <div className="mt-1 text-sm font-semibold text-white">
                    Live analysis
                  </div>
                </div>

                <div className="glass-card-soft rounded-2xl px-4 py-3">
                  <div className="text-[11px] uppercase tracking-[0.18em] text-slate-400">
                    Output
                  </div>
                  <div className="mt-1 text-sm font-semibold text-white">
                    Charts + summary
                  </div>
                </div>

                <div className="glass-card-soft rounded-2xl px-4 py-3 col-span-2 sm:col-span-1">
                  <div className="text-[11px] uppercase tracking-[0.18em] text-slate-400">
                    Language
                  </div>
                  <div className="mt-1 text-sm font-semibold text-white">
                    English
                  </div>
                </div>
              </div>
            </div>
          </div>
        }
        messages={
          <MessageList
            messages={messages}
            onSelectStep={handleSelectStep}
          />
        }
        input={
          <ChatInput
            value={input}
            onChange={setInput}
            onSubmit={handleSubmit}
            disabled={isLoading}
          />
        }
      />
    </div>
  );
}