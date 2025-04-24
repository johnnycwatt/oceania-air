import { Container, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function QuickAccessMobile() {
  return (
    <Container className="mt-5">
      <Button variant="outline-danger" as={Link} to="/search" className="w-100 mb-3">
        Search Flights
      </Button>
      <Button variant="outline-danger" as={Link} to="/manage" className="w-100 mb-3">
        Manage Booking
      </Button>
      <Button variant="outline-danger" as={Link} to="/status" className="w-100">
        Flight Status
      </Button>
    </Container>
  );
}

export default QuickAccessMobile;