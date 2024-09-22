
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom"



import Login from './Components/Login/Login';
import Buttons from "./Buttons";
import Layout from "./Layout";

function App() {
  const router= createBrowserRouter([
    {
      element: <Layout/>,
      children: [
        {
          path: "/adminlogin",
          element: <Login/>
        },
        {
          path: "/home",
          element: <Buttons/>
        }
        
      ]
    }
    


  ])


  return (
    <RouterProvider router={router}/>
    
  );
}

export default App;
