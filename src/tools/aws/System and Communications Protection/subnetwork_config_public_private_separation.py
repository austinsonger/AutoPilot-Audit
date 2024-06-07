# main.py
import sys
import os
# Adjust the Python path to include the parent directory of aws
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _config.config import environments, current_year, current_date
from _config.command_runner import CommandRunner
from _config.aws_handler import AWSHandler

def main():
    command_runner = CommandRunner()
    for env_name, config in environments.items():
        config.set_aws_credentials()  # Set AWS credentials
        aws_handler = AWSHandler(env_name, config)
        # Define the evidence description
        evidence_description = "subnetwork_configuration"
        # Generate the output file paths
        output_file_subnets = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_subnets.json"
        output_file_route_tables = f"/evidence-artifacts/{current_year}/{env_name}/{current_date}.{evidence_description}_route_tables.json"
        # Define the AWS CLI commands with output file paths
        aws_command_subnets = [
            'aws', 'ec2', 'describe-subnets', '--region', config.region, '--output', 'json'
        ]
        aws_command_route_tables = [
            'aws', 'ec2', 'describe-route-tables', '--region', config.region, '--output', 'json'
        ]
        # Collect evidence
        aws_handler.collect_evidence(command_runner, aws_command_subnets, output_file_subnets)
        aws_handler.collect_evidence(command_runner, aws_command_route_tables, output_file_route_tables)

if __name__ == "__main__":
    main()

"""
NIST 800-53 Control Numbers:
- AC-4: Information Flow Enforcement
- SC-7: Boundary Protection
- SC-7(3): Boundary Protection / Access Points

SOC 2 Control Numbers:
- CC6.6: Logical and Physical Access Controls
- CC6.8: System Operations
- CC6.9: Change Management
"""
