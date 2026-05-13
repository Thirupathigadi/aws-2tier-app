import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from vpc import create_vpc_and_subnets
from ec2 import create_web_sg, launch_ec2
from rds import create_db_sg, create_rds

def main():

    print("\n=== STEP 1: VPC & Subnets ===")
vpc_id, pub_subnet_id, priv_subnet_ids = create_vpc_and_subnets()

print("\n=== STEP 2: Security Groups ===")
web_sg_id = create_web_sg(vpc_id)
db_sg_id  = create_db_sg(vpc_id, web_sg_id)

print("\n=== STEP 3: RDS MySQL ===")
db_endpoint = create_rds(priv_subnet_ids, db_sg_id)

    print("\n=== STEP 4: EC2 Web Server ===")
    instance = launch_ec2(pub_subnet_id, web_sg_id, db_endpoint)

    print("\n✅ DEPLOYMENT COMPLETE!")
    print(f"   App URL: http://{instance.public_ip_address}:5000")
    print(f"   Health:  http://{instance.public_ip_address}:5000/health")


if __name__ == '__main__':
    main()
