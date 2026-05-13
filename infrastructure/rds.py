import boto3
import time


def create_rds(priv_subnet_id, db_sg_id):
    rds = boto3.client('rds')

    subnet_group_name = '2tier-db-subnet'

    try:
        rds.create_db_subnet_group(
            DBSubnetGroupName=subnet_group_name,
            DBSubnetGroupDescription='RDS private subnets',
            SubnetIds=[priv_subnet_id]
        )
        print("DB Subnet Group created")

    except rds.exceptions.DBSubnetGroupAlreadyExistsFault:
        print("DB Subnet Group already exists")

    try:
        rds.create_db_instance(
            DBInstanceIdentifier='2tier-db',
            DBInstanceClass='db.t3.micro',
            Engine='mysql',
            MasterUsername='admin',
            MasterUserPassword='Admin1234!123',
            DBName='appdb',
            AllocatedStorage=20,
            VpcSecurityGroupIds=[db_sg_id],
            DBSubnetGroupName=subnet_group_name,
            MultiAZ=False,
            PubliclyAccessible=False,
            Tags=[{'Key': 'Name', 'Value': '2tier-rds'}]
        )
        print("RDS creation started")

    except rds.exceptions.DBInstanceAlreadyExistsFault:
        print("RDS already exists, skipping creation")

    waiter = rds.get_waiter('db_instance_available')
    waiter.wait(DBInstanceIdentifier='2tier-db')

    info = rds.describe_db_instances(DBInstanceIdentifier='2tier-db')
    endpoint = info['DBInstances'][0]['Endpoint']['Address']

    print(f"RDS endpoint: {endpoint}")
    return endpoint
