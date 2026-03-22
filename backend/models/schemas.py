from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field, model_validator

ToolName = Literal["find_tests", "summarize_tests", "compare_groups", "trend_analysis", "inspect_data_samples"]
ChartType = Literal["line", "bar", "scatter", "box"]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


class AssistantChart(BaseModel):
    type: ChartType
    title: str
    xLabel: str
    yLabel: str
    xKey: str
    yKey: str
    data: List[Dict[str, Any]] = Field(default_factory=list)
    interpretation: Optional[str] = None


class AssistantStat(BaseModel):
    label: str
    value: Union[str, int, float]
    description: Optional[str] = None


class DataFilter(BaseModel):
    key: str
    value: str


class TimeRange(BaseModel):
    start: str
    end: str


class DataUsed(BaseModel):
    testsCount: int = 0
    filters: List[DataFilter] = Field(default_factory=list)
    parameters: List[str] = Field(default_factory=list)
    resultTypes: List[str] = Field(default_factory=list)
    timeRange: Optional[TimeRange] = None


class ToolTraceStep(BaseModel):
    step: int
    tool: str
    purpose: str
    inputSummary: str
    outputSummary: str


class ChatResponse(BaseModel):
    answer: str
    charts: List[AssistantChart] = Field(default_factory=list)
    stats: List[AssistantStat] = Field(default_factory=list)
    dataUsed: Optional[DataUsed] = None
    toolTrace: List[ToolTraceStep] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    nextSteps: List[str] = Field(default_factory=list)
    toolUsed: Optional[str] = None


class ToolCall(BaseModel):
    tool_name: ToolName
    args: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_args(self) -> "ToolCall":
        # 1. Liste des arguments obligatoires (le strict minimum)
        required = {
            "find_tests": [],
            "summarize_tests": [],
            "compare_groups": ["material", "metric", "group_by", "group_a", "group_b"],
            "trend_analysis": ["material", "metric", "date_range"],
            "inspect_data_samples": ["material"],
        }

        # 2. Liste des arguments AUTORISÉS (la "whitelist")
        allowed = {
            "find_tests": {"material", "test_type", "machine", "site", "customer", "date_range", "limit"},
            "summarize_tests": {"material", "test_type", "machine", "site", "customer", "date_range"},
            # AJOUT DE "normalize_units" ICI :
            "compare_groups": {
                "material", "metric", "group_by", "group_a", "group_b", 
                "test_type", "site", "customer", "date_range", "normalize_units"
            },
            "trend_analysis": {"material", "metric", "test_type", "group_by", "machine", "site", "date_range"},
            "inspect_data_samples": {"material", "test_type", "machine", "site", "customer", "date_range"},
        }
        
        # Validation des manquants
        missing = [k for k in required[self.tool_name] if not self.args.get(k)]
        if missing:
            raise ValueError(f"Missing required args for {self.tool_name}: {', '.join(missing)}")
            
        # Validation des intrus (c'est ici que l'erreur 500 s'arrêtera)
        invalid = set(self.args) - allowed[self.tool_name]
        if invalid:
            raise ValueError(f"Invalid args for {self.tool_name}: {', '.join(sorted(invalid))}")
            
        return self


class FinalAnswer(BaseModel):
    answer: str
    suggested_follow_up: Optional[str] = None