from cloud_auditor.models import Finding


def test_finding_serialization():

    finding = Finding(
        provider="aws",
        account="123456789012",
        region="us-east-1",
        resource_type="EBS Volume",
        resource_id="vol-123",
        issue="Unattached",
        severity="medium",
        estimated_monthly_savings=1.20
    )

    data = finding.to_dict()

    assert data["resource_id"] == "vol-123"

    assert (
        data["estimated_monthly_savings"]
        == 1.20
    )
    