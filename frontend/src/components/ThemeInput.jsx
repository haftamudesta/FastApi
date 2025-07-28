import {useState} from 'react'

const ThemeInput = ({OnSubmit}) => {
        const [theme,setTheme]=useState("")
        const [error,setError]=useState("")

        const handleSubmitt=(e)=>{
                e.preventDefault()
                if (!theme.trim()){
                        setError("Please enter a theme name!")
                        return
                }
                OnSubmit(theme)
        }
  return (
    <div className=''>
        <h2>Generate Your adventure</h2>
        <p>Enter a theme for your interactive story</p>
        <form onSubmit={handleSubmitt}>
                <div className=''>
                        <input 
                        type="text" 
                        value={theme}
                        onChange={(e)=>setTheme(e.target.value)}
                       placeholder='Enter a theme(e.g space,medieval...'
                       className={error?'text-red-500 border-red-500':''}
                        />
                        {error&& <p className='text-red-600 font-bold'>{error}</p>}
                </div>
                <button type='submit' className='text-white bg-blue-700'>Generate Story</button>
        </form>
    </div>
  )
}

export default ThemeInput
