import os
import json
import tempfile
from transformers import GenerationConfig

def verify_fix():
    print("--- Starting Verification for Issue #31435 ---")
    
    # 1. Create a dummy generation_config.json
    config_data = {
        "do_sample": True,
        "temperature": 0.7,
        "max_length": 50,
        "transformers_version": "4.42.0"
    }
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = os.path.join(tmp_dir, "custom_config.json")
        with open(config_path, "w") as f:
            json.dump(config_data, f)
        
        print(f"Created local config file at: {config_path}")
        
        # 2. Attempt to load using the direct file path
        # Before the fix, this would likely fail or try to look it up on the Hub
        try:
            print(f"Attempting to load GenerationConfig from: {config_path}")
            config = GenerationConfig.from_pretrained(config_path)
            
            # 3. Verify attributes
            assert config.do_sample is True
            assert config.temperature == 0.7
            assert config.max_length == 50
            
            print("SUCCESS: GenerationConfig successfully loaded from direct file path.")
            print(f"Loaded config: {config}")
            return True
            
        except Exception as e:
            print(f"FAILED: Could not load GenerationConfig from direct file path.")
            print(f"Error: {e}")
            return False

if __name__ == "__main__":
    success = verify_fix()
    if not success:
        exit(1)
