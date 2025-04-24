import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CustomNavbar from './components/Navbar';
import LandingPage from './components/LandingPage';
import FlightSearch from './components/FlightSearch';
import ManageBooking from './components/ManageBooking';
import FlightStatus from './components/FlightStatus';
import FlightSearchForm from './components/FlightSearchForm';
import FlightList from './components/FlightList';

function App() {
  return (
    <Router>
      <CustomNavbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/search" element={<FlightSearch />} />
        <Route path="/flights" element={<FlightList />} />
        <Route path="/manage" element={<ManageBooking />} />
        <Route path="/status" element={<FlightStatus />} />
      </Routes>
    </Router>
  );
}

export default App;