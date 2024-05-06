import { useState } from "react";
import SignUp from "./pages/auth/signup";
import Login from "./pages/auth/login";
import { createBrowserRouter } from "react-router-dom";
import ErrorPage from "./pages/ErrorPage";
import Dashboard from './pages/main/HomePage'

const router = createBrowserRouter([
  {
    path: "/",
    element: <SignUp />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/login",
    element: <Login />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/dashboard",
    element: <Dashboard />,
    errorElement: <ErrorPage />,
  },
]);

export default router;
