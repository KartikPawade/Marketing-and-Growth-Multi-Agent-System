from app.graph.node_wrapper import node_logger
from app.schemas.qa import QAReport


@node_logger("qa")
def qa_node(state):
    content = state.get("content")
    issues: list[str] = []
    recommendations: list[str] = []

    if not content:
        issues.append("No content to review")
        passed = False
    else:
        # Simple QA: content exists (dict from ContentOutput or legacy)
        if isinstance(content, dict):
            assets = content.get("assets") or []
            if not assets:
                issues.append("No content assets generated")
            for i, asset in enumerate(assets):
                if not asset.get("headline") or not asset.get("body"):
                    issues.append(f"Asset {i + 1}: missing headline or body")
        passed = len(issues) == 0
        if not passed and not recommendations:
            recommendations.append("Address the issues above before publishing.")

    report = QAReport(passed=passed, issues=issues, recommendations=recommendations)
    state["qa_report"] = report.model_dump()
    return state