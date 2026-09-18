import typer

from rich.console import Console

from .aws import session
from .demo import demo_findings
from .audit import scan_aws
from .report import render, export
from .cleanup import execute, plan


app = typer.Typer(
    help=(
        "Cloud Infrastructure Auditor "
        "& FinOps Cost Optimizer"
    )
)

console = Console()


@app.command()
def audit(

    profile: str = typer.Option(
        None,
        "--profile",
        help="AWS named profile"
    ),

    role_arn: str = typer.Option(
        None,
        "--role-arn",
        help="Optional IAM role ARN to assume"
    ),

    days: int = typer.Option(
        14,
        min=1,
        max=90,
        help="CloudWatch lookback period"
    ),

    cpu_threshold: float = typer.Option(
        5.0,
        min=0,
        max=100,
        help="Low CPU threshold"
    ),

    output: str = typer.Option(
        None,
        "--output",
        "-o",
        help="CSV or JSON report"
    ),

    no_ec2: bool = typer.Option(
        False,
        "--no-ec2",
        help="Skip EC2 utilization scan"
    ),

    demo: bool = typer.Option(
        False,
        "--demo",
        help="Run with sample data without connecting to AWS"
    )
):
    """
    Audit all enabled AWS regions.
    """

    try:

        if demo:
            findings = demo_findings()
        else:
            aws_session = session(
                profile,
                role_arn
            )

            findings = scan_aws(
                aws_session,
                include_ec2=not no_ec2,
                days=days,
                cpu_threshold=cpu_threshold
            )

        render(
            findings
        )

        if output:

            export(
                findings,
                output
            )

            console.print(
                f"Report written to {output}"
            )

    except Exception as exc:

        console.print(
            f"[bold red]"
            f"Audit failed:"
            f"[/bold red] {exc}"
        )

        raise typer.Exit(
            code=1
        )


@app.command()
def cleanup(

    profile: str = typer.Option(
        None,
        "--profile"
    ),

    role_arn: str = typer.Option(
        None,
        "--role-arn"
    ),

    dry_run: bool = typer.Option(
        True,
        "--dry-run/--execute",
        help="Dry-run is the default"
    ),

    confirm: bool = typer.Option(
        False,
        "--confirm",
        help="Required for destructive operations"
    )
):
    """
    Show or execute safe cleanup candidates.
    """

    try:

        aws_session = session(
            profile,
            role_arn
        )

        findings = scan_aws(
            aws_session,
            include_ec2=False
        )

        candidates = plan(
            findings
        )

        render(
            candidates
        )

        if dry_run:

            console.print(
                "\nDry-run only: "
                "no resources changed."
            )

            return

        if not confirm:

            console.print(
                "[bold red]"
                "Missing --confirm; "
                "refusing execution."
                "[/bold red]"
            )

            raise typer.Exit(
                code=2
            )

        execute(
            aws_session,
            candidates,
            confirm=True
        )

    except typer.Exit:

        raise

    except Exception as exc:

        console.print(
            f"[bold red]"
            f"Cleanup failed:"
            f"[/bold red] {exc}"
        )

        raise typer.Exit(
            code=1
        )


@app.command()
def version():
    """
    Display application version.
    """

    from . import __version__

    console.print(
        f"cloud-auditor {__version__}"
    )


if __name__ == "__main__":
    app()
    