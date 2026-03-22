export type ChartType = "line" | "bar" | "scatter" | "box";

export type AssistantChart = {
  type: ChartType;
  title: string;
  xLabel: string;
  yLabel: string;
  xKey: string;
  yKey: string;
  data: Record<string, unknown>[];
  interpretation?: string;
};

export type AssistantStat = {
  label: string;
  value: string | number;
  description?: string;
};

export type DataUsed = {
  testsCount: number;
  filters: Array<{
    key: string;
    value: string;
  }>;
  parameters: string[];
  resultTypes: string[];
  timeRange?: {
    start: string;
    end: string;
  };
};

export type ToolTraceStep = {
  step: number;
  tool: string;
  purpose: string;
  inputSummary: string;
  outputSummary: string;
};

export type AssistantResponse = {
  answer: string;
  charts?: AssistantChart[];
  stats?: AssistantStat[];
  dataUsed?: DataUsed;
  toolTrace?: ToolTraceStep[];
  limitations?: string[];
  nextSteps?: string[];
  toolUsed?: string;
};