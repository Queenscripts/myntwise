import React from "react";

export default function Pagination({
  postsPerPage,
  totalPosts,
  paginateFront,
  paginateBack,
  clickedPageNumber,
  advice,
  paginate
}) {
const pageNumbers= []

if(advice)for(let i = 1; i< Math.ceil(postsPerPage/9)+1; i++){
    pageNumbers.push(i)
  }

  return (
    <div className='py-2'>
      <div>
        <p className='text-sm text-gray-700'>
          Showing 
          <span className='font-medium'> { Math.ceil(advice.slice(1,advice.length).length===9?9*clickedPageNumber:advice[0])}{" "} </span>
          {" "}
          of
          <span className='font-medium'> {totalPosts} </span>
          results
        </p>
      </div>
      <nav className='block'></nav>
      <div>
      <nav aria-label="Page navigation">
        <ul class="inline-flex space-x-2">
        <li>
        <a
              onClick={() => {
                paginateBack();
              }}
              // href='#'
              className='relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50'
            ><button class="flex items-center justify-center w-10 h-10 text-indigo-600 transition-colors duration-150 rounded-full focus:shadow-outline hover:bg-indigo-100">
        <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20"><path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" fill-rule="evenodd"></path></svg></button>
        </a>
        </li>

          <li>
  
          {pageNumbers.slice(clickedPageNumber-1,clickedPageNumber+4).map((number) => (
            
                <button class="w-10 h-10 text-indigo-600 transition-colors duration-150 rounded-full focus:shadow-outline hover:bg-indigo-100"
                  onClick={() => {
                    paginate(number);
                  }}
                  href='#'
                  className={
                    clickedPageNumber === number
                      ? "w-10 h-10 text-white transition-colors duration-150 bg-indigo-600 border border-r-0 border-indigo-600 rounded-full focus:shadow-outline"
                      : "w-10 h-10 text-indigo-600 transition-colors duration-150 rounded-full focus:shadow-outline hover:bg-indigo-100"
                  }
                >
                  
                  {number}
                  </button>
              ))}
          </li>
          <li><a
              onClick={() => {
                paginateFront();
              }}
              // href='#'
              className='relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50'
            ><button class="flex items-center justify-center w-10 h-10 text-indigo-600 transition-colors duration-150 bg-white rounded-full focus:shadow-outline hover:bg-indigo-100">
            <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20"><path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" fill-rule="evenodd"></path></svg></button>
            </a>
          </li>
        </ul>
      </nav>
      </div>
    </div>
  );
}