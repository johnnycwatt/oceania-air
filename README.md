# Oceania Air

## Overview
This web application is designed to simulate a flight booking system for a fictitious airline, allowing users to search for flights, view available options, and eventually book them. The application focuses on providing a seamless user experience for flight search and listing, with an emphasis on accurate time zone handling and data integrity.

## Features
- **Flight Search**: Users can search for flights by selecting departure and arrival airports, travel dates, and the number of passengers. 
- **Flight Listing**: Displays a list of available flights with details such as origin and destination airports, departure time (adjusted to the local time of the origin airport), and price.
- **Time Zone Handling**: Departure times are converted from UTC to the local time zone of the origin airport, ensuring accurate scheduling information for users.
- **Data Validation**: Ensures flights cannot have the same origin and destination, arrival times are after departure times, and bookings respect seat availability.

## Tech Stack

### Backend
- **Framework**: Django (Python)
- **API**: Django REST Framework (DRF) for building RESTful APIs
- **Database**: SQLite
- **Testing**: Django’s built-in testing framework

### Frontend
- **Framework**: React (JavaScript)
- **Styling**: Bootstrap

## Progress
### Backend
- **Models**: Fully implemented models for Airport, Aircraft, Flight, Booking and Passengers.

- **APIs**: Created endpoints for listing and creating flights, airports, bookings, and passengers. Added filtering support to the flight list endpoint to enable search functionality.

- **Business Logic**: Implemented validations for flight creation and booking creation

- **Tests**: Have done backend manual tests and have created automated tests for flight and booking creation testing standard scenarios and potential edge cases.

### Frontend
- **Flight Search Form**: Implemented with airport dropdowns populated via `/api/flights/airports/`. Supports searching by origin, destination, and date, with validation for past dates and return trip dates. Currently being used in the FlightSearch page and as a widget on the Landing page

- **Flight List**: Displays available flights based on search. Includes departure time in the origin airport’s local time zone and flight price.

- **Routing**: Set up basic routing with React Router

- **Time Zone Handling**: Added logic to convert UTC times to local times based on the origin airport’s timezone

### Next Steps
- **Booking Flow**
- **Styling**

## Notes

This project is a work in progress. 

