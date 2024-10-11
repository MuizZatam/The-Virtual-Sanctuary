import React from 'react'
import githubIcon from '../assets/github-icon.svg'

function Contribute() {
  return (
    <button style={{backgroundColor: "", color: "#ffffff", fontSize: "22px"}} className='flex max-w-[200px] ml-12  p-2.5 justify-between align-middle bg-slate-900 hover:bg-slate-700 items-center border rounded-xl shadow-md'>
        <p className='text-xl'>Contribute</p>
        <div className='mx-2'><img src={githubIcon} alt="github-icon" /></div>
    </button>
  )
}

export default Contribute