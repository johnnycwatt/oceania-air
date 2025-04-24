import { Container } from 'react-bootstrap';
import FlightSearchForm from './FlightSearchForm.jsx';
function FlightSearch() {
  return (
    <Container className="mt-5">
      <h2>Search Flights</h2>
      <FlightSearchForm />
    </Container>
  );
}

export default FlightSearch;