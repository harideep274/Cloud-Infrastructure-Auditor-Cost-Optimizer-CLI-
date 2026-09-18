import csv
import json

from pathlib import Path

from rich.console import Console
from rich.table import Table

from .models import Finding


def render(
    findings: list[Finding]
):
    """
    Render findings in terminal.
    """

    table = Table(
        title="Cloud Infrastructure Audit"
    )

    table.add_column("Region")
    table.add_column("Type")
    table.add_column("Resource")
    table.add_column("Issue")
    table.add_column("Severity")
    table.add_column("Est. Monthly $")

    for finding in findings:

        table.add_row(
            finding.region,
            finding.resource_type,
            finding.resource_id,
            finding.issue,
            finding.severity,
            f"{finding.estimated_monthly_savings:.2f}"
        )

    Console().print(
        table
    )

    total = sum(
        finding.estimated_monthly_savings
        for finding in findings
    )

    Console().print(
        f"\nPotential monthly savings: "
        f"${total:,.2f}"
    )


def export(
    findings,
    path: str
):
    """
    Export report to JSON or CSV.
    """

    output = Path(path)

    rows = [
        finding.to_dict()
        for finding in findings
    ]

    if output.suffix.lower() == ".json":

        output.write_text(
            json.dumps(
                rows,
                indent=2,
                default=str
            )
        )

        return

    if output.suffix.lower() == ".csv":

        flat_rows = []

        for row in rows:

            copy = row.copy()

            copy["metadata"] = json.dumps(
                copy["metadata"],
                default=str
            )

            flat_rows.append(
                copy
            )

        fieldnames = [
            "provider",
            "account",
            "region",
            "resource_type",
            "resource_id",
            "issue",
            "severity",
            "estimated_monthly_savings",
            "recommendation",
            "metadata"
        ]

        with output.open(
            "w",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()

            writer.writerows(
                flat_rows
            )

        return

    raise ValueError(
        "Output must end in .json or .csv"
    )
