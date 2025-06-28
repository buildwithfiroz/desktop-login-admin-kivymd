import subprocess
import time

TARGET_GATEWAY = "192.168.1.1"  # Replace this with your network's gateway IP


def get_gateway_ip():
    """Retrieve the current network's gateway IP on macOS."""
    try:
        result = subprocess.run(
            ["route", "-n", "get", "default"], capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if "gateway" in line:
                return line.split(":")[1].strip()
    except Exception as e:
        print(f"Error fetching gateway IP: {e}")
    return None


def main():
    while True:
        gateway_ip = get_gateway_ip()
        if gateway_ip == TARGET_GATEWAY:
            print(
                f"Connected to target network with gateway {TARGET_GATEWAY}. Running the Python app..."
            )
            # os.system("python3 /path/to/your_app.py")  # Replace with your app's path
            print("Les goo")
            time.sleep(6)  # Wait to prevent repeated runs
        else:
            print(f"Not connected to the target network. Current gateway: {gateway_ip}")
        time.sleep(5)


if __name__ == "__main__":
    main()
