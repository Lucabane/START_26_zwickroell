import { mockAssistantResponse } from "../mocks/chat-response";
import type { AssistantResponse } from "../../types/chat";

export async function sendChatMessage(
  message: string,
): Promise<AssistantResponse> {
  console.log("Sending message to backend:", message);

  try {
    const response = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    const data = await response.json();
    console.log("Backend response:", data);

    return data;
  } catch (error) {
    console.error("API failed, fallback to mock:", error);

    // fallback pour la démo si backend cassé
    await new Promise((resolve) => setTimeout(resolve, 500));
    return mockAssistantResponse;
  }
}