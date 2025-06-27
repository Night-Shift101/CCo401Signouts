from datetime import datetime
import re

class DataUtils:
    
    @staticmethod
    def convert_ui_to_storage(ui_data):
        
        storage_data = {
            'soldiers': ui_data.get('soldiers', []),
            'destination': ui_data.get('destination', '').strip(),
            'phone': DataUtils.format_phone_number(ui_data.get('phone', '')),
            'categories': ui_data.get('categories', []),
            'datetime': datetime.now().isoformat(),
            'ds': ui_data.get('ds', '').strip()
        }
        
        return storage_data
    
    @staticmethod
    def convert_storage_to_display(storage_data):
        
        entry_id = storage_data.get('id', '')
        soldiers = storage_data.get('soldiers', [])
        destination = storage_data.get('destination', '')
        phone = storage_data.get('phone', '')
        ds = storage_data.get('ds', '')
        datetime_str = storage_data.get('datetime', '')
        try:
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            formatted_datetime = dt.strftime("%Y-%m-%d %H:%M")
        except:
            formatted_datetime = datetime_str
        
        return (entry_id, soldiers, destination, phone, formatted_datetime, ds)
    
    @staticmethod
    def format_phone_number(phone):

        digits = re.sub(r'\D', '', phone)

        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':

            return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:

            return phone
    
    @staticmethod
    def validate_signout_data(data):
        
        errors = []

        soldiers = data.get('soldiers', [])
        if not soldiers:
            errors.append("At least one soldier must be selected")
        elif not isinstance(soldiers, list):
            errors.append("Soldiers data must be a list")

        destination = data.get('destination', '').strip()
        if not destination:
            errors.append("Destination is required")
        elif len(destination) > 100:
            errors.append("Destination must be 100 characters or less")

        phone = data.get('phone', '').strip()
        if not phone:
            errors.append("Phone number is required")
        elif not DataUtils.is_valid_phone(phone):
            errors.append("Invalid phone number format")
        
        return errors
    
    @staticmethod
    def is_valid_phone(phone):

        digits = re.sub(r'\D', '', phone)

        return len(digits) == 10 or (len(digits) == 11 and digits[0] == '1')
    
    @staticmethod
    def format_soldiers_for_display(soldiers, max_display=3):
        
        if not soldiers:
            return "No soldiers"
        
        if len(soldiers) <= max_display:
            return ", ".join(soldiers)
        else:
            displayed = soldiers[:max_display]
            remaining = len(soldiers) - max_display
            return f"{', '.join(displayed)} and {remaining} more"
    
    @staticmethod
    def get_duration_from_datetime(start_datetime):
        
        try:
            start = datetime.fromisoformat(start_datetime.replace('Z', '+00:00'))
            now = datetime.now()
            duration = now - start
            
            total_minutes = int(duration.total_seconds() // 60)
            hours = total_minutes // 60
            minutes = total_minutes % 60
            
            if hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        except Exception:
            return "Unknown"
    
    @staticmethod
    def search_signouts(signouts, search_term):
        
        if not search_term:
            return signouts
        
        search_term = search_term.lower()
        filtered = []
        
        for entry in signouts:

            soldiers_match = any(search_term in soldier.lower() 
                               for soldier in entry.get('soldiers', []))

            destination_match = search_term in entry.get('destination', '').lower()

            id_match = search_term in entry.get('id', '').lower()
            
            if soldiers_match or destination_match or id_match:
                filtered.append(entry)
        
        return filtered
    
    @staticmethod
    def sort_signouts(signouts, sort_by='datetime', reverse=False):
        
        if sort_by == 'datetime':
            return sorted(signouts, 
                         key=lambda x: x.get('datetime', ''), 
                         reverse=reverse)
        elif sort_by == 'destination':
            return sorted(signouts, 
                         key=lambda x: x.get('destination', '').lower(), 
                         reverse=reverse)
        elif sort_by == 'id':
            return sorted(signouts, 
                         key=lambda x: int(x.get('id', '0')), 
                         reverse=reverse)
        else:
            return signouts
    
    @staticmethod
    def get_sample_data():
        
        sample_data = [
            {
                'id': '001',
                'soldiers': ['SGT Smith, J.', 'SPC Johnson, M.', 'PFC Brown, D.'],
                'destination': 'Fort Liberty',
                'phone': '(555) 123-4567',
                'categories': ['Leave'],
                'datetime': '2025-06-25T08:00:00',
                'notes': 'Training Exercise'
            },
            {
                'id': '002',
                'soldiers': ['CPL Wilson, S.', 'PV2 Davis, M.'],
                'destination': 'Womack Army Medical Center',
                'phone': '(555) 234-5678',
                'categories': ['Family'],
                'datetime': '2025-06-25T09:00:00',
                'notes': 'Medical Appointments'
            },
            {
                'id': '003',
                'soldiers': ['SSG Garcia, C.'],
                'destination': 'Downtown Fayetteville',
                'phone': '(555) 345-6789',
                'categories': ['Off Post', 'Family'],
                'datetime': '2025-06-25T10:00:00',
                'notes': 'Personal Business'
            }
        ]
        
        return sample_data