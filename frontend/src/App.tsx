import { useState } from "react";
import SignUp from "./pages/auth/signup";
import Login from "./pages/auth/login";
import { createBrowserRouter } from "react-router-dom";
import ErrorPage from "./pages/ErrorPage";
import Dashboard from "./pages/main/HomePage";
import Budget from "./pages/main/Budget";
import Expenses from "./pages/main/Expenses";
import Income from "./pages/main/Income";

const router = createBrowserRouter([
  {
    path: "/sign-up",
    element: <SignUp />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/",
    element: <Login />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/dashboard",
    element: <Dashboard />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/budgets",
    element: <Budget />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/expenses",
    element: <Expenses />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/income",
    element: <Income />,
    errorElement: <ErrorPage />,
  },
]);

export default router;
