import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Navbar from './components/Navbar';

// Pages
const Home = () => <div className="container mt-5"><h1>Welcome to Caroni Trading</h1></div>;
const StockScanner = () => <div className="container mt-5"><h1>Stock Scanner</h1></div>;

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/scanner',
    element: <StockScanner />,
  },
]);

const App = () => (
  <>
    <Navbar />
    <RouterProvider router={router} />
  </>
);

export default App;
