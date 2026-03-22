# backend/tools/find_tests.py
from typing import Any, Dict
from backend.services.data_access_layer import dal

def find_tests(args: Dict[str, Any]) -> Dict[str, Any]:
    limit = args.get("limit", 5)
    material = args.get("material", "metal plate")
    
    # 1. Database Scan
    filters = {k: v for k, v in args.items() if k not in ["limit"] and v}
    all_tests = dal.get_tests(filters)
    total_count = len(all_tests)
    
    # 2. Sample selection
    samples = all_tests[:limit]
    
    if not samples:
        return {"summary": f"❌ No matching tests found for **{material}**.", "evidence": {"count": 0}}

    # 3. English Markdown Table Construction
    text_summary = f"## 📋 Search Results\n\n"
    text_summary += f"Showing the latest **{len(samples)}** records identified for **{material}**:\n\n"
    
    text_summary += "| Test ID | Date | Machine | Customer |\n"
    text_summary += "| :--- | :--- | :--- | :--- |\n"
    
    for t in samples:
        tid = t.get("test_id", "N/A")
        date = (t.get("date") or "N/A")[:10]
        mach = t.get("machine", "N/A")
        cust = t.get("customer", "N/A")
        text_summary += f"| `{tid}` | {date} | {mach} | {cust} |\n"

    text_summary += f"\n\n> **System:** A total of **{total_count}** documents were analyzed in MongoDB for this query."

    # 4. Evidence return
    return {
        "summary": text_summary,
        "evidence": {
            "count": len(samples),
            "total_count": total_count,
            "samples": [t.get("test_id") for t in samples]
        }
    }