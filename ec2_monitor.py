import subprocess
import json
import sys

REGION = "ap-south-1"

def get_ec2_instance():

    command = ["aws", "ec2", "describe-instances", "--region", REGION, "--output", "json"]

    result = subprocess.run(command, capture_output = True, text = True)

    if result.returncode != 0:
        print("Error! Fetching EC2 Instances")
        print(result.stderr)
        sys.exit(1)

    return json.loads(result.stdout)

def get_instance_status():

    command = ["aws", "ec2", "describe-instance-status", "--region", REGION, "--include-all-instances", "--output", "json"]

    result = subprocess.run(command, capture_output = True, text = True)

    if result.returncode != 0:
        print("Error! Fetching Instance Status")
        print(result.stderr)
        sys.exit(1)

    return json.loads(result.stdout)

def main():

    instance_data = get_ec2_instance()
    instance_status = get_instance_status()

    status_lookup = {
        item["InstanceId"] : item
        for item in instance_status["InstanceStatuses"]
    }

    instances = [
        instance
        for reservation in instance_data["Reservations"]
        for instance in reservation["Instances"]
    ]

    if not instances:
        print("No EC2 Instances Found", REGION)
        return

    print(f"\nEC2 Instance Report - {REGION}")
    print("-" * 90)

    for instance in instances:
        instance_id = instance["InstanceId"]
        state = instance["State"]["Name"]
        instance_type = instance["InstanceType"]

        name = next(
            (
                tag["Value"]
                for tag in instance.get("Tags", [])
                if tag["Key"] == "Name"
            ),
            "Unnamed"
        )

        system_status = status_lookup.get(instance_id, {})
        system_health_check = system_status.get(
            "SystemStatus", {}
        ).get("Status", "not-available")

        instance_health_check = system_status.get(
            "InstanceStatus", {}
        ).get("Status", "not-available")

        if state != "running":
            alert = "NOT RUNNING"
        elif system_health_check != "ok" or instance_health_check != "ok":
            alert = "CHECK REQUIRED"
        else:
            alert = "HEALTHY"

        print(f"Name:           {name}")
        print(f"Instance ID:    {instance_id}")
        print(f"Type:           {instance_type}")
        print(f"State:          {state}")
        print(f"System Check:   {system_health_check}")
        print(f"Instance Check: {instance_health_check}")
        print(f"Result:         {alert}")
        print("-" * 90)

if __name__ == "__main__":
    main()
