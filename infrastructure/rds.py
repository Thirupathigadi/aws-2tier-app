import boto3

def create_db_sg(vpc_id, web_sg_id):
    ec2 = boto3.client('ec2')

    sg = ec2.create_security_group(
        GroupName='db-sg',
        Description='DB tier security group',
        VpcId=vpc_id
    )

    sg_id = sg['GroupId']

    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[{
            'IpProtocol': 'tcp',
            'FromPort': 3306,
            'ToPort': 3306,
            'UserIdGroupPairs': [{'GroupId': web_sg_id}]
        }]
    )

    print(f"DB SG created: {sg_id}")
    return sg_id


def create_rds(priv_subnet_ids, db_sg_id):

    rds = boto3.client('rds')

    subnet_group_name = "tier-db-subnet"

    # Create subnet group
    try:
        rds.create_db_subnet_group(
            DBSubnetGroupName=subnet_group_name,
            DBSubnetGroupDescription='RDS private subnets',
            SubnetIds=priv_subnet_ids
        )
        print("DB subnet group created")

    except rds.exceptions.DBSubnetGroupAlreadyExistsFault:
        print("DB subnet group already exists")

    # Create DB instance
    rds.create_db_instance(
        DBInstanceIdentifier='tier-db',
        DBInstanceClass='db.t3.micro',
        Engine='mysql',
        MasterUsername='admin',
        MasterUserPassword='Admin1234!123',
        DBName='appdb',
        AllocatedStorage=20,
        VpcSecurityGroupIds=[db_sg_id],
        DBSubnetGroupName=subnet_group_name,
        MultiAZ=False,
        PubliclyAccessible=False
    )

    print("RDS creating... wait 5–10 mins")

    waiter = rds.get_waiter('db_instance_available')
    waiter.wait(DBInstanceIdentifier='2tier-db')

    endpoint = rds.describe_db_instances(
        DBInstanceIdentifier='2tier-db'
    )['DBInstances'][0]['Endpoint']['Address']

    print(f"RDS endpoint: {endpoint}")
    return endpoint
