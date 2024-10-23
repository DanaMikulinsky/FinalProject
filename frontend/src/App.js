import {BrowserRouter as Router, Route, Routes} from 'react-router-dom'

import './App.css';
import Chat from "./components/Chat";
import ChatManager from "./components/ChatManager";

export default function App() {
  return (
      <div className={'main'}>
          <Router>
              <Routes>
                  <Route path={'/'} element={<ChatManager />} />
                  <Route path='/chat' element={<Chat/>}/>
              </Routes>
          </Router>
      </div>
  )
}