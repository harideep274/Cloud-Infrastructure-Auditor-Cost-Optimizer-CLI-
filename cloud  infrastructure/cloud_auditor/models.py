from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Finding:
    provider: str
    account: str
    region: str
    resource_type: str
    resource_id: str
    issue: str
    severity: str
    estimated_monthly_savings: float = 0.0
    recommendation: str = ""
    metadata: dict[str, Any] | None = None

    def to_dict(self):
        return asdict(self)
    