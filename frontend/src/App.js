import {BrowserRouter as Router, Route, Routes} from 'react-router-dom'

import './App.css';
import Chat from "./components/Chat";

export default function App() {
  return (
      <div className={'main'}>
          <Router>
              <Routes>
                  <Route path='/chat' element={<Chat/>}/>
              </Routes>
          </Router>
      </div>
  )
}