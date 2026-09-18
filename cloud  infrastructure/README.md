


## Demo Mode

If your AWS account has restricted access to EC2, EBS, or Elastic IP APIs, you can run the auditor using built-in sample infrastructure data:

```bash
python3 -m cloud_auditor.cli audit --demo
```

Demo Mode does not connect to AWS and does not modify any cloud resources. It is intended for demonstrations, development, and testing when real AWS scanning is unavailable.
