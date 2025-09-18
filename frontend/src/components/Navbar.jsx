import React from 'react'

const Navbar = (prop) => {

    const fun = prop.func;
  return (
    <div>
      <h1 className='bg-amber-950'>"Hello"</h1>
      <button onClick={fun}>click</button>
    </div>
  )
}

export default Navbar
