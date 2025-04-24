import {Form, Button, Row, Col} from 'react-bootstrap';

function FlightSearchForm(){
  return (
    <Form className="mt-3">
      <Row>
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
      <Row className="mt-3">
        <Col md={3}>
          <Form.Group controlId="tripType">
            <Form.Label>Trip Type</Form.Label>
            <Form.Select>
              <option>One Way</option>
              <option>Return</option>
            </Form.Select>
          </Form.Group>
        </Col>
        <Col md={3}>
          <Form.Group controlId="departureDate">
            <Form.Label>Departure Date</Form.Label>
            <Form.Control type="date" />
          </Form.Group>
        </Col>
        <Col md={3}>
          <Form.Group controlId="returnDate">
            <Form.Label>Return Date</Form.Label>
            <Form.Control type="date" />
          </Form.Group>
        </Col>
        <Col md={3}>
          <Form.Group controlId="passengers">
            <Form.Label>Passengers</Form.Label>
            <Form.Control type="number" min="1" defaultValue="1" />
          </Form.Group>
        </Col>
      </Row>
      <Button variant="danger" type="submit" className="mt-3">
        Search Flights
      </Button>
    </Form>
  );
}

export default FlightSearchForm;