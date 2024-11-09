import os
from unittest.mock import MagicMock, patch
from manager import DNSManager

class TestEnvironment:
    def __init__(self):
        # Use permanent project directories
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.zones_dir = os.path.join(self.project_root, 'bind', 'zones')
        self.config_dir = os.path.join(self.project_root, 'bind', 'config')
        
        # Create directories if they don't exist
        os.makedirs(self.zones_dir, exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)
        
        self.mock_db_data = [
            ("example.com", "192.168.1.100"),
            ("test.com", "192.168.1.101")
        ]

    def setup_mocks(self):
        # Mock database connection
        db_mock = MagicMock()
        cursor_mock = MagicMock()
        cursor_mock.fetchall.return_value = self.mock_db_data
        db_mock.cursor.return_value = cursor_mock

        # Mock environment variables
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_NAME'] = 'test_db'
        os.environ['DB_USER'] = 'test_user'
        os.environ['DB_PASSWORD'] = 'test_pass'
        os.environ['NPM_API_URL'] = 'http://localhost:81'
        os.environ['NPM_EMAIL'] = 'test@example.com'
        os.environ['NPM_PASSWORD'] = 'test_password'

        return db_mock

    def run_test(self):
        print("Starting DNS Manager test...")
        print(f"Using project directories:")
        print(f"Zones: {self.zones_dir}")
        print(f"Config: {self.config_dir}")
        
        db_mock = self.setup_mocks()
        
        with patch('psycopg2.connect', return_value=db_mock):
            dns_manager = DNSManager()
            dns_manager.zones_path = self.zones_dir
            dns_manager.bind_config_path = os.path.join(self.config_dir, 'zones.conf')
            
            print("\nTesting domain processing...")
            dns_manager.check_new_domains()
        
        # Verify both zone files and config
        print("\nChecking generated zone files:")
        self._check_zone_files()
        
        print("\nChecking BIND config file:")
        config_file = os.path.join(self.config_dir, 'zones.conf')
        if os.path.exists(config_file):
            print(f"✓ BIND config file created")
            with open(config_file, 'r') as f:
                content = f.read()
            print(f"Config preview:\n{content[:200]}...")
        else:
            print("✗ BIND config file missing")

    def _check_zone_files(self):
        for domain, ip in self.mock_db_data:
            zone_file = os.path.join(self.zones_dir, f"{domain}.zone")
            if os.path.exists(zone_file):
                print(f"✓ Zone file created for {domain}")
                with open(zone_file, 'r') as f:
                    content = f.read()
                print(f"Content preview:\n{content[:200]}...")
            else:
                print(f"✗ Zone file missing for {domain}")

if __name__ == "__main__":
    test_env = TestEnvironment()
    test_env.run_test()
