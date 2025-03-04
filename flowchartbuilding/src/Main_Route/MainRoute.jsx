import { Route, Routes } from 'react-router-dom';
import RegisterPage from '../authentication_pages/RegisterPage';
import LoginPage from '../authentication_pages/LoginPage';
import Controller from '../admin_control_page/controller';
import IndexPage from '../index_page/index';
import OperatorControl from '../operator_control/operator_control';
import ProtectedRoute from '../authentication_pages/ProtectedRoute'; // Import the ProtectedRoute component

const MainRoute = () => {
    return (
        <Routes>
            <Route path="*" element={<IndexPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route
                path="/admin-panel"
                element={<ProtectedRoute element={Controller} />} // Protect the Controller component
            />
            <Route
                path="/operator-control"
                element={<ProtectedRoute element={OperatorControl} />} // Protect the OperatorControl component
            />
        </Routes>
    );
};

export default MainRoute;