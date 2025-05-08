from django.core.management.base import BaseCommand
from flights.models import Airport, Aircraft

class Command(BaseCommand):
    help = 'Populate airports and aircraft for Oceania Air'

    def handle(self, *args, **kwargs):
        # Define airports with ICAO code, name, and timezone
        airports_data = [
            {'icao_code': 'NZNE', 'name': 'Dairy Flat', 'timezone': 'GMT+12'},
            {'icao_code': 'YMML', 'name': 'Melbourne', 'timezone': 'GMT+10'},
            {'icao_code': 'NZRO', 'name': 'Rotorua', 'timezone': 'GMT+12'},
            {'icao_code': 'NZGB', 'name': 'Great Barrier Island', 'timezone': 'GMT+12'},
            {'icao_code': 'NZCI', 'name': 'Chatham Islands', 'timezone': 'GMT+12:45'},
            {'icao_code': 'NZTL', 'name': 'Lake Tekapo', 'timezone': 'GMT+12'},
        ]

        # Populate airports
        for airport in airports_data:
            Airport.objects.get_or_create(
                icao_code=airport['icao_code'],
                defaults={
                    'name': airport['name'],
                    'timezone': airport['timezone']
                }
            )

        # Define aircraft with model, capacity, registration_number, and status
        aircraft_data = [
            {'model': 'SyberJet SJ30i', 'capacity': 6, 'registration_number': 'ZK-SJ30', 'status': 'active'},
            {'model': 'Cirrus SF50', 'capacity': 4, 'registration_number': 'ZK-CIR1', 'status': 'active'},
            {'model': 'Cirrus SF50', 'capacity': 4, 'registration_number': 'ZK-CIR2', 'status': 'active'},
            {'model': 'HondaJet Elite', 'capacity': 5, 'registration_number': 'ZK-HJE1', 'status': 'active'},
            {'model': 'HondaJet Elite', 'capacity': 5, 'registration_number': 'ZK-HJE2', 'status': 'active'},
        ]

        # Populate aircraft
        for aircraft in aircraft_data:
            Aircraft.objects.get_or_create(
                registration_number=aircraft['registration_number'],
                defaults={
                    'model': aircraft['model'],
                    'capacity': aircraft['capacity'],
                    'status': aircraft['status']
                }
            )

        self.stdout.write(self.style.SUCCESS('Airports and aircraft populated successfully!'))