import { Container } from 'react-bootstrap';
import FlightSearchForm from './FlightSearchForm';


function LandingPage() {
  return (
    <Container className="mt-5">
      <h1>Welcome to Oceania Air</h1>
      <p>Plan your next journey with us.</p>
      <FlightSearchForm isWidget={true} />
    </Container>
  );
}

export default LandingPage;