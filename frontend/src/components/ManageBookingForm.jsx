import { Form, Button, Row, Col } from 'react-bootstrap';

function ManageBookingForm() {
  return (
    <Form className="mt-3">
      <Row>
        <Col md={6}>
          <Form.Group controlId="referenceNumber">
            <Form.Label>Reference Number</Form.Label>
            <Form.Control type="text" placeholder="Your Reference Number" />
          </Form.Group>
        </Col>
        <Col md={6}>
          <Form.Group controlId="email">
            <Form.Label>Email Address</Form.Label>
            <Form.Control type="email" placeholder="Your Email" />
          </Form.Group>
        </Col>
      </Row>
      <Button variant="danger" type="submit" className="mt-3">
        Manage Booking
      </Button>
    </Form>
  );
}

export default ManageBookingForm;