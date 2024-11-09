CREATE TABLE domains (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) NOT NULL UNIQUE,
    ip_address VARCHAR(45) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    ssl_status VARCHAR(50) DEFAULT 'pending'
);

CREATE INDEX idx_unprocessed_domains ON domains (is_processed)
WHERE
    NOT is_processed;