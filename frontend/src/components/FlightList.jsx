// oceania-air/frontend/src/components/FlightList.jsx
import React from 'react';
import { useLocation } from 'react-router-dom';
import { FaPlane } from 'react-icons/fa'; // Import airplane icon
import '../App.css'; // Ensure CSS is imported

const FlightList = () => {
  const location = useLocation();
  const flights = location.state?.flights || [];

  // Timezone mapping based on assignment requirements
  const timezoneMap = {
    'GMT+12': 'Pacific/Auckland',     // Mainland NZ (NZNE, NZRO, NZGB, NZTL)
    'GMT+12:45': 'Pacific/Chatham',   // Chatham Islands (NZCI)
    'GMT+10': 'Australia/Melbourne',  // Melbourne (YMML)
  };

  // Helper function to format time in 24-hour format
  const getLocalTime = (utcTime, timezone) => {
    const ianaTimezone = timezoneMap[timezone] || 'UTC';
    return new Date(utcTime).toLocaleTimeString('en-US', {
      timeZone: ianaTimezone,
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    }); // e.g., "14:30"
  };

  // Helper function to format date for comparison (YYYY-MM-DD)
  const getLocalDate = (utcTime, timezone) => {
    const ianaTimezone = timezoneMap[timezone] || 'UTC';
    return new Date(utcTime).toLocaleDateString('en-CA', {
      timeZone: ianaTimezone,
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    }); // e.g., "2025-05-12"
  };

  // Helper function to format display date
  const formatDisplayDate = (utcTime, timezone) => {
    const ianaTimezone = timezoneMap[timezone] || 'UTC';
    return new Date(utcTime).toLocaleDateString('en-US', {
      timeZone: ianaTimezone,
      weekday: 'long',
      month: 'long',
      day: 'numeric',
      year: 'numeric',
    }); // e.g., "Friday, May 30, 2025"
  };

  // Extract header information from the first flight (assuming all flights share the same route and date)
  let originName = '';
  let originCode = '';
  let destinationName = '';
  let destinationCode = '';
  let departureDate = '';

  if (flights.length > 0) {
    const firstFlight = flights[0];
    originName = firstFlight.origin.name;
    originCode = firstFlight.origin.icao_code;
    destinationName = firstFlight.destination.name;
    destinationCode = firstFlight.destination.icao_code;
    departureDate = formatDisplayDate(firstFlight.departure_time, firstFlight.origin.timezone);
  }

  return (
    <div className="flight-list">
      {flights.length > 0 ? (
        <>
          {/* Header Section */}
          <div className="flight-header">
            <h2>
              {originName} ({originCode}) <FaPlane className="airplane-icon" /> {destinationName} ({destinationCode})
            </h2>
            <p>Choose your outbound flight</p>
            <p>{originName} to {destinationName}</p>
            <p>{departureDate} ({flights.length} options)</p>
          </div>

          {/* Scrollable Flight Cards */}
          <div className="flight-cards-container">
            {flights.map((flight) => {
              const departureLocalTime = getLocalTime(flight.departure_time, flight.origin.timezone);
              const arrivalLocalTime = getLocalTime(flight.arrival_time, flight.destination.timezone);
              const departureLocalDate = getLocalDate(flight.departure_time, flight.origin.timezone);
              const arrivalLocalDate = getLocalDate(flight.arrival_time, flight.destination.timezone);
              const dayDiff = arrivalLocalDate > departureLocalDate ? ' (+1)' : '';

              const durationMs = new Date(flight.arrival_time) - new Date(flight.departure_time);
              const hours = Math.floor(durationMs / 3600000);
              const minutes = Math.floor((durationMs % 3600000) / 60000);
              const durationStr = `${hours}h ${minutes}m`;

              return (
                <div key={flight.id} className="flight-card p-3 mb-3 border rounded">
                  <div className="row align-items-center">
                    <div className="col-3">
                      <div className="departure-date">{departureLocalDate}</div>
                      <div className="departure-time">{departureLocalTime}</div>
                      <div className="airport-code">{flight.origin.icao_code}</div>
                    </div>
                    <div className="col-3 text-center">
                      <div className="duration">{durationStr}</div>
                      <div>→</div>
                    </div>
                    <div className="col-3">
                      <div className="arrival-date">{arrivalLocalDate}</div>
                      <div className="arrival-time">{arrivalLocalTime}{dayDiff}</div>
                      <div className="airport-code">{flight.destination.icao_code}</div>
                    </div>
                    <div className="col-3 text-right">
                      <div className="price">${flight.price}</div>
                    </div>
                  </div>
                  <div className="row mt-2">
                    <div className="col-12 flight-details">
                      {flight.aircraft.model} - {flight.flight_number}
                    </div>
                  </div>
                  <button className="btn btn-primary mt-2">Select</button>
                </div>
              );
            })}
          </div>
        </>
      ) : (
        <p>No flights found.</p>
      )}
    </div>
  );
};

export default FlightList;