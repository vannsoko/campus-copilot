import os
import datetime

from auth.session import AnnySession
from booking_client import BookingClient

def main():
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    
    if not username or not password:
        print("❌ Missing USERNAME or PASSWORD in .env")
        return False

    target_date_str = os.getenv("CANCEL_DATE")
    if not target_date_str:
        print("❌ Missing CANCEL_DATE in .env")
        return False

    session = AnnySession(username, password, provider_name="tum")
    cookies = session.login()

    if not cookies:
        print("❌ Login failed")
        return False

    booking = BookingClient(cookies, customer_account_id=session.customer_account_id)
    
    print(f"ℹ️ Fetching active bookings to find reservation on {target_date_str}...")
    active_bookings = booking.get_active_bookings()
    
    found = False
    for b in active_bookings:
        start_date = b.get('attributes', {}).get('start_date')
        status = b.get('attributes', {}).get('status')
        
        if start_date and status in ["accepted", "pending"]:
            if start_date.startswith(target_date_str):
                found = True
                booking_id = b.get('id')
                print(f"ℹ️ Found matching active booking {booking_id} for {start_date}")
                booking.cancel_booking(booking_id)
                
    if not found:
        print(f"⚠️ No active booking found for date {target_date_str}")

if __name__ == "__main__":
    main()
