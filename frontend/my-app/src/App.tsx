import { useRef } from 'react'
import './App.css'
import MyButton from'./../components/MyButton'

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
      <MyButton label="Add Category" onClick={addCategory} className="btn-add"></MyButton>
    </div>
    <div>
      <MyButton label="Add Sub-Category" onClick={addSubCategory} className="btn-add"></MyButton>
    </div>
    <div>
      <MyButton label="Add Video" onClick={addVideo} className="btn-add"></MyButton>
      <input type='file'
      style={{display: 'none'}}
        ref={fileInputRef}
        />
    </div>
    </>
  )
}

export default App
