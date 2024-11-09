import os
import time
import schedule
import psycopg2
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DNSManager:
    def __init__(self):
        self.db_conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        self.npm_url = os.environ['NPM_API_URL']
        self.npm_email = os.environ['NPM_EMAIL']
        self.npm_password = os.environ['NPM_PASSWORD']
        self.npm_token = None
        
        # Set paths based on environment
        self.is_production = os.getenv('ENV', 'development') == 'production'
        if self.is_production:
            self.zones_path = '/var/lib/bind'
            self.bind_config_path = '/etc/bind/zones.conf'
        else:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.zones_path = os.path.join(project_root, 'bind', 'zones')
            self.bind_config_path = os.path.join(project_root, 'bind', 'config', 'zones.conf')
            
        os.makedirs(os.path.dirname(self.bind_config_path), exist_ok=True)
        os.makedirs(self.zones_path, exist_ok=True)
        
        logger.info(f"DNS Manager initialized in {'production' if self.is_production else 'development'} mode")

    def login_to_npm(self):
        response = requests.post(f"{self.npm_url}/api/tokens", json={
            "identity": self.npm_email,
            "secret": self.npm_password
        })
        if (response.status_code == 200):
            self.npm_token = response.json()['token']

    def create_zone_file(self, domain, records):
        zone_content = f"""$TTL 86400
@       IN      SOA     ns1.{domain}. admin.{domain}. (
                        {int(datetime.now().timestamp())}
                        3600
                        1800
                        604800
                        86400 )

        IN      NS      ns1.{domain}.
        IN      A       {records['main_ip']}
"""
        zone_file = os.path.join(self.zones_path, f"{domain}.zone")
        try:
            with open(zone_file, 'w') as f:
                f.write(zone_content)
            logger.info(f"Created zone file for {domain}")
        except Exception as e:
            logger.error(f"Failed to create zone file for {domain}: {str(e)}")
            raise

    def update_bind_config(self, domain):
        try:
            os.makedirs(os.path.dirname(self.bind_config_path), exist_ok=True)
            with open(self.bind_config_path, 'a') as f:
                f.write(f"""
zone "{domain}" {{
    type master;
    file "{os.path.join(self.zones_path, f'{domain}.zone')}";
}};
""")
            logger.info(f"Updated BIND config for {domain}")
        except Exception as e:
            logger.error(f"Failed to update BIND config: {str(e)}")
            raise

    def create_ssl_cert(self, domain):
        if not self.npm_token:
            self.login_to_npm()
        
        headers = {'Authorization': f'Bearer {self.npm_token}'}
        data = {
            "domain_names": [domain],
            "force_ssl": True,
            "http2_support": True,
            "forward_scheme": "http",
            "forward_host": "shopify-app",
            "forward_port": 80
        }
        
        response = requests.post(
            f"{self.npm_url}/api/nginx/proxy", 
            headers=headers,
            json=data
        )
        return response.status_code == 201

    def check_new_domains(self):
        try:
            cur = self.db_conn.cursor()
            logger.info("Checking for new domains...")
            cur.execute("""
                SELECT domain, ip_address 
                FROM domains 
                WHERE is_processed = FALSE
            """)
            
            for domain, ip in cur.fetchall():
                records = {'main_ip': ip}
                self.create_zone_file(domain, records)
                self.update_bind_config(domain)
                self.create_ssl_cert(domain)
                
                cur.execute("""
                    UPDATE domains 
                    SET is_processed = TRUE 
                    WHERE domain = %s
                """, (domain,))
                
            self.db_conn.commit()
        except Exception as e:
            logger.error(f"Error processing domains: {str(e)}")
            raise
        finally:
            if 'cur' in locals():
                cur.close()

def main():
    dns_manager = DNSManager()
    schedule.every(10).minutes.do(dns_manager.check_new_domains)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
