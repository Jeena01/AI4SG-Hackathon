import {useState} from "react";

import "./App.css";
import { Modal } from "./components/Modal";
import { Table } from "./components/Table"; 

function App () { 


  return (
     <div className="App">
    <Table />
    <Modal />
    </div>
  );
  
}
export default App; 