import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def wait_for_api():
    """Wait for the API to be ready"""
    print("⏳ Waiting for API to be ready...")
    max_retries = 12
    for i in range(max_retries):
        try:
            resp = requests.get(f"{BASE_URL}/")
            if resp.status_code == 200:
                print("✅ API is ready!")
                return True
        except requests.exceptions.ConnectionError:
            if i < max_retries - 1:
                print(f"   Attempt {i+1}/{max_retries}...")
                time.sleep(5)
            else:
                print("❌ API not responding after multiple attempts.")
                print("   Please check if Docker containers are running with: docker-compose ps")
                return False
    return False

def demo_workflow():
    print("\n" + "="*60)
    print("🚀 DIGITAL LEGACY VAULT - DEMO WORKFLOW")
    print("="*60)
    
    # 1. Create users
    print("\n1. 📝 CREATING USERS")
    print("-" * 30)
    
    users = [
        {
            "email": "john@example.com",
            "password": "password123",
            "full_name": "John Doe",
            "date_of_birth": "1980-01-15"
        },
        {
            "email": "jane@example.com", 
            "password": "password123",
            "full_name": "Jane Smith",
            "date_of_birth": "1985-05-20"
        },
        {
            "email": "bob@example.com",
            "password": "password123", 
            "full_name": "Bob Wilson",
            "date_of_birth": "1975-11-30"
        }
    ]
    
    tokens = {}
    user_ids = {}
    
    for user_data in users:
        try:
            # Register users
            resp = requests.post(f"{BASE_URL}/auth/register", json=user_data)
            if resp.status_code == 200:
                print(f"   ✅ Registered: {user_data['email']}")
            else:
                print(f"   ⚠ User might already exist: {user_data['email']}")
            
            # Login
            resp = requests.post(f"{BASE_URL}/auth/login", json={
                "email": user_data["email"],
                "password": user_data["password"]
            })
            if resp.status_code == 200:
                token = resp.json()["access_token"]
                tokens[user_data["email"]] = token
                
                # Get user ID
                headers = {"Authorization": f"Bearer {token}"}
                resp_user = requests.get(f"{BASE_URL}/users/me", headers=headers)
                if resp_user.status_code == 200:
                    user_info = resp_user.json()
                    user_ids[user_data["email"]] = user_info["id"]
                    print(f"   ✅ Logged in: {user_data['email']} (ID: {user_info['id']})")
                else:
                    print(f"   ❌ Failed to get user info for {user_data['email']}")
            else:
                print(f"   ❌ Failed to login: {user_data['email']}")
                
        except Exception as e:
            print(f"   ❌ Error with {user_data['email']}: {e}")
    
    if not tokens:
        print("❌ No users were created successfully. Exiting demo.")
        return
    
    print("\n2. 💼 JOHN CREATING DIGITAL ASSETS")
    print("-" * 40)
    
    # 2. John creates digital assets
    headers_john = {"Authorization": f"Bearer {tokens['john@example.com']}"}
    
    assets = [
        {
            "asset_type": "crypto_wallet",
            "name": "Bitcoin Wallet",
            "description": "Main Bitcoin cold wallet",
            "access_instructions": {
                "wallet_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                "recovery_phrase": "encrypted_phrase_here",
                "private_key": "encrypted_key_here"
            },
            "metadata": {
                "currency": "BTC",
                "estimated_value": 50000
            }
        },
        {
            "asset_type": "social_media",
            "name": "Twitter Account",
            "description": "Personal Twitter account",
            "access_instructions": {
                "username": "@johndoe",
                "password": "encrypted_password",
                "backup_codes": "encrypted_codes"
            },
            "metadata": {
                "platform": "twitter",
                "followers": 1500
            }
        }
    ]
    
    created_assets = []
    for asset_data in assets:
        resp = requests.post(f"{BASE_URL}/assets", json=asset_data, headers=headers_john)
        if resp.status_code == 200:
            asset = resp.json()
            created_assets.append(asset)
            print(f"   ✅ Created asset: {asset_data['name']} (ID: {asset['id']})")
        else:
            print(f"   ❌ Failed to create asset: {asset_data['name']}")
            print(f"      Error: {resp.text}")
    
    if not created_assets:
        print("   ❌ No assets created. Exiting demo.")
        return
    
    # 3. John adds beneficiaries to Bitcoin wallet
    print("\n3. 👥 ADDING BENEFICIARIES TO BITCOIN WALLET")
    print("-" * 50)
    
    bitcoin_asset_id = created_assets[0]["id"]
    
    beneficiaries = [
        {
            "user_id": user_ids["jane@example.com"],
            "share_percentage": 60.0,
            "approval_required": True
        },
        {
            "user_id": user_ids["bob@example.com"], 
            "share_percentage": 40.0,
            "approval_required": True
        }
    ]
    
    for beneficiary_data in beneficiaries:
        resp = requests.post(
            f"{BASE_URL}/assets/{bitcoin_asset_id}/beneficiaries", 
            json=beneficiary_data, 
            headers=headers_john
        )
        if resp.status_code == 200:
            beneficiary = resp.json()
            email = [email for email, uid in user_ids.items() if uid == beneficiary_data["user_id"]][0]
            print(f"   ✅ Added beneficiary: {email} ({beneficiary_data['share_percentage']}%)")
        else:
            print(f"   ❌ Failed to add beneficiary for user {beneficiary_data['user_id']}")
            print(f"      Error: {resp.text}")
    
    # 4. Simulate death verification (initiated by Jane)
    print("\n4. 📋 JANE INITIATING DEATH VERIFICATION FOR JOHN")
    print("-" * 55)
    
    headers_jane = {"Authorization": f"Bearer {tokens['jane@example.com']}"}
    
    death_event = {
        "user_id": user_ids["john@example.com"],
        "verification_type": "death_certificate", 
        "evidence_data": {
            "certificate_number": "DC-2024-001",
            "issue_date": "2024-01-15",
            "issuing_authority": "City Hospital",
            "document_hash": "abc123encrypted"
        },
        "required_approvals": 2
    }
    
    resp = requests.post(f"{BASE_URL}/death-verifications", json=death_event, headers=headers_jane)
    if resp.status_code == 200:
        death_event_info = resp.json()
        death_event_id = death_event_info["id"]
        print(f"   ✅ Created death verification event: ID {death_event_id}")
        print(f"   📊 Status: {death_event_info['status']}")
        print(f"   👥 Required approvals: {death_event_info['required_approvals']}")
    else:
        print("   ❌ Failed to create death verification event")
        print(f"      Error: {resp.text}")
        return
    
    # 5. Multi-signature approvals
    print("\n5. 🔐 MULTI-SIGNATURE APPROVAL PROCESS")
    print("-" * 40)
    
    # Jane approves
    approval_data = {
        "approval_status": "approved",
        "comments": "I confirm John's passing as his sister"
    }
    resp = requests.post(
        f"{BASE_URL}/death-verifications/{death_event_id}/approvals",
        json=approval_data,
        headers=headers_jane
    )
    if resp.status_code == 200:
        approval = resp.json()
        print(f"   ✅ Jane approved the death verification")
        print(f"   📊 Current approvals: 1/{death_event_info['required_approvals']}")
    else:
        print("   ❌ Jane failed to approve")
        print(f"      Error: {resp.text}")
    
    # Bob approves  
    headers_bob = {"Authorization": f"Bearer {tokens['bob@example.com']}"}
    approval_data["comments"] = "I confirm John's passing as his brother"
    resp = requests.post(
        f"{BASE_URL}/death-verifications/{death_event_id}/approvals", 
        json=approval_data,
        headers=headers_bob
    )
    if resp.status_code == 200:
        approval = resp.json()
        print(f"   ✅ Bob approved the death verification")
        print(f"   📊 Current approvals: 2/{death_event_info['required_approvals']}")
        
        # Check updated event status
        resp_event = requests.get(f"{BASE_URL}/death-verifications/{death_event_id}", headers=headers_jane)
        if resp_event.status_code == 200:
            updated_event = resp_event.json()
            print(f"   📊 Event status: {updated_event['status']}")
        else:
            print("   ⚠ Could not fetch updated event status")
    else:
        print("   ❌ Bob failed to approve")
        print(f"      Error: {resp.text}")
    
    # 6. Check asset transfers
    print("\n6. 🔄 CHECKING ASSET TRANSFERS")
    print("-" * 30)
    
    time.sleep(2)  # Give time for transfers to process
    
    resp = requests.get(f"{BASE_URL}/transfers", headers=headers_jane)
    if resp.status_code == 200:
        transfers = resp.json()
        print(f"   ✅ Created {len(transfers)} asset transfers")
        
        for transfer in transfers:
            resp_asset = requests.get(f"{BASE_URL}/assets/{transfer['asset_id']}", headers=headers_jane)
            asset_name = "Unknown Asset"
            if resp_asset.status_code == 200:
                asset_info = resp_asset.json()
                asset_name = asset_info["name"]
            
            to_email = [email for email, uid in user_ids.items() if uid == transfer['to_user_id']][0]
            status_icon = "✅" if transfer['transfer_status'] == 'completed' else "⏳"
            print(f"   {status_icon} Transfer: {asset_name} to {to_email} ({transfer['transfer_status']})")
    else:
        print("   ❌ Failed to retrieve transfers")
        print(f"      Error: {resp.text}")
    
    # 7. Demo data overview
    print("\n7. 📊 DEMO DATA OVERVIEW")
    print("-" * 25)
    print("   👤 Users created:")
    for email, uid in user_ids.items():
        print(f"      - {email} (ID: {uid})")
    
    print(f"   💼 Assets created: {len(created_assets)}")
    print(f"   📋 Death verification events: 1")
    print(f"   🔄 Asset transfers: {len(transfers) if 'transfers' in locals() else 0}")
    
    print("\n" + "="*60)
    print("🎉 DEMO COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📖 Next steps:")
    print("   1. Access API documentation: http://localhost:8000/docs")
    print("   2. Use the tokens above to authenticate in Swagger UI")
    print("   3. Explore the database: docker-compose exec db mysql -u user -ppassword legacy_vault")
    print("   4. Check container status: docker-compose ps")
    print("\n💡 Tip: Run 'docker-compose down' to stop the services when done")

if __name__ == "__main__":
    if not wait_for_api():
        sys.exit(1)
    
    try:
        demo_workflow()
    except KeyboardInterrupt:
        print("\n\n⚠ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        print("💡 Check if all services are running properly")