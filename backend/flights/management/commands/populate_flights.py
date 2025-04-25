import pytz
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from flights.models import Airport, Aircraft, Flight

class Command(BaseCommand):
    help = 'Populate flights for 20 weeks starting from May 5, 2025'

    def handle(self, *args, **kwargs):
        # Define airports by ICAO code
        airports = {
            'NZNE': Airport.objects.get(icao_code='NZNE'),  # Dairy Flat
            'YMML': Airport.objects.get(icao_code='YMML'),  # Melbourne
            'NZRO': Airport.objects.get(icao_code='NZRO'),  # Rotorua
            'NZGB': Airport.objects.get(icao_code='NZGB'),  # Great Barrier Island
            'NZCI': Airport.objects.get(icao_code='NZCI'),  # Chatham Islands
            'NZTL': Airport.objects.get(icao_code='NZTL'),  # Lake Tekapo
        }

        # Define aircraft by registration number
        aircraft = {
            'ZK-SJ30': Aircraft.objects.get(registration_number='ZK-SJ30'),
            'ZK-CIR1': Aircraft.objects.get(registration_number='ZK-CIR1'),
            'ZK-CIR2': Aircraft.objects.get(registration_number='ZK-CIR2'),
            'ZK-HJE1': Aircraft.objects.get(registration_number='ZK-HJE1'),
            'ZK-HJE2': Aircraft.objects.get(registration_number='ZK-HJE2'),
        }

        # Time zone offsets (hours from UTC)
        timezones = {
            'NZNE': 12,    # GMT+12
            'YMML': 10,    # GMT+10
            'NZRO': 12,    # GMT+12
            'NZGB': 12,    # GMT+12
            'NZCI': 12.75, # GMT+12:45
            'NZTL': 12,    # GMT+12
        }

        # Convert local time to UTC
        def local_to_utc(local_dt, tz_offset):
            return local_dt - timedelta(hours=tz_offset)

        # Start date Monday, May 5, 2025 (UTC)
        start_date = datetime(2025, 5, 5, tzinfo=pytz.utc)

        # Generate flights for 20 weeks
        for week in range(20):
            week_start = start_date + timedelta(weeks=week)

            # 1. Melbourne Prestige Service (Weekly)
            # Outbound: Friday, 10:00 AM NZST, Flight Number: OA100
            friday = week_start + timedelta(days=4)
            outbound_local_dep = datetime(friday.year, friday.month, friday.day, 10, 0)
            outbound_utc_dep = local_to_utc(outbound_local_dep, timezones['NZNE'])
            outbound_utc_arr = outbound_utc_dep + timedelta(hours=4)  # Westbound, longer duration
            Flight.objects.get_or_create(
                flight_number='OA100',
                departure_time=outbound_utc_dep.replace(tzinfo=pytz.utc),
                defaults={
                    'origin': airports['NZNE'],
                    'destination': airports['YMML'],
                    'arrival_time': outbound_utc_arr.replace(tzinfo=pytz.utc),
                    'aircraft': aircraft['ZK-SJ30'],
                    'capacity': 6,
                    'seats_available': 6,
                    'price': 500.00,
                    'status': 'scheduled'
                }
            )
            # Return: Sunday, 3:00 PM AEST, Flight Number: OA101
            sunday = week_start + timedelta(days=6)
            return_local_dep = datetime(sunday.year, sunday.month, sunday.day, 15, 0)
            return_utc_dep = local_to_utc(return_local_dep, timezones['YMML'])
            return_utc_arr = return_utc_dep + timedelta(hours=3)  # Eastbound, shorter duration
            Flight.objects.get_or_create(
                flight_number='OA101',
                departure_time=return_utc_dep.replace(tzinfo=pytz.utc),
                defaults={
                    'origin': airports['YMML'],
                    'destination': airports['NZNE'],
                    'arrival_time': return_utc_arr.replace(tzinfo=pytz.utc),
                    'aircraft': aircraft['ZK-SJ30'],
                    'capacity': 6,
                    'seats_available': 6,
                    'price': 500.00,
                    'status': 'scheduled'
                }
            )

            # 2. Rotorua Shuttle Service (Twice Daily, Weekdays)
            for day in range(5):  # Monday to Friday
                current_day = week_start + timedelta(days=day)
                # Morning Outbound: 7:00 AM NZST, Flight Number: OA200
                morning_out_local_dep = datetime(current_day.year, current_day.month, current_day.day, 7, 0)
                morning_out_utc_dep = local_to_utc(morning_out_local_dep, timezones['NZNE'])
                morning_out_utc_arr = morning_out_utc_dep + timedelta(minutes=50)  # Southbound
                Flight.objects.get_or_create(
                    flight_number='OA200',
                    departure_time=morning_out_utc_dep.replace(tzinfo=pytz.utc),
                    defaults={
                        'origin': airports['NZNE'],
                        'destination': airports['NZRO'],
                        'arrival_time': morning_out_utc_arr.replace(tzinfo=pytz.utc),
                        'aircraft': aircraft['ZK-CIR1'],
                        'capacity': 5,
                        'seats_available': 5,
                        'price': 150.00,
                        'status': 'scheduled'
                    }
                )
                # Morning Return: 8:30 AM NZST, Flight Number: OA201
                morning_ret_local_dep = datetime(current_day.year, current_day.month, current_day.day, 8, 30)
                morning_ret_utc_dep = local_to_utc(morning_ret_local_dep, timezones['NZRO'])
                morning_ret_utc_arr = morning_ret_utc_dep + timedelta(minutes=40)  # Northbound, shorter
                Flight.objects.get_or_create(
                    flight_number='OA201',
                    departure_time=morning_ret_utc_dep.replace(tzinfo=pytz.utc),
                    defaults={
                        'origin': airports['NZRO'],
                        'destination': airports['NZNE'],
                        'arrival_time': morning_ret_utc_arr.replace(tzinfo=pytz.utc),
                        'aircraft': aircraft['ZK-CIR1'],
                        'capacity': 5,
                        'seats_available': 5,
                        'price': 150.00,
                        'status': 'scheduled'
                    }
                )
                # Afternoon Outbound: 4:00 PM NZST, Flight Number: OA202
                afternoon_out_local_dep = datetime(current_day.year, current_day.month, current_day.day, 16, 0)
                afternoon_out_utc_dep = local_to_utc(afternoon_out_local_dep, timezones['NZNE'])
                afternoon_out_utc_arr = afternoon_out_utc_dep + timedelta(minutes=50)
                Flight.objects.get_or_create(
                    flight_number='OA202',
                    departure_time=afternoon_out_utc_dep.replace(tzinfo=pytz.utc),
                    defaults={
                        'origin': airports['NZNE'],
                        'destination': airports['NZRO'],
                        'arrival_time': afternoon_out_utc_arr.replace(tzinfo=pytz.utc),
                        'aircraft': aircraft['ZK-CIR1'],
                        'capacity': 5,
                        'seats_available': 5,
                        'price': 150.00,
                        'status': 'scheduled'
                    }
                )
                # Afternoon Return: 5:30 PM NZST, Flight Number: OA203
                afternoon_ret_local_dep = datetime(current_day.year, current_day.month, current_day.day, 17, 30)
                afternoon_ret_utc_dep = local_to_utc(afternoon_ret_local_dep, timezones['NZRO'])
                afternoon_ret_utc_arr = afternoon_ret_utc_dep + timedelta(minutes=40)
                Flight.objects.get_or_create(
                    flight_number='OA203',
                    departure_time=afternoon_ret_utc_dep.replace(tzinfo=pytz.utc),
                    defaults={
                        'origin': airports['NZRO'],
                        'destination': airports['NZNE'],
                        'arrival_time': afternoon_ret_utc_arr.replace(tzinfo=pytz.utc),
                        'aircraft': aircraft['ZK-CIR1'],
                        'capacity': 5,
                        'seats_available': 5,
                        'price': 150.00,
                        'status': 'scheduled'
                    }
                )

            # 3. Great Barrier Island Service (Three Times Weekly)
            for day_offset in [0, 2, 4]:  # Mon, Wed, Fri
                outbound_date = week_start + timedelta(days=day_offset)
                # Outbound: 9:00 AM NZST, Flight Number: OA300
                outbound_local_dep = datetime(outbound_date.year, outbound_date.month, outbound_date.day, 9, 0)
                outbound_utc_dep = local_to_utc(outbound_local_dep, timezones['NZNE'])
                outbound_utc_arr = outbound_utc_dep + timedelta(minutes=32)
                Flight.objects.get_or_create(
                    flight_number='OA300',
                    departure_time=outbound_utc_dep.replace(tzinfo=pytz.utc),
                    defaults={
                        'origin': airports['NZNE'],
                        'destination': airports['NZGB'],
                        'arrival_time': outbound_utc_arr.replace(tzinfo=pytz.utc),
                        'aircraft': aircraft['ZK-CIR2'],
                        'capacity': 5,
                        'seats_available': 5,
                        'price': 100.00,
                        'status': 'scheduled'
                    }
                )
                # Return: Next day, 9:00 AM NZST, Flight Number: OA301
                return_date = outbound_date + timedelta(days=1)
                return_local_dep = datetime(return_date.year, return_date.month, return_date.day, 9, 0)
                return_utc_dep = local_to_utc(return_local_dep, timezones['NZGB'])
                return_utc_arr = return_utc_dep + timedelta(minutes=32)
                Flight.objects.get_or_create(
                    flight_number='OA301',
                    departure_time=return_utc_dep.replace(tzinfo=pytz.utc),
                    defaults={
                        'origin': airports['NZGB'],
                        'destination': airports['NZNE'],
                        'arrival_time': return_utc_arr.replace(tzinfo=pytz.utc),
                        'aircraft': aircraft['ZK-CIR2'],
                        'capacity': 5,
                        'seats_available': 5,
                        'price': 100.00,
                        'status': 'scheduled'
                    }
                )

            # 4. Chatham Islands Service (Twice Weekly)
            for day_offset in [1, 4]:  # Tue, Fri
                outbound_date = week_start + timedelta(days=day_offset)
                # Outbound: 11:00 AM NZST, Flight Number: OA400
                outbound_local_dep = datetime(outbound_date.year, outbound_date.month, outbound_date.day, 11, 0)
                outbound_utc_dep = local_to_utc(outbound_local_dep, timezones['NZNE'])
                outbound_utc_arr = outbound_utc_dep + timedelta(hours=1, minutes=22)  # Eastbound
                Flight.objects.get_or_create(
                    flight_number='OA400',
                    departure_time=outbound_utc_dep.replace(tzinfo=pytz.utc),
                    defaults={
                        'origin': airports['NZNE'],
                        'destination': airports['NZCI'],
                        'arrival_time': outbound_utc_arr.replace(tzinfo=pytz.utc),
                        'aircraft': aircraft['ZK-HJE1'],
                        'capacity': 6,
                        'seats_available': 6,
                        'price': 300.00,
                        'status': 'scheduled'
                    }
                )
                # Return: Next day, 11:00 AM CHADT, Flight Number: OA401
                return_date = outbound_date + timedelta(days=1)
                return_local_dep = datetime(return_date.year, return_date.month, return_date.day, 11, 0)
                return_utc_dep = local_to_utc(return_local_dep, timezones['NZCI'])
                return_utc_arr = return_utc_dep + timedelta(hours=1, minutes=53)  # Westbound, longer
                Flight.objects.get_or_create(
                    flight_number='OA401',
                    departure_time=return_utc_dep.replace(tzinfo=pytz.utc),
                    defaults={
                        'origin': airports['NZCI'],
                        'destination': airports['NZNE'],
                        'arrival_time': return_utc_arr.replace(tzinfo=pytz.utc),
                        'aircraft': aircraft['ZK-HJE1'],
                        'capacity': 6,
                        'seats_available': 6,
                        'price': 300.00,
                        'status': 'scheduled'
                    }
                )

            # 5. Lake Tekapo Service (Weekly)
            # Outbound: Monday, 1:00 PM NZST, Flight Number: OA500
            monday = week_start
            outbound_local_dep = datetime(monday.year, monday.month, monday.day, 13, 0)
            outbound_utc_dep = local_to_utc(outbound_local_dep, timezones['NZNE'])
            outbound_utc_arr = outbound_utc_dep + timedelta(hours=1, minutes=38)
            Flight.objects.get_or_create(
                flight_number='OA500',
                departure_time=outbound_utc_dep.replace(tzinfo=pytz.utc),
                defaults={
                    'origin': airports['NZNE'],
                    'destination': airports['NZTL'],
                    'arrival_time': outbound_utc_arr.replace(tzinfo=pytz.utc),
                    'aircraft': aircraft['ZK-HJE2'],
                    'capacity': 6,
                    'seats_available': 6,
                    'price': 250.00,
                    'status': 'scheduled'
                }
            )
            # Return: Tuesday, 1:00 PM NZST, Flight Number: OA501
            tuesday = week_start + timedelta(days=1)
            return_local_dep = datetime(tuesday.year, tuesday.month, tuesday.day, 13, 0)
            return_utc_dep = local_to_utc(return_local_dep, timezones['NZTL'])
            return_utc_arr = return_utc_dep + timedelta(hours=1, minutes=38)
            Flight.objects.get_or_create(
                flight_number='OA501',
                departure_time=return_utc_dep.replace(tzinfo=pytz.utc),
                defaults={
                    'origin': airports['NZTL'],
                    'destination': airports['NZNE'],
                    'arrival_time': return_utc_arr.replace(tzinfo=pytz.utc),
                    'aircraft': aircraft['ZK-HJE2'],
                    'capacity': 6,
                    'seats_available': 6,
                    'price': 250.00,
                    'status': 'scheduled'
                }
            )

        self.stdout.write(self.style.SUCCESS('Flights populated successfully for 20 weeks starting May 5, 2025!'))