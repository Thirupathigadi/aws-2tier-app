import boto3

def create_web_sg(vpc_id):
    ec2 = boto3.client('ec2')
    sg = ec2.create_security_group(
        GroupName='web-sg', Description='Web tier', VpcId=vpc_id)
    sg_id = sg['GroupId']
    ec2.authorize_security_group_ingress(GroupId=sg_id, IpPermissions=[
        {'IpProtocol':'tcp','FromPort':80,'ToPort':80,
         'IpRanges':[{'CidrIp':'0.0.0.0/0'}]},
        {'IpProtocol':'tcp','FromPort':5000,'ToPort':5000,
         'IpRanges':[{'CidrIp':'0.0.0.0/0'}]},
        {'IpProtocol':'tcp','FromPort':22,'ToPort':22,
         'IpRanges':[{'CidrIp':'0.0.0.0/0'}]},
    ])
    print(f"Web SG created: {sg_id}")
    return sg_id

def launch_ec2(subnet_id, sg_id, db_endpoint):
    ec2 = boto3.resource('ec2')
    user_data = f"""#!/bin/bash
yum update -y
yum install -y python3 python3-pip git
pip3 install flask pymysql gunicorn cryptography
cd /home/ec2-user
git clone https://github.com/YOUR_USERNAME/aws-2tier-app.git
cd aws-2tier-app
export DB_HOST="{db_endpoint}"
export DB_USER="admin"
export DB_PASSWORD="Admin1234!"
export DB_NAME="appdb"
nohup gunicorn -w 2 -b 0.0.0.0:5000 app.app:app &
"""
    instances = ec2.create_instances(
        ImageId='ami-0f58b397bc5c1f2e8',
        InstanceType='t2.micro',
        MinCount=1, MaxCount=1,
        SubnetId=subnet_id,
        SecurityGroupIds=[sg_id],
        UserData=user_data,
        TagSpecifications=[{
            'ResourceType':'instance',
            'Tags':[{'Key':'Name','Value':'web-server'}]
        }]
    )
    instance = instances[0]
    print("Waiting for EC2 to start...")
    instance.wait_until_running()
    instance.reload()
    print(f"EC2 ready: {instance.id} | IP: {instance.public_ip_address}")
    return instance
