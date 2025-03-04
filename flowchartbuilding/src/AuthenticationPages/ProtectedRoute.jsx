import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../authentication_pages/AuthContext"

const ProtectedRoute = ({ element: Component, ...rest }) => {
  const { isAuthenticated } = useContext(AuthContext);

  return isAuthenticated ? (
    <Component {...rest} />
  ) : (
    <Navigate to="/login" replace />
  );
};

export default ProtectedRoute;