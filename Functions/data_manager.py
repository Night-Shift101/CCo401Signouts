import json
import os
import logging
from datetime import datetime
from pathlib import Path

class DataManager:

    def __init__(self, data_dir="data"):
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.current_signouts_file = self.data_dir / "current_signouts.json"
        self.logs_dir = self.data_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)

        self._initialize_signouts_file()

        self._setup_daily_logging()
    
    def _initialize_signouts_file(self):
        
        if not self.current_signouts_file.exists():
            initial_data = {
                "last_updated": datetime.now().isoformat(),
                "signouts": []
            }
            self._save_json(self.current_signouts_file, initial_data)
    
    def _setup_daily_logging(self):
        
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.logs_dir / f"signout_log_{today}.log"

        self.logger = logging.getLogger("SignoutSystem")
        self.logger.setLevel(logging.INFO)

        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

        self.logger.info("=== Soldier Sign-out System Started ===")
    
    def _save_json(self, file_path, data):
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save JSON file {file_path}: {e}")
            raise
    
    def _load_json(self, file_path):
        
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"Failed to load JSON file {file_path}: {e}")
            return {}
    
    def add_signout(self, signout_data):

        data = self._load_json(self.current_signouts_file)

        current_signouts = data.get('signouts', [])
        if current_signouts:
            max_id = max(int(entry.get('id', '0')) for entry in current_signouts)
            new_id = str(max_id + 1).zfill(3)
        else:
            new_id = "001"

        new_entry = {
            'id': new_id,
            'soldiers': signout_data['soldiers'],
            'destination': signout_data['destination'],
            'phone': signout_data['phone'],
            'datetime': signout_data['datetime'],
            'notes': signout_data.get('notes', ''),
            'created_at': datetime.now().isoformat()
        }

        current_signouts.append(new_entry)
        data['signouts'] = current_signouts
        data['last_updated'] = datetime.now().isoformat()

        self._save_json(self.current_signouts_file, data)

        soldiers_str = ", ".join(signout_data['soldiers'])
        self.logger.info(
            f"SIGN-OUT | ID: {new_id} | Soldiers: {soldiers_str} | "
            f"Destination: {signout_data['destination']} | Phone: {signout_data['phone']}"
        )
        
        return new_id
    
    def remove_signout(self, entry_id: str) -> bool:

        data = self._load_json(self.current_signouts_file)
        current_signouts = data.get('signouts', [])

        entry_to_remove = None
        for i, entry in enumerate(current_signouts):
            if entry['id'] == entry_id:
                entry_to_remove = current_signouts.pop(i)
                break
        
        if entry_to_remove:

            data['signouts'] = current_signouts
            data['last_updated'] = datetime.now().isoformat()
            self._save_json(self.current_signouts_file, data)

            soldiers_str = ", ".join(entry_to_remove['soldiers'])
            self.logger.info(
                f"SIGN-IN | ID: {entry_id} | Soldiers: {soldiers_str} | "
                f"Duration: {self._calculate_duration(entry_to_remove['datetime'])}"
            )
            
            return True
        
        self.logger.warning(f"Attempted to remove non-existent sign-out ID: {entry_id}")
        return False
    
    def get_current_signouts(self):
        
        data = self._load_json(self.current_signouts_file)
        return data.get('signouts', [])
    
    def get_signout_by_id(self, entry_id):
        
        current_signouts = self.get_current_signouts()
        for entry in current_signouts:
            if entry['id'] == entry_id:
                return entry
        return None
    
    def update_signout(self, entry_id, updated_data):

        data = self._load_json(self.current_signouts_file)
        current_signouts = data.get('signouts', [])

        for entry in current_signouts:
            if entry['id'] == entry_id:

                for key, value in updated_data.items():
                    if key != 'id':  # Don't allow ID changes
                        entry[key] = value
                
                entry['last_modified'] = datetime.now().isoformat()

                data['signouts'] = current_signouts
                data['last_updated'] = datetime.now().isoformat()
                self._save_json(self.current_signouts_file, data)

                soldiers_str = ", ".join(entry['soldiers'])
                self.logger.info(f"UPDATED | ID: {entry_id} | Soldiers: {soldiers_str}")
                
                return True
        
        self.logger.warning(f"Attempted to update non-existent sign-out ID: {entry_id}")
        return False
    
    def _calculate_duration(self, start_datetime: str) -> str:
        
        try:
            start = datetime.fromisoformat(start_datetime.replace('Z', '+00:00'))
            now = datetime.now()
            duration = now - start
            
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            
            if hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        except Exception:
            return "Unknown"
    
    def get_statistics(self):
        
        current_signouts = self.get_current_signouts()
        
        total_entries = len(current_signouts)
        total_soldiers = sum(len(entry['soldiers']) for entry in current_signouts)

        destinations = {}
        for entry in current_signouts:
            dest = entry['destination']
            destinations[dest] = destinations.get(dest, 0) + len(entry['soldiers'])
        
        return {
            'total_entries': total_entries,
            'total_soldiers': total_soldiers,
            'destinations': destinations
        }
    
    def cleanup_old_logs(self, days_to_keep=30):
        
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        for log_file in self.logs_dir.glob("signout_log_*.log"):
            if log_file.stat().st_mtime < cutoff_date:
                try:
                    log_file.unlink()
                    self.logger.info(f"Deleted old log file: {log_file.name}")
                except Exception as e:
                    self.logger.error(f"Failed to delete log file {log_file.name}: {e}")
    
    def export_current_signouts(self, export_file: str):
        
        data = self._load_json(self.current_signouts_file)
        self._save_json(Path(export_file), data)
        self.logger.info(f"Exported current sign-outs to: {export_file}")
    
    def get_log_files(self):
        
        log_files = []
        for log_file in sorted(self.logs_dir.glob("signout_log_*.log")):
            log_files.append(log_file.name)
        return log_files
    
    def log_system_event(self, event: str, details: str = ""):
        
        if details:
            self.logger.info(f"SYSTEM | {event} | {details}")
        else:
            self.logger.info(f"SYSTEM | {event}")