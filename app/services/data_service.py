import pandas as pd
import os
import uuid
import json
from datetime import datetime
from config.settings import Config

HISTORY_FILE = os.path.join(Config.DATA_DIR, 'generation_history.csv')

def save_generation_record(prompt_type, inputs, output):
    """Saves a content generation record to CSV using Pandas."""
    record_id = f"gen_{uuid.uuid4().hex[:8]}"
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    new_record = {
        'id': record_id,
        'timestamp': timestamp,
        'type': prompt_type,
        'inputs_json': json.dumps(inputs),
        'output': output
    }
    
    # Using Pandas to handle the new row
    df_new = pd.DataFrame([new_record])
    
    if os.path.exists(HISTORY_FILE):
        df_new.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
    else:
        df_new.to_csv(HISTORY_FILE, mode='w', header=True, index=False)
        
    return {
        'id': record_id,
        'type': prompt_type,
        'timestamp': timestamp,
        'output': output
    }

def get_history(limit=10):
    """Retrieves history records from CSV."""
    if not os.path.exists(HISTORY_FILE):
        return []
        
    try:
        df = pd.read_csv(HISTORY_FILE)
        
        # Sort by timestamp descending
        df = df.sort_values(by='timestamp', ascending=False)
        
        # Limit rows
        df_limit = df.head(limit)
        
        # Convert to dictionary format
        records = df_limit.to_dict(orient='records')
        
        # Unpack JSON strings back to python dicts
        for record in records:
            if 'inputs_json' in record and isinstance(record['inputs_json'], str):
                try:
                    record['inputs'] = json.loads(record['inputs_json'])
                except Exception:
                    record['inputs'] = record['inputs_json']
                del record['inputs_json']
                
        return records
    except pd.errors.EmptyDataError:
        return []
    except Exception as e:
        print(f"Error reading history: {e}")
        return []
