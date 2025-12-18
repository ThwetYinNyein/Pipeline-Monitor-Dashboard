"""
Test script to verify pipeline initialization and logging works correctly
"""
import os
import sys
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from bootstrap import init_pipeline

def test_pipeline_init():
    """Test pipeline initialization"""
    print("=" * 60)
    print("Testing Pipeline Initialization")
    print("=" * 60)
    
    try:
        # Test 1: Initialize a test pipeline
        print("\n[Test 1] Initializing test pipeline...")
        logger, base_dir, log_dir = init_pipeline("test_pipeline")
        
        print(f"[OK] Base directory: {base_dir}")
        print(f"[OK] Log directory: {log_dir}")
        
        # Test 2: Write some log messages
        print("\n[Test 2] Writing log messages...")
        logger.info("This is an INFO message")
        logger.warning("This is a WARNING message")
        logger.error("This is an ERROR message")
        print("[OK] Log messages written successfully")
        
        # Test 3: Verify log file exists
        print("\n[Test 3] Verifying log file creation...")
        if os.path.exists(log_dir):
            log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
            if log_files:
                print(f"[OK] Log file created: {log_files[0]}")
                log_file_path = os.path.join(log_dir, log_files[0])
                print(f"[OK] Full path: {log_file_path}")
                
                # Read and display log contents
                print("\n[Test 4] Log file contents:")
                print("-" * 60)
                with open(log_file_path, 'r', encoding='utf-8') as f:
                    print(f.read())
                print("-" * 60)
            else:
                print("[FAIL] No log files found")
                return False
        else:
            print("[FAIL] Log directory not created")
            return False
        
        print("\n" + "=" * 60)
        print("[OK] ALL TESTS PASSED!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pipeline_categories():
    """Test that each pipeline category can initialize properly"""
    print("\n" + "=" * 60)
    print("Testing Pipeline Categories")
    print("=" * 60)
    
    categories = {
        "ayapay": "test_ayapay_pipeline",
        "mbx": "test_mbx_pipeline",
        "milestone": "test_milestone_pipeline"
    }
    
    results = {}
    
    for category, pipeline_name in categories.items():
        print(f"\n[Testing {category}] Initializing {pipeline_name}...")
        try:
            logger, base_dir, log_dir = init_pipeline(pipeline_name)
            logger.info(f"Test log entry for {category} category")
            
            # Verify log file
            if os.path.exists(log_dir):
                log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
                if log_files:
                    print(f"[OK] {category}: Log created at {log_dir}")
                    results[category] = True
                else:
                    print(f"[FAIL] {category}: No log file created")
                    results[category] = False
            else:
                print(f"[FAIL] {category}: Log directory not created")
                results[category] = False
                
        except Exception as e:
            print(f"[FAIL] {category}: Failed - {e}")
            results[category] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("Category Test Summary:")
    print("=" * 60)
    for category, success in results.items():
        status = "[PASS]" if success else "[FAIL]"
        print(f"{category:20s} : {status}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n[OK] ALL CATEGORY TESTS PASSED!")
    else:
        print("\n[FAIL] SOME CATEGORY TESTS FAILED")
    
    return all_passed

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TERMINUS PIPELINE TEST SUITE")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 60)
    
    # Run tests
    test1_passed = test_pipeline_init()
    test2_passed = test_pipeline_categories()
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL TEST SUMMARY")
    print("=" * 60)
    print(f"Basic Initialization Test: {'[PASS]' if test1_passed else '[FAIL]'}")
    print(f"Category Tests:            {'[PASS]' if test2_passed else '[FAIL]'}")
    
    if test1_passed and test2_passed:
        print("\n[SUCCESS] ALL TESTS PASSED - System is ready for production!")
        sys.exit(0)
    else:
        print("\n[WARNING] SOME TESTS FAILED - Please review errors above")
        sys.exit(1)

