import boto3

def create_vpc_and_subnets():
    ec2 = boto3.client('ec2')

    # Create VPC
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = vpc['Vpc']['VpcId']

    ec2.create_tags(
        Resources=[vpc_id],
        Tags=[{'Key': 'Name', 'Value': '2tier-vpc'}]
    )

    ec2.modify_vpc_attribute(
        VpcId=vpc_id,
        EnableDnsHostnames={'Value': True}
    )

    print(f"VPC created: {vpc_id}")

    # Internet Gateway
    igw = ec2.create_internet_gateway()
    igw_id = igw['InternetGateway']['InternetGatewayId']
    ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)

    # Public Subnet
    pub_subnet = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock='10.0.1.0/24',
        AvailabilityZone='ap-south-1a'
    )
    pub_subnet_id = pub_subnet['Subnet']['SubnetId']

    ec2.modify_subnet_attribute(
        SubnetId=pub_subnet_id,
        MapPublicIpOnLaunch={'Value': True}
    )

    # Private Subnet 1
    priv_subnet_1 = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock='10.0.2.0/24',
        AvailabilityZone='ap-south-1a'
    )['Subnet']['SubnetId']

    # Private Subnet 2 (IMPORTANT FOR RDS)
    priv_subnet_2 = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock='10.0.3.0/24',
        AvailabilityZone='ap-south-1b'
    )['Subnet']['SubnetId']

    # Route Table
    rt = ec2.create_route_table(VpcId=vpc_id)
    rt_id = rt['RouteTable']['RouteTableId']

    ec2.create_route(
        RouteTableId=rt_id,
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id
    )

    ec2.associate_route_table(RouteTableId=rt_id, SubnetId=pub_subnet_id)

    print(f"Public: {pub_subnet_id}")
    print(f"Private: {[priv_subnet_1, priv_subnet_2]}")

    return vpc_id, pub_subnet_id, [priv_subnet_1, priv_subnet_2]
