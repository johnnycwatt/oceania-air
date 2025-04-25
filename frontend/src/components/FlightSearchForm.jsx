import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

function FlightSearchForm({ isWidget = false }) {
  const [airports, setAirports] = useState([]);
  const [departure, setDeparture] = useState('');
  const [arrival, setArrival] = useState('');
  const [tripType, setTripType] = useState('one-way');
  const [departureDate, setDepartureDate] = useState(null); // Use null for DatePicker
  const [returnDate, setReturnDate] = useState(null); // Use null for DatePicker
  const [passengers, setPassengers] = useState(1);
  const [expanded, setExpanded] = useState(!isWidget);
  const [departureTimezone, setDepartureTimezone] = useState('');
  const [flexibleDates, setFlexibleDates] = useState(false);

  const navigate = useNavigate();
  const today = new Date();

  // Fetch airports on mount
  useEffect(() => {
    const fetchAirports = async () => {
      try {
        const response = await axios.get('/api/flights/airports/');
        if (Array.isArray(response.data)) {
          setAirports(response.data);
        } else {
          console.error('Expected an array of airports:', response.data);
          setAirports([]);
        }
      } catch (error) {
        console.error('Error fetching airports:', error);
        setAirports([]);
      }
    };
    fetchAirports();
  }, []);

  const parseOffset = (timezone) => {
    const match = timezone.match(/GMT([+-]\d+(?:\.\d+)?)/);
    return match ? parseFloat(match[1]) : 0;
  };

  const handleContinue = () => {
    if (!departure || !arrival) {
      alert('Please select departure and arrival airports.');
      return;
    }
    setExpanded(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!departure || !arrival || !departureDate) {
      alert('Please fill in all required fields.');
      return;
    }
    if (departureDate < today) {
      alert('Departure date cannot be in the past.');
      return;
    }
    if (tripType === 'return' && (!returnDate || returnDate <= departureDate)) {
      alert('Return date must be after departure date.');
      return;
    }

    try {
      const offset = parseOffset(departureTimezone);
      const localStart = new Date(departureDate.setHours(0, 0, 0, 0));
      const localEnd = new Date(departureDate.setHours(23, 59, 59, 999));
      const utcStart = new Date(localStart.getTime() - offset * 3600000);
      const utcEnd = new Date(localEnd.getTime() - offset * 3600000);

      let params = {
        'origin__icao_code': departure,
        'destination__icao_code': arrival,
        'departure_time__gte': utcStart.toISOString(),
        'departure_time__lt': utcEnd.toISOString(),
      };

      if (flexibleDates) {
        const flexStart = new Date(localStart.getTime() - 5 * 24 * 3600000);
        const flexEnd = new Date(localEnd.getTime() + 5 * 24 * 3600000);
        params['departure_time__gte'] = flexStart.toISOString();
        params['departure_time__lt'] = flexEnd.toISOString();
      }

      if (tripType === 'return') {
        params.returnDate = returnDate.toISOString().split('T')[0];
      }

      const response = await axios.get('/api/flights/flights', { params });
      navigate('/flights', { state: { flights: response.data, tripType } });
    } catch (error) {
      console.error('Error searching flights:', error);
      alert('An error occurred while searching for flights. Please try again.');
    }
  };

  return (
    <div className="flight-search-container">
      <Form onSubmit={handleSubmit} className="flight-search-form">
        <Row>
          <Col md={6}>
            <Form.Group controlId="departure">
              <Form.Label>Departure Airport</Form.Label>
              <Form.Select
                value={departure}
                onChange={(e) => {
                  setDeparture(e.target.value);
                  const selectedAirport = airports.find(a => a.icao_code === e.target.value);
                  if (selectedAirport) {
                    setDepartureTimezone(selectedAirport.timezone);
                  }
                }}
              >
                <option value="">Select departure airport</option>
                {airports.length > 0 ? (
                  airports.map((airport) => (
                    <option key={airport.id} value={airport.icao_code}>
                      {airport.icao_code} - {airport.name}
                    </option>
                  ))
                ) : (
                  <option disabled>No airports available</option>
                )}
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group controlId="arrival">
              <Form.Label>Arrival Airport</Form.Label>
              <Form.Select
                value={arrival}
                onChange={(e) => setArrival(e.target.value)}
              >
                <option value="">Select arrival airport</option>
                {airports.length > 0 ? (
                  airports.map((airport) => (
                    <option key={airport.id} value={airport.icao_code}>
                      {airport.icao_code} - {airport.name}
                    </option>
                  ))
                ) : (
                  <option disabled>No airports available</option>
                )}
              </Form.Select>
            </Form.Group>
          </Col>
        </Row>

        {isWidget && !expanded ? (
          <Button variant="danger" onClick={handleContinue} className="mt-3 w-100">
            Continue
          </Button>
        ) : (
          <>
            <Row className="mt-3">
              <Col md={6}>
                <Form.Group controlId="tripType">
                  <Form.Label>Trip Type</Form.Label>
                  <Form.Select
                    value={tripType}
                    onChange={(e) => setTripType(e.target.value)}
                  >
                    <option value="one-way">One Way</option>
                    <option value="return">Return</option>
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>
            <Row className="mt-3">
              <Col md={6}>
                <Form.Group controlId="departureDate">
                  <Form.Label>Departing Date</Form.Label>
                  <DatePicker
                    selected={departureDate}
                    onChange={(date) => setDepartureDate(date)}
                    minDate={today}
                    className="form-control"
                    dateFormat="MMMM d, yyyy"
                    placeholderText="Select departure date"
                  />
                </Form.Group>
              </Col>
              {tripType === 'return' && (
                <Col md={6}>
                  <Form.Group controlId="returnDate">
                    <Form.Label>Returning Date</Form.Label>
                    <DatePicker
                      selected={returnDate}
                      onChange={(date) => setReturnDate(date)}
                      minDate={departureDate || today}
                      className="form-control"
                      dateFormat="MMMM d, yyyy"
                      placeholderText="Select return date"
                    />
                  </Form.Group>
                </Col>
              )}
            </Row>
            <Row className="mt-3">
              <Col md={6}>
                <Form.Group controlId="flexibleDates">
                  <Form.Check
                    type="checkbox"
                    label="My dates are flexible (+/- 5 days)"
                    checked={flexibleDates}
                    onChange={(e) => setFlexibleDates(e.target.checked)}
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row className="mt-3">
              <Col md={6}>
                <Form.Group controlId="passengers">
                  <Form.Label>Passengers</Form.Label>
                  <Form.Control
                    type="number"
                    value={passengers}
                    onChange={(e) => setPassengers(e.target.value)}
                    min="1"
                  />
                </Form.Group>
              </Col>
            </Row>
            <Button variant="danger" type="submit" className="mt-3 w-100">
              Search Flights
            </Button>
          </>
        )}
      </Form>
    </div>
  );
}

export default FlightSearchForm;