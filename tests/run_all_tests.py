#!/usr/bin/env python3
import pytest
import sys
import os

def run_all_tests():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    test_files = [
        "test_lections.py", "test_records.py", "test_teachers.py", "test_students.py", "test_problem_marks.py", "test_metaphors.py", "test_crud_operations.py", "test_performance.py", "test_accessibility.py"
    ]
    
    results = {}
    all_passed = True
    
    for test_file in test_files:
        test_path = os.path.join(current_dir, test_file)
        if os.path.exists(test_path):
            exit_code = pytest.main(["-v", test_path])
            results[test_file] = exit_code == 0
            if exit_code != 0:
                all_passed = False
        else:
            print(f"Файл не найден: {test_file}")
            results[test_file] = False
            all_passed = False
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(run_all_tests())