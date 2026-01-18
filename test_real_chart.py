from aff import *
import sys

def test_real_chart():
    input_file = "real.aff"
    
    # 1. Load from file
    print(f"Loading {input_file}...")
    chart = AffChart.from_file(input_file)
    print(f"Loaded {len(chart.notes)} notes.")
    
    # 2. Serialize to string
    serialized_1 = chart.serialize()
    
    # 3. Load from the serialized string
    chart_2 = AffChart.from_string(serialized_1)
    
    # 4. Serialize again
    serialized_2 = chart_2.serialize()
    
    # 5. Compare
    if serialized_1 == serialized_2:
        print("Success: Round-trip serialization matches!")
    else:
        print("Failure: Round-trip serialization does not match!")
        
        # Find the first difference
        lines1 = serialized_1.splitlines()
        lines2 = serialized_2.splitlines()
        
        for i, (l1, l2) in enumerate(zip(lines1, lines2)):
            if l1 != l2:
                print(f"First difference at line {i+1}:")
                print(f"Original: {l1}")
                print(f"New:      {l2}")
                break
        else:
            if len(lines1) != len(lines2):
                print(f"Line count difference: {len(lines1)} vs {len(lines2)}")
        
        sys.exit(1)

if __name__ == "__main__":
    test_real_chart()
