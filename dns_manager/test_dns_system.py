import os
import time
import psycopg2
import requests
import dns.resolver
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class DNSSystemTester:
    def __init__(self):
        self.db_conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'dns_manager'),
            user=os.getenv('DB_USER', 'dnsadmin'),
            password=os.getenv('DB_PASSWORD'),
            port=5432
        )
        self.npm_url = os.getenv('NPM_API_URL', 'http://localhost:81')
        self.npm_email = os.getenv('NPM_EMAIL')
        self.npm_password = os.getenv('NPM_PASSWORD')
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
        resolver.nameservers = ['127.0.0.1']
        resolver.port = 1053

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
        test_ip = "192.168.1.100"

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
