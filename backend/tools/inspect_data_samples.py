# backend/tools/inspect_data_samples.py
from typing import Any, Dict
from backend.services.data_access_layer import dal

def execute_inspection(args: Dict[str, Any]) -> Dict[str, Any]:
    material = args.get("material", "metal plate")
    all_tests = dal.get_tests({"material": material})
    
    if not all_tests:
        return {"summary": f"❌ No production records found for: **{material}**", "evidence": {}}

    sample = all_tests[0]
    columns = sample.get("columns", [])
    
    seen_names = set()
    cleaned_cols = []
    golden_keys = {"Standard force", "Maximum force", "Standard travel", "Young's modulus", "Strain at break"}

    for col in columns:
        name = col.get("name")
        val = col.get("value")
        unit = col.get("unit", "-")
        
        if not name or name == "None":
            continue
        if name in seen_names:
            continue
            
        is_important = any(key in name for key in golden_keys)
        has_value = val is not None and str(val).strip() not in ["", "N/A", "None"]

        if is_important or has_value:
            seen_names.add(name)
            cleaned_cols.append({
                "name": name,
                "value": val if has_value else "*(available)*",
                "unit": unit if unit else "-"
            })

    # --- English Render ---
    text_summary = f"## 🔍 Data Structure: {material}\n\n"
    text_summary += "The **Semantic Mapper** has identified the following key physical properties in MongoDB:\n\n"
    text_summary += "| Physical Property | Sample Value | Unit |\n"
    text_summary += "| :--- | :--- | :--- |\n"
    
    # Sort to put Golden Keys first
    cleaned_cols.sort(key=lambda x: any(k in x['name'] for k in golden_keys), reverse=True)

    for col in cleaned_cols[:12]:
        text_summary += f"| **{col['name']}** | {col['value']} | `{col['unit']}` |\n"

    return {
        "summary": text_summary,
        "evidence": {"columns": cleaned_cols, "count": 1}
    }