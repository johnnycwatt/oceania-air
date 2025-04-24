import { Tabs, Tab, Container } from 'react-bootstrap';
import FlightSearchForm from './FlightSearchForm';
import ManageBookingForm from './ManageBookingForm';
import FlightStatusForm from './FlightStatusForm';

function QuickAccessTabs() {
  return (
    <Container className="mt-5">
      <Tabs defaultActiveKey="search" id="quick-access-tabs" className="mb-3">
        <Tab eventKey="search" title="Search Flights">
          <FlightSearchForm />
        </Tab>
        <Tab eventKey="manage" title="Manage Booking">
          <ManageBookingForm />
        </Tab>
        <Tab eventKey="status" title="Flight Status">
          <FlightStatusForm />
        </Tab>
      </Tabs>
    </Container>
  );
}

export default QuickAccessTabs;