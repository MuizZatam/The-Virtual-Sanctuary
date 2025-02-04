import React from 'react'
import searchIcon from '../assets/search-icon.svg'

function SearchBar() {
  return (
    <div className='py-12'>
      <label class="relative block">
        <span class="sr-only">Search</span>
        <span class="absolute inset-y-0 left-0 flex items-center pl-2">
          <img  src={searchIcon} class="h-5 w-5 fill-slate-500" viewBox="0 0 20 20"></img>
        </span>
      <input class="min-h-12 min-w-64 placeholder:italic placeholder:text-slate-600 block bg-white w-full border border-slate-300 rounded-md py-2 pl-9 pr-3 shadow-sm focus:outline-none focus:border-sky-300 focus:ring-sky-300 focus:ring-1 sm:text-lg" placeholder="Search for anything..." type="text" name="search"/>
      </label>
    </div>
  )
}

export default SearchBar