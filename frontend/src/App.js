import {BrowserRouter as Router, Route, Routes} from 'react-router-dom'

import './App.css'
import ChatManager from "./components/ChatManager"

export default function App() {
  return (
      <div className={'main'}>
          <Router>
              <Routes>
                  <Route path={'/'} element={<ChatManager />} />
              </Routes>
          </Router>
      </div>
  )
}