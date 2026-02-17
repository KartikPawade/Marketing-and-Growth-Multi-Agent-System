# app/agents/qa_agent.py
from app.schemas.qa import QAReport


class QAAgent:
    def __init__(self) -> None:
        pass

    def run(self, content: dict | None) -> QAReport:
        issues: list[str] = []
        recommendations: list[str] = []

        if not content:
            issues.append("No content to review")
            passed = False
        else:
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

        return QAReport(passed=passed, issues=issues, recommendations=recommendations)
