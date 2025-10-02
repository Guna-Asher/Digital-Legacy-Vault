CREATE DATABASE IF NOT EXISTS legacy_vault;
USE legacy_vault;

-- Users table with temporal tables for audit
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) WITH SYSTEM VERSIONING;

-- Digital assets table with JSON for flexible metadata
CREATE TABLE digital_assets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    owner_id INT NOT NULL,
    asset_type ENUM('crypto_wallet', 'social_media', 'cloud_storage', 'documents', 'other') NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    access_instructions JSON,
    metadata JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
) WITH SYSTEM VERSIONING;

-- Beneficiaries table with multi-signature support
CREATE TABLE beneficiaries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_id INT NOT NULL,
    user_id INT NOT NULL,
    share_percentage DECIMAL(5,2) NOT NULL,
    approval_required BOOLEAN DEFAULT FALSE,
    has_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES digital_assets(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE KEY unique_asset_beneficiary (asset_id, user_id)
) WITH SYSTEM VERSIONING;

-- Death verification events with multi-signature workflow
CREATE TABLE death_verification_events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    status ENUM('pending', 'verified', 'rejected', 'requires_more_evidence') NOT NULL,
    verification_type ENUM('death_certificate', 'multiple_witnesses', 'legal_document') NOT NULL,
    evidence_data JSON,
    required_approvals INT DEFAULT 1,
    current_approvals INT DEFAULT 0,
    initiated_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (initiated_by) REFERENCES users(id)
) WITH SYSTEM VERSIONING;

-- Multi-signature approvals table
CREATE TABLE multisig_approvals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    approver_id INT NOT NULL,
    approval_status ENUM('approved', 'rejected', 'pending') DEFAULT 'pending',
    comments TEXT,
    approved_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES death_verification_events(id),
    FOREIGN KEY (approver_id) REFERENCES users(id),
    UNIQUE KEY unique_event_approver (event_id, approver_id)
) WITH SYSTEM VERSIONING;

-- Asset transfer log for complete audit trail
CREATE TABLE asset_transfers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_id INT NOT NULL,
    from_user_id INT NOT NULL,
    to_user_id INT NOT NULL,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transfer_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    death_event_id INT NOT NULL,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES digital_assets(id),
    FOREIGN KEY (from_user_id) REFERENCES users(id),
    FOREIGN KEY (to_user_id) REFERENCES users(id),
    FOREIGN KEY (death_event_id) REFERENCES death_verification_events(id)
) WITH SYSTEM VERSIONING;

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_assets_owner ON digital_assets(owner_id);
CREATE INDEX idx_beneficiaries_asset ON beneficiaries(asset_id);
CREATE INDEX idx_death_events_user ON death_verification_events(user_id);
CREATE INDEX idx_transfers_asset ON asset_transfers(asset_id);