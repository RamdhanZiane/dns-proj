import os
import time
import psycopg2
import requests
import dns.resolver
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default configuration - matches docker-compose.yml
DEFAULT_CONFIG = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'dns_manager',
    'DB_USER': 'dnsadmin',
    'DB_PASSWORD': 'your_secure_password',  # Should match value in .env
    'NPM_API_URL': 'http://localhost:81',
    'NPM_EMAIL': 'admin@example.com',
    'NPM_PASSWORD': 'your_npm_password'
}

class DNSSystemTester:
    def __init__(self):
        # Use environment variables with fallback to defaults
        self.config = {
            key: os.getenv(key, DEFAULT_CONFIG[key])
            for key in DEFAULT_CONFIG
        }
        
        print("\n🔧 Testing with configuration:")
        print(f"DB_HOST: {self.config['DB_HOST']}")
        print(f"DB_NAME: {self.config['DB_NAME']}")
        print(f"DB_USER: {self.config['DB_USER']}")
        
        try:
            self.db_conn = psycopg2.connect(
                host=self.config['DB_HOST'],
                database=self.config['DB_NAME'],
                user=self.config['DB_USER'],
                password=self.config['DB_PASSWORD'],
                port=5432
            )
            print("✅ Database connection successful")
        except psycopg2.Error as e:
            print(f"❌ Database connection failed: {str(e)}")
            print("\n🔍 Troubleshooting tips:")
            print("1. Check if PostgreSQL is running:")
            print("   docker ps | grep postgres")
            print("2. Verify credentials in .env file")
            print("3. Ensure database is initialized:")
            print("   docker-compose exec postgres psql -U dnsadmin -d dns_manager")
            raise

        self.npm_url = self.config['NPM_API_URL']
        self.npm_email = self.config['NPM_EMAIL']
        self.npm_password = self.config['NPM_PASSWORD']
        self.npm_token = None

    def add_test_domain(self, domain, ip_address):
        print(f"\n🔍 Adding test domain: {domain}")
        cur = self.db_conn.cursor()
        try:
            cur.execute("""
                INSERT INTO domains (domain, ip_address)
                VALUES (%s, %s)
                RETURNING id
            """, (domain, ip_address))
            domain_id = cur.fetchone()[0]
            self.db_conn.commit()
            print(f"✅ Domain added successfully with ID: {domain_id}")
            return domain_id
        except Exception as e:
            self.db_conn.rollback()
            print(f"❌ Error adding domain: {str(e)}")
            raise
        finally:
            cur.close()

    def wait_for_processing(self, domain, timeout=300):
        print(f"\n⏳ Waiting for domain processing: {domain}")
        start_time = time.time()
        while time.time() - start_time < timeout:
            cur = self.db_conn.cursor()
            cur.execute("""
                SELECT is_processed, ssl_status
                FROM domains
                WHERE domain = %s
            """, (domain,))
            result = cur.fetchone()
            cur.close()

            if result and result[0]:
                print(f"✅ Domain processed. SSL Status: {result[1]}")
                return True
            
            time.sleep(5)
            print(".", end="", flush=True)

        print(f"\n❌ Timeout waiting for domain processing")
        return False

    def verify_dns_records(self, domain):
        print(f"\n🔍 Verifying DNS records for: {domain}")
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['10.142.0.2']
        resolver.port = 53

        try:
            answers = resolver.resolve(domain, 'A')
            print(f"✅ DNS A record found: {[str(rdata) for rdata in answers]}")
            return True
        except Exception as e:
            print(f"❌ DNS lookup failed: {str(e)}")
            return False

    def check_ssl_certificate(self, domain):
        print(f"\n🔒 Checking SSL certificate for: {domain}")
        try:
            response = requests.get(f"https://{domain}", verify=False)
            print(f"✅ HTTPS connection successful: {response.status_code}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ HTTPS connection failed: {str(e)}")
            return False

    def run_tests(self):
        test_domain = f"test-{int(datetime.now().timestamp())}.example.com"
        test_ip = "127.0.0.1"

        try:
            # Test 1: Add domain
            domain_id = self.add_test_domain(test_domain, test_ip)

            # Test 2: Wait for processing
            if self.wait_for_processing(test_domain):
                # Test 3: Verify DNS
                dns_ok = self.verify_dns_records(test_domain)
                
                # Test 4: Check SSL
                ssl_ok = self.check_ssl_certificate(test_domain)

                if dns_ok and ssl_ok:
                    print("\n✅ All tests passed successfully!")
                else:
                    print("\n⚠️ Some tests failed")
            else:
                print("\n❌ Domain processing failed")

        except Exception as e:
            print(f"\n❌ Test failed with error: {str(e)}")
        finally:
            self.db_conn.close()

if __name__ == "__main__":
    tester = DNSSystemTester()
    tester.run_tests()
