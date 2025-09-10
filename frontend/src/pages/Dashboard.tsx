import React from 'react';
import { useAuth } from '../hooks/useAuth';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();

  const getRoleBasedContent = () => {
    switch (user?.role) {
      case 'Student':
        return (
          <div className="row">
            <div className="col-md-4">
              <div className="card mb-3">
                <div className="card-body">
                  <h5 className="card-title">Course Registration</h5>
                  <p className="card-text">Register for courses and electives</p>
                  <button className="btn btn-primary">Register</button>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card mb-3">
                <div className="card-body">
                  <h5 className="card-title">View Attendance</h5>
                  <p className="card-text">Check your attendance records</p>
                  <button className="btn btn-info">View</button>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card mb-3">
                <div className="card-body">
                  <h5 className="card-title">Fee Payment</h5>
                  <p className="card-text">Pay your semester fees</p>
                  <button className="btn btn-success">Pay Now</button>
                </div>
              </div>
            </div>
          </div>
        );
      case 'Faculty':
        return (
          <div className="row">
            <div className="col-md-4">
              <div className="card mb-3">
                <div className="card-body">
                  <h5 className="card-title">Mark Attendance</h5>
                  <p className="card-text">Log student attendance</p>
                  <button className="btn btn-primary">Mark</button>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card mb-3">
                <div className="card-body">
                  <h5 className="card-title">Leave Management</h5>
                  <p className="card-text">Apply for leaves</p>
                  <button className="btn btn-warning">Apply</button>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card mb-3">
                <div className="card-body">
                  <h5 className="card-title">View Timetable</h5>
                  <p className="card-text">Check your class schedule</p>
                  <button className="btn btn-info">View</button>
                </div>
              </div>
            </div>
          </div>
        );
      case 'Admin':
        return (
          <div className="row">
            <div className="col-md-4">
              <div className="card mb-3">
                <div className="card-body">
                  <h5 className="card-title">Manage Applications</h5>
                  <p className="card-text">Review admission applications</p>
                  <button className="btn btn-primary">Manage</button>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card mb-3">
                <div className="card-body">
                  <h5 className="card-title">HR Management</h5>
                  <p className="card-text">Manage employees and leaves</p>
                  <button className="btn btn-info">Manage</button>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card mb-3">
                <div className="card-body">
                  <h5 className="card-title">Finance Reports</h5>
                  <p className="card-text">View financial reports</p>
                  <button className="btn btn-success">View</button>
                </div>
              </div>
            </div>
          </div>
        );
      default:
        return (
          <div className="row">
            <div className="col">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">Welcome to University ERP</h5>
                  <p className="card-text">Your role: {user?.role}</p>
                </div>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="container mt-4">
      <div className="row mb-4">
        <div className="col">
          <div className="d-flex justify-content-between align-items-center">
            <h2>Dashboard</h2>
            <div>
              <span className="me-3">Welcome, {user?.first_name} {user?.last_name}</span>
              <button className="btn btn-outline-danger" onClick={logout}>
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
      {getRoleBasedContent()}
    </div>
  );
};

export default Dashboard;
