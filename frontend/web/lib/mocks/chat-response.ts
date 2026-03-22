import type { AssistantResponse } from "@/types/chat";

export const mockAssistantResponse: AssistantResponse = {
  answer:
    "I found 18 tensile tests performed on steel during the last month. Most of them were carried out on the Z010 machine, with a consistent testing protocol. No significant anomalies were detected in this selection.",

  stats: [
    {
      label: "Tests count",
      value: 18,
      description: "Tensile tests matching the applied filters",
    },
    {
      label: "Material",
      value: "Steel",
      description: "Material inferred from the user query",
    },
    {
      label: "Period",
      value: "Last month",
      description: "Time window interpreted from the question",
    },
    {
      label: "Dominant machine",
      value: "Z010",
      description: "Most represented machine in the dataset",
    },
    {
      label: "Primary standard",
      value: "ISO 6892-1",
      description: "Most frequent testing standard",
    },
  ],

  charts: [
    {
      type: "bar",
      title: "Distribution of tests by machine",
      xLabel: "Machine",
      yLabel: "Number of tests",
      xKey: "machine",
      yKey: "count",
      data: [
        { machine: "Z010", count: 10 },
        { machine: "Z020", count: 5 },
        { machine: "Z100", count: 3 },
      ],
      interpretation:
        "Most of the tests were performed on the Z010 machine.",
    },
    {
      type: "line",
      title: "Test distribution over the last month",
      xLabel: "Date",
      yLabel: "Number of tests",
      xKey: "date",
      yKey: "count",
      data: [
        { date: "2026-02-03", count: 2 },
        { date: "2026-02-07", count: 3 },
        { date: "2026-02-11", count: 4 },
        { date: "2026-02-16", count: 2 },
        { date: "2026-02-21", count: 3 },
        { date: "2026-02-25", count: 4 },
      ],
      interpretation:
        "The tests are relatively evenly distributed across the selected time period.",
    },
  ],

  dataUsed: {
    testsCount: 18,
    filters: [
      { key: "Test type", value: "Tensile" },
      { key: "Material", value: "Steel" },
      { key: "Date range", value: "2026-02-01 → 2026-02-28" },
    ],
    parameters: [
      "Material",
      "Date",
      "Machine",
      "Tester",
      "Standard",
      "Customer",
    ],
    resultTypes: [
      "Maximum force",
      "Tensile strength",
      "Young's modulus",
      "Strain at break",
    ],
    timeRange: {
      start: "2026-02-01",
      end: "2026-02-28",
    },
  },

  toolTrace: [
    {
      step: 1,
      tool: "parse_user_query",
      purpose: "Extract business filters from the user query",
      inputSummary:
        "show me tensile tests on steel from last month",
      outputSummary:
        "testType=tensile, material=steel, dateRange=2026-02-01..2026-02-28",
    },
    {
      step: 2,
      tool: "resolve_material_alias",
      purpose: "Map the user term to a normalized database value",
      inputSummary: "steel",
      outputSummary: "material=Steel",
    },
    {
      step: 3,
      tool: "search_tests",
      purpose: "Retrieve tests matching the filters",
      inputSummary:
        "type=tensile, material=Steel, dateRange=2026-02-01..2026-02-28",
      outputSummary: "18 tests found",
    },
    {
      step: 4,
      tool: "summarize_test_metadata",
      purpose: "Aggregate key metadata for analysis",
      inputSummary: "18 tests",
      outputSummary:
        "dominant machine=Z010, primary standard=ISO 6892-1",
    },
    {
      step: 5,
      tool: "build_visualizations",
      purpose: "Prepare data for charts",
      inputSummary: "18 filtered tests",
      outputSummary: "2 charts generated",
    },
    {
      step: 6,
      tool: "generate_final_answer",
      purpose: "Generate a clear and structured response",
      inputSummary: "summary + stats + charts + traceability",
      outputSummary: "final structured response ready",
    },
  ],

  limitations: [
    "This response provides an overview of the tests and their main metadata, without including detailed raw curve data.",
    "The 'steel' category is interpreted as a business-level grouping of steel-type materials.",
  ],

  nextSteps: [
    "Show the full details of the 18 tests",
    "Compare these results with the previous month",
    "Analyze the average tensile strength for this selection",
  ],
};