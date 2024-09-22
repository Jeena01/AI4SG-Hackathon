
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom"



import Login from './Components/Login/Login';
import Buttons from "./Buttons";

function App() {
  const router= createBrowserRouter([
    {
      path: "/adminlogin",
      element: <Login/>
    },
    {
      path: "/home",
      element: <Buttons/>
    }


  ])


  return (
    <RouterProvider router={router}/>
    
  );
}

export default App;
