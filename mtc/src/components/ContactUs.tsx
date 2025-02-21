import React from 'react';
import './ContactUs.css';

interface ContactUsProps {
  onBackClick: () => void;
}

export default function ContactUs({ onBackClick }: ContactUsProps) {
  return (
    <div className="contact-us">
      <h1>Contact Us</h1>
      <form>
        <div className="form-group">
          <input type="text" id="name" name="name" placeholder="Name" required />
        </div>
        <div className="form-group">
          <input type="email" id="email" name="email" placeholder="Email" required />
        </div>
        <div className="form-group">
          <input type="tel" id="phone" name="phone" placeholder="Phone" required />
        </div>
        <div className="form-group">
          <input type="text" id="company" name="company" placeholder="Company" required />
        </div>
        <div className="form-group">
          <textarea id="message" name="message" placeholder="Message" required></textarea>
        </div>
        <button type="submit">Submit</button>
        <button type="button" onClick={onBackClick}>Home</button>
      </form>
    </div>
  );
}