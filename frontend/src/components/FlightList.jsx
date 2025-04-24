import React from 'react';
import { useLocation } from 'react-router-dom';

const FlightList = () => {
  const location = useLocation();
  const flights = location.state?.flights || [];

  // Map GMT offsets to IANA time zones (expand this as needed)
  const timezoneMap = {
    'GMT+12': 'Pacific/Auckland',
    'GMT+10': 'Australia/Melbourne',
  };

  const formatLocalTime = (utcTime, timezone) => {
    const ianaTimezone = timezoneMap[timezone] || 'UTC'; // Fallback to UTC if unmapped
    return new Date(utcTime).toLocaleString('en-US', {
      timeZone: ianaTimezone,
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      timeZoneName: 'short',
    });
  };

  return (
    <div>
      <h2>Available Flights</h2>
      {flights.length > 0 ? (
        <ul>
          {flights.map((flight) => (
            <li key={flight.id}>
              {flight.origin.icao_code} to {flight.destination.icao_code} -{' '}
              Departure: {formatLocalTime(flight.departure_time, flight.origin.timezone)} -{' '}
              Price: ${flight.price}
            </li>
          ))}
        </ul>
      ) : (
        <p>No flights found.</p>
      )}
    </div>
  );
};

export default FlightList;