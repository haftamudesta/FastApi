import { BrowserRouter,Routes,Route,Router } from 'react-router-dom'
import './App.css'
import StoryLoader from './components/StoryLoader'

function App() {
  
  return (
    <>
      <header>Interactive Story Generator</header>
      <main>
        <Routes>
          <Route path={'/story/:id'} element={<StoryLoader />} />
        </Routes>
      </main>
    </>
  )
}

export default App
