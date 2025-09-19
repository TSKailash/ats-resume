import { BrowserRouter,Routes,Route } from "react-router-dom"
import GeneralHome from "./components/GeneralHome"
import Login from "./components/Login"
import Register from "./components/Register"

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<GeneralHome/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/register" element={<Register/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
