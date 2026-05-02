"""
Load Test Script
Tests the purchase API with 100 concurrent requests to verify concurrency handling
"""
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:8000/api"
PURCHASE_ENDPOINT = f"{BASE_URL}/purchase/"

# Shared results storage
results = {
    'successful': 0,
    'failed': 0,
    'errors': [],
    'start_time': None,
    'end_time': None
}

def purchase_request(product_id=1, quantity=1):
    """Make a single purchase request"""
    try:
        response = requests.post(
            PURCHASE_ENDPOINT,
            json={'product_id': product_id, 'quantity': quantity},
            timeout=10
        )
        
        if response.status_code == 200:
            results['successful'] += 1
            return {
                'status': 'success',
                'data': response.json()
            }
        elif response.status_code == 409:  # Insufficient stock
            results['failed'] += 1
            return {
                'status': 'conflict',
                'data': response.json()
            }
        else:
            results['failed'] += 1
            results['errors'].append(response.text)
            return {
                'status': 'error',
                'code': response.status_code
            }
    except Exception as e:
        results['failed'] += 1
        results['errors'].append(str(e))
        return {
            'status': 'exception',
            'error': str(e)
        }


def run_concurrent_test(num_requests=100, product_id=1, quantity=1):
    """Run concurrent purchase requests"""
    print(f"\n=== Starting Concurrent Load Test ===")
    print(f"Requests: {num_requests}")
    print(f"Product ID: {product_id}")
    print(f"Quantity per request: {quantity}")
    print(f"Total units requested: {num_requests * quantity}")
    
    results['start_time'] = time.time()
    
    # Use ThreadPoolExecutor for concurrent requests
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [
            executor.submit(purchase_request, product_id, quantity)
            for _ in range(num_requests)
        ]
        
        # Track completion
        completed = 0
        for future in as_completed(futures):
            completed += 1
            if completed % 20 == 0:
                print(f"Completed: {completed}/{num_requests}")
            result = future.result()
    
    results['end_time'] = time.time()
    
    # Print results
    print(f"\n=== Load Test Results ===")
    print(f"Successful purchases: {results['successful']}")
    print(f"Failed purchases: {results['failed']}")
    print(f"Total requests: {results['successful'] + results['failed']}")
    print(f"Success rate: {results['successful'] / num_requests * 100:.2f}%")
    print(f"Duration: {results['end_time'] - results['start_time']:.2f}s")
    print(f"RPS: {num_requests / (results['end_time'] - results['start_time']):.2f}")
    
    if results['errors']:
        print(f"\nErrors encountered ({len(results['errors'])}): ")
        for error in results['errors'][:5]:  # Show first 5 errors
            print(f"  - {error}")


if __name__ == '__main__':
    print("Make sure Django server is running on http://localhost:8000")
    input("Press Enter to start the test...")
    
    # Test 1: 100 concurrent requests to purchase
    run_concurrent_test(num_requests=100, product_id=1, quantity=1)
