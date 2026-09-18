from cloud_auditor.demo import demo_findings


def test_demo_findings():
    findings = demo_findings()

    assert len(findings) == 4
    assert all(f.provider == "aws" for f in findings)
    assert findings[0].resource_type == "EBS Volume"
    assert findings[1].resource_type == "Elastic IP"
    assert findings[2].resource_type == "EC2 Instance"
    assert findings[3].estimated_monthly_savings == 16.00
