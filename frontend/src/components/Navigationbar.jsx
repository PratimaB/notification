import { Link } from "react-router-dom";
import "./Navigationbar.css";
import logo from "../assets/logo.jpg";

function Navigationbar() {
    return (
        <nav className="navbar">
            <div className="navbar-logo">
                <img src={logo} alt="Logo" className="logo" />
                <span className="app-name">SRX</span>
            </div>
            <ul className="navbar-links">
                <li><a href="/">Login</a></li>
                <Link to="/register">Register</Link>
                <Link to="/about">About</Link>
            </ul>
        </nav>
    );
}
export default Navigationbar