import os
import pandas as pd
import numpy as np
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

np.random.seed(42)

years = [2020, 2021, 2022, 2023, 2024, 2025]
months = list(range(1, 13))

# Realistic Indian Cities & Metropolitan Areas with exact Lat/Lon coordinates
indian_city_data = {
    'Mumbai': {
        'pop_range': (12500000, 13500000),
        'areas': [
            ('Bandra West', 19.0596, 72.8295),
            ('Colaba', 18.9067, 72.8147),
            ('Andheri East', 19.1136, 72.8697),
            ('Dadar', 19.0178, 72.8478),
            ('Kurla', 19.0726, 72.8845),
            ('Thane City', 19.2183, 72.9781)
        ]
    },
    'Delhi NCR': {
        'pop_range': (16000000, 17500000),
        'areas': [
            ('Connaught Place', 28.6304, 77.2177),
            ('Dwarka', 28.5921, 77.0460),
            ('Rohini', 28.7041, 77.1025),
            ('Saket', 28.5244, 77.2188),
            ('Noida Sector 62', 28.6280, 77.3649),
            ('Gurugram Cyber City', 28.4950, 77.0895)
        ]
    },
    'Bengaluru': {
        'pop_range': (8500000, 9800000),
        'areas': [
            ('Indiranagar', 12.9784, 77.6408),
            ('Koramangala', 12.9352, 77.6245),
            ('Whitefield', 12.9698, 77.7499),
            ('Jayanagar', 12.9250, 77.5938),
            ('MG Road', 12.9756, 77.6066),
            ('Electronic City', 12.8399, 77.6770)
        ]
    },
    'Kolkata': {
        'pop_range': (4500000, 5200000),
        'areas': [
            ('Park Street', 22.5551, 88.3518),
            ('Salt Lake Sector 5', 22.5726, 88.4331),
            ('Howrah Central', 22.5958, 88.2636),
            ('New Town', 22.5855, 88.4714),
            ('Alipore', 22.5332, 88.3333)
        ]
    },
    'Chennai': {
        'pop_range': (7000000, 8100000),
        'areas': [
            ('T. Nagar', 13.0418, 80.2341),
            ('Adyar', 13.0012, 80.2565),
            ('Anna Nagar', 13.0850, 80.2101),
            ('Velachery', 12.9815, 80.2180),
            ('Mylapore', 13.0339, 80.2690)
        ]
    },
    'Hyderabad': {
        'pop_range': (6800000, 7900000),
        'areas': [
            ('Banjara Hills', 17.4156, 78.4347),
            ('Hitech City', 17.4435, 78.3772),
            ('Secunderabad', 17.4399, 78.4983),
            ('Gachibowli', 17.4401, 78.3489),
            ('Jubilee Hills', 17.4319, 78.4071)
        ]
    },
    'Pune': {
        'pop_range': (3100000, 3800000),
        'areas': [
            ('Kothrud', 18.5074, 73.8077),
            ('Viman Nagar', 18.5679, 73.9143),
            ('Hinjewadi IT Park', 18.5912, 73.7389),
            ('Baner', 18.5590, 73.7868),
            ('Shivajinagar', 18.5314, 73.8446)
        ]
    },
    'Ahmedabad': {
        'pop_range': (5500000, 6300000),
        'areas': [
            ('Navrangpura', 23.0366, 72.5611),
            ('SG Highway', 23.0300, 72.5076),
            ('Maninagar', 22.9978, 72.6000),
            ('Satellite', 23.0300, 72.5176),
            ('Bodakdev', 23.0450, 72.5100)
        ]
    }
}

# Indian IPC / NCRB Crime Categories
crime_types = [
    'Theft (IPC 379)',
    'Cyber Crime (IT Act)',
    'Vehicle Theft (IPC 379)',
    'Burglary / Housebreak (IPC 457)',
    'Robbery & Snatching (IPC 392)',
    'Assault & Hurt (IPC 354/323)',
    'Financial Fraud (IPC 420)'
]

severity_map = {
    'Theft (IPC 379)': 'Low',
    'Cyber Crime (IT Act)': 'Medium',
    'Vehicle Theft (IPC 379)': 'Medium',
    'Burglary / Housebreak (IPC 457)': 'Medium',
    'Financial Fraud (IPC 420)': 'Medium',
    'Robbery & Snatching (IPC 392)': 'High',
    'Assault & Hurt (IPC 354/323)': 'Critical'
}

data = []

for year in years:
    # Multi-year trend (subtle annual pattern)
    year_trend = 1.0 + (year - 2020) * 0.028
    for month in months:
        # Seasonal variation in India (festive season / summer spikes)
        season_factor = 1.0 + 0.12 * np.sin((month - 4) * np.pi / 6)
        
        for city, info in indian_city_data.items():
            base_pop = np.random.randint(info['pop_range'][0], info['pop_range'][1])
            pop = int(base_pop * (1 + (year - 2020) * 0.012))
            
            for area_name, base_lat, base_lon in info['areas']:
                for crime in crime_types:
                    base_count = {
                        'Theft (IPC 379)': np.random.randint(120, 280),
                        'Cyber Crime (IT Act)': np.random.randint(80, 210),
                        'Vehicle Theft (IPC 379)': np.random.randint(60, 150),
                        'Burglary / Housebreak (IPC 457)': np.random.randint(45, 110),
                        'Financial Fraud (IPC 420)': np.random.randint(50, 130),
                        'Robbery & Snatching (IPC 392)': np.random.randint(25, 75),
                        'Assault & Hurt (IPC 354/323)': np.random.randint(20, 65)
                    }[crime]
                    
                    noise = np.random.normal(1.0, 0.10)
                    final_count = max(5, int(base_count * year_trend * season_factor * noise))
                    
                    # Precise coordinate jitter around Indian locations
                    lat = round(base_lat + np.random.uniform(-0.008, 0.008), 6)
                    lon = round(base_lon + np.random.uniform(-0.008, 0.008), 6)
                    
                    severity = severity_map[crime]
                    
                    data.append({
                        'Year': year,
                        'Month': month,
                        'City': city,
                        'Area': area_name,
                        'Crime_Type': crime,
                        'Crime_Count': final_count,
                        'Population': pop,
                        'Severity': severity,
                        'Latitude': lat,
                        'Longitude': lon
                    })

df = pd.DataFrame(data)
csv_path = os.path.join(DATA_DIR, 'sample_data.csv')
crime_data_path = os.path.join(DATA_DIR, 'crime_data.csv')
df.to_csv(csv_path, index=False)
df.to_csv(crime_data_path, index=False)
print(f"Generated {len(df)} Indian historical crime dataset records at {csv_path}")
