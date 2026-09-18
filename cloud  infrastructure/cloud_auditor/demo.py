from .models import Finding


def demo_findings():
    """Return realistic sample findings for demonstrations."""
    return [
        Finding(
            provider="aws",
            account="123456789012",
            region="ap-south-1",
            resource_type="EBS Volume",
            resource_id="vol-demo-001",
            issue="Unattached EBS volume",
            severity="medium",
            estimated_monthly_savings=8.00,
            recommendation="Delete the volume if it is no longer required.",
            metadata={"size_gib": 100, "state": "available"},
        ),
        Finding(
            provider="aws",
            account="123456789012",
            region="ap-south-1",
            resource_type="Elastic IP",
            resource_id="eip-demo-001",
            issue="Unassociated Elastic IP",
            severity="medium",
            estimated_monthly_savings=3.65,
            recommendation="Release the Elastic IP if it is not required.",
            metadata={"associated": False},
        ),
        Finding(
            provider="aws",
            account="123456789012",
            region="us-east-1",
            resource_type="EC2 Instance",
            resource_id="i-demo-001",
            issue="Low CPU utilization",
            severity="low",
            estimated_monthly_savings=0.00,
            recommendation="Consider stopping, downsizing, or scheduling this instance.",
            metadata={"instance_type": "t3.large", "avg_cpu_percent": 2.4},
        ),
        Finding(
            provider="aws",
            account="123456789012",
            region="eu-west-1",
            resource_type="EBS Volume",
            resource_id="vol-demo-002",
            issue="Unattached EBS volume",
            severity="high",
            estimated_monthly_savings=16.00,
            recommendation="Review and delete the volume if it is no longer required.",
            metadata={"size_gib": 200, "state": "available"},
        ),
    ]
