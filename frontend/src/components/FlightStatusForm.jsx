import { Form, Button, Row, Col, ToggleButtonGroup, ToggleButton } from 'react-bootstrap';
import { useState } from 'react';

function FlightStatusForm() {
  const [searchType, setSearchType] = useState('route');

  return (
    <Form className="mt-3">
      <ToggleButtonGroup
        type="radio"
        name="searchType"
        defaultValue="route"
        onChange={(val) => setSearchType(val)}
      >
        <ToggleButton id="tbg-radio-1" value="route" variant="outline-danger">
          By Route
        </ToggleButton>
        <ToggleButton id="tbg-radio-2" value="flightNumber" variant="outline-danger">
          By Flight Number
        </ToggleButton>
      </ToggleButtonGroup>
      {searchType === 'route' ? (
        <Row className="mt-3">
          <Col md={6}>
            <Form.Group controlId="departureAirport">
              <Form.Label>Departure Airport</Form.Label>
              <Form.Control type="text" placeholder="e.g., NZNE (Dairy Flat)" />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group controlId="arrivalAirport">
              <Form.Label>Arrival Airport</Form.Label>
              <Form.Control type="text" placeholder="e.g., YMML (Melbourne)" />
            </Form.Group>
          </Col>
        </Row>
      ) : (
        <Form.Group controlId="flightNumber" className="mt-3">
          <Form.Label>Flight Number</Form.Label>
          <Form.Control type="text" placeholder="e.g., OA101" />
        </Form.Group>
      )}
      <Button variant="danger" type="submit" className="mt-3">
        Check Status
      </Button>
    </Form>
  );
}

export default FlightStatusForm;