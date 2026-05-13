import urllib.request
import json
import sys

# Replace with your EC2 IP after deploy — or read from a file
EC2_IP = open("/tmp/ec2_ip.txt").read().strip() if os.path.exists("/tmp/ec2_ip.txt") else "localhost"

try:
    url = f"http://{EC2_IP}:5000/health"
    res = urllib.request.urlopen(url, timeout=10)
    data = json.loads(res.read())
    print(f"Health check: {data}")
    if data.get("status") == "healthy":
        print("✅ App and DB are connected!")
        sys.exit(0)
    else:
        print("❌ DB not reachable")
        sys.exit(1)
except Exception as e:
    print(f"❌ Could not reach app: {e}")
    sys.exit(1)
