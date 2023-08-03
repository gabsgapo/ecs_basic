from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ecs_patterns as ecs_patterns
)
from constructs import Construct

class CdkEcsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(self, "VPC",
            nat_gateways=0,
            subnet_configuration=[ec2.SubnetConfiguration(name="public_subnet", subnet_type=ec2.SubnetType.PUBLIC)]
        )

        # Create IAM Role for ECS container
        app_role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            description="Container app role"
        )
        
        # Create task definition to deploy Fargate
        task = ecs.FargateTaskDefinition(self, "Task",
            task_role=app_role
        )
        
        # Build Container from Docker hub registry
        container = task.add_container("MyContainer",
            image=ecs.ContainerImage.from_registry("nginx:latest"),
            memory_reservation_mib=256,
            cpu=256
        )
        port_mapping = ecs.PortMapping(
            container_port=80,
            protocol=ecs.Protocol.TCP
        )
        container.add_port_mappings(port_mapping)
        
        # Config Fargate service
        lb_fargate = ecs_patterns.ApplicationLoadBalancedFargateService(self, "MyApp",
            vpc=vpc,
            task_definition=task,
            desired_count=1,
            service_name="MyWebApp",
            assign_public_ip=True,
            public_load_balancer=True
        )
