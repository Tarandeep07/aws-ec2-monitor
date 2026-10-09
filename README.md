# AWS EC2 Instance Monitoring

A Python-based AWS EC2 monitoring tool that uses the AWS CLI to list EC2 instances, check their running state and health status, and identify instances requiring attention. This project automates routine cloud monitoring to reduce manual effort.

## Features

* Lists EC2 instances in a specified AWS region.
* Displays instance ID, name, type, and current state.
* Retrieves system and instance health checks.
* Identifies instances that are not running or require attention.
* Handles AWS CLI errors and missing instance information.

## Technologies Used

* **Python** — scripting and automation
* **AWS CLI** — interaction with AWS services
* **Amazon EC2** — virtual server management
* **JSON** — processing AWS responses

## Project Structure

```text
aws-ec2-instance-monitor/
├── ec2_monitor.py
├── README.md
```

## Prerequisites

* Python 3 installed
* AWS CLI installed
* An AWS account with appropriate EC2 read permissions
* AWS CLI credentials configured

Verify your installations:

```bash
python --version
aws --version
aws sts get-caller-identity
```

## Configuration

Configure the AWS CLI:

```bash
aws configure
```

Set the AWS region in `ec2_monitor.py`:

```python
REGION = "ap-south-1"
```

Change the region if your EC2 instances are located elsewhere.

The configured identity requires permissions to call:

* `ec2:DescribeInstances`
* `ec2:DescribeInstanceStatus`

Use read-only permissions and avoid hardcoding credentials in the script.

## Usage

Run the monitoring script:

```bash
python ec2_monitor.py
```

The script retrieves EC2 instance details and health information, then generates a report in the terminal.

## Sample Output

```text
EC2 Instance Report - ap-south-1
------------------------------------------------------------------------------------------
Name:           Web-Server
Instance ID:    i-0123456789abcdef0
Type:           t2.micro
State:          running
System Check:   ok
Instance Check: ok
Result:         HEALTHY
------------------------------------------------------------------------------------------
Name:           Test-Server
Instance ID:    i-0abcdef1234567890
Type:           t2.micro
State:          stopped
System Check:   not-available
Instance Check: not-available
Result:         NOT RUNNING
------------------------------------------------------------------------------------------
```

*Note: The output above is illustrative. Actual results depend on your AWS account and EC2 instances.*

## Monitoring Logic

| Condition                                           | Result           |
| --------------------------------------------------- | ---------------- |
| Instance state is not `running`                     | `NOT RUNNING`    |
| Instance is running, but a health check is not `ok` | `CHECK REQUIRED` |
| Instance is running and both health checks are `ok` | `HEALTHY`        |

A running instance is not necessarily healthy. The system and instance status checks provide additional information about its operational condition.

## Error Handling

The script checks AWS CLI command failures and displays the corresponding error message. It also handles missing instance names and unavailable health-check information.

## Future Improvements

* Save monitoring reports to log files.
* Send alerts through Amazon SNS.
* Schedule periodic monitoring using Linux cron.
* Export reports to CSV.
* Extend monitoring to multiple AWS regions.

## Learning Outcomes

This project demonstrates practical use of Python scripting, AWS CLI commands, JSON parsing, Amazon EC2 monitoring, error handling, and cloud automation.
