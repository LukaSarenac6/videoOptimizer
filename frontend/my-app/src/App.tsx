import { useRef } from 'react'
import './App.css'

function App() {
  
  const fileInputRef = useRef<HTMLInputElement>(null)

  function addCategory() {
    console.log("cat")
  }

  function addSubCategory() {
    console.log("sub-cat")
  }

  function addVideo() {
    fileInputRef.current?.click()
  }

  return (
    <>
    <div>
      <button className="btn-add" onClick={addCategory}>Add Category</button>
    </div>
    <div>
      <button className="btn-add" onClick={addSubCategory}>Add Sub-Category</button>
    </div>
    <div>
      <button className="btn-add" onClick={addVideo}>Add Video</button>
      <input type='file'
      style={{display: 'none'}}
        ref={fileInputRef}
        />
    </div>
    </>
  )
}

export default App
