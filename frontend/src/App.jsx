import React from 'react'
import Navbar from './components/Navbar';

const App = () => {
  const handleHandle=()=>{
    console.log("Handle")
  }
  console.log(name);
  return (
    <div>
      <Navbar func={handleHandle}/>
      
    </div>
  )
}

export default App
