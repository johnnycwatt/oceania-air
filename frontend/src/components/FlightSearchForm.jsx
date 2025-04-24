import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function FlightSearchForm({ isWidget = false }) {
  // State variables
  const [airports, setAirports] = useState([]); // Initialize as an empty array
  const [departure, setDeparture] = useState(''); // ICAO code of departure airport
  const [arrival, setArrival] = useState(''); // ICAO code of arrival airport
  const [tripType, setTripType] = useState('one-way');
  const [departureDate, setDepartureDate] = useState('');
  const [returnDate, setReturnDate] = useState('');
  const [passengers, setPassengers] = useState(1);
  const [expanded, setExpanded] = useState(!isWidget);

  const navigate = useNavigate();
  const today = new Date().toISOString().split('T')[0];

  // Fetch airports when component mounts
  useEffect(() => {
    const fetchAirports = async () => {
      try {
        const response = await axios.get('/api/flights/airports/');
        // Ensure response.data is an array before setting state
        if (Array.isArray(response.data)) {
          setAirports(response.data);
        } else {
          console.error('Expected an array of airports, but received:', response.data);
          setAirports([]); // Fallback to empty array
        }
      } catch (error) {
        console.error('Error fetching airports:', error);
        setAirports([]); // Fallback to empty array on error
      }
    };
    fetchAirports();
  }, []); // Empty dependency array to run once on mount

  // Handle "Continue" button in widget mode
  const handleContinue = () => {
    if (!departure || !arrival) {
      alert('Please select departure and arrival airports.');
      return;
    }
    setExpanded(true);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validation
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
      // Prepare API parameters with ICAO codes
      const params = {
        origin: departure,
        destination: arrival,
        date: departureDate,
        passengers,
      };
      if (tripType === 'return') {
        params.returnDate = returnDate;
      }

      // Make API call
      const response = await axios.get('/api/flights/flights', { params });

      // Navigate to flight list page
      navigate('/flights', { state: { flights: response.data, tripType } });
    } catch (error) {
      console.error('Error searching flights:', error);
      alert('An error occurred while searching for flights. Please try again.');
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Row>
        <Col md={6}>
          <Form.Group controlId="departure">
            <Form.Label>Departure Airport</Form.Label>
            <Form.Select
              value={departure}
              onChange={(e) => setDeparture(e.target.value)}
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
        <Button variant="secondary" onClick={handleContinue} className="mt-3">
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
                <Form.Control
                  type="date"
                  value={departureDate}
                  onChange={(e) => setDepartureDate(e.target.value)}
                  min={today}
                />
              </Form.Group>
            </Col>
            {tripType === 'return' && (
              <Col md={6}>
                <Form.Group controlId="returnDate">
                  <Form.Label>Returning Date</Form.Label>
                  <Form.Control
                    type="date"
                    value={returnDate}
                    onChange={(e) => setReturnDate(e.target.value)}
                    min={departureDate || today}
                  />
                </Form.Group>
              </Col>
            )}
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
          <Button variant="primary" type="submit" className="mt-3">
            Search Flights
          </Button>
        </>
      )}
    </Form>
  );
}

export default FlightSearchForm;