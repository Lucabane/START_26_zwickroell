import type { AssistantResponse } from "@/types/chat";

export type UserMessage = {
  id: string;
  role: "user";
  content: string;
};

export type AssistantMessage = {
  id: string;
  role: "assistant";
  content: AssistantResponse;
  isLoading?: boolean;
};

export type ChatMessage = UserMessage | AssistantMessage;