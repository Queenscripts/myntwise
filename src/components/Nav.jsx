import React from 'react';
import { Transition } from "@headlessui/react";
import {
 
  useLocation, 
  
} from "react-router-dom";
function Header(){
    return(
        <div class="py-20 relative h-65 overflow-hidden" 
        style={{
                backgroundSize: "cover",
                backgroundPosition: "center",
                backgroundRepeat: "no-repeat",
                backgroundAttachment: "fixed",
                backgroundImage: "linear-gradient(7deg, #9b1aacdb 0%, #089280a6 100%), url(../static/img/biteyes.jpg)"}}>
        <h2 class="text-4xl font-bold mb-2 text-white" style={{padding: "0 40px"}}>
            Make Smart Money Choices 
            {/* {% if user %}{{user.name}} {% endif %} */}
        </h2>
        <h3 class="text-2xl mb-8 text-gray-200"  style={{padding: "0 40px"}}>
          Monitor your finances and get suggestions on what to buy next.
        </h3>
    <div class="container mx-10 " onClick={()=>{console.log("clicking")}}>
    { user?
      <button onClick={()=>location="/dashboard#advice"} class="bg-white font-bold rounded-full py-4 px-8 shadow-lg uppercase tracking-wider">
        Get Deals
      </button> :
      <button  onClick={()=>location="/login"} class="bg-white font-bold rounded-full py-4 px-8 shadow-lg uppercase tracking-wider">
        Login
      </button>
    }
  </div>
        </div>
    )
}
export default function Nav(props){
  let location = useLocation()

  const [isOpen, setIsOpen] = React.useState(false);
  return( 
        <>
        
        <nav className="bg-teal-500 sticky top-0" style={{zIndex: 1}}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 w-full">
            <div className="flex items-center w-full">
              <div className="flex flex-shrink-0">
                <a className="flex flex-shrink-0" href="/">
                <img src="./static/favicon_io/favicon-16x16.png"/>
                <span className="self-center text-lg font-semibold whitespace-nowrap text-white">MyntWise </span>
                </a>
              </div>
              <div className="hidden md:block w-full">
                <div className="ml-10 flex items-center space-x-4" style={{justifyContent: "end"}}>
                  { props.user &&
                  <>
                  
                  <a
                    href="/dashboard"
                    className={location.pathname=='/dashboard'? "hover:text-gray-300 text-white px-3 py-2 rounded-md text-sm font-medium": "hover:text-white text-gray-300 focus:text-white px-3 py-2 rounded-md text-sm font-medium"}
                  >
                    Dashboard
                  </a>

                  <a
                    href="/budgets"
                    className={location.pathname=='/budgets'? "hover:text-gray-300 text-white px-3 py-2 rounded-md text-sm font-medium": "hover:text-white text-gray-300 focus:text-white px-3 py-2 rounded-md text-sm font-medium"}
                  >
                    Budgets
                  </a>
                  </>
                  }

                  <a
                    href="/about"
                    className={location.pathname=='/about'? "hover:text-gray-300 text-white px-3 py-2 rounded-md text-sm font-medium": "hover:text-white text-gray-300 focus:text-white px-3 py-2 rounded-md text-sm font-medium"}
                  >
                    About
                  </a>

                  {
              props.user ?
            
                <a href="/logout" className="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white lg:mt-0">Logout</a>
            : 
            
                  <a href="/signup" className="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white lg:mt-0">Signup</a>
            
            }
                </div>
              </div>
            </div>
            <div className="-mr-2 flex md:hidden">
              <button
                onClick={() => setIsOpen(!isOpen)}
                type="button"
                className="bg-transparent inline-flex items-center justify-center p-2 rounded-md text-gray-900 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
                aria-controls="mobile-menu"
                aria-expanded="false"
              >
                <span className="sr-only">Open main menu</span>
                {!isOpen ? (
                  <svg
                    className="block h-6 w-6"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M4 6h16M4 12h16M4 18h16"
                    />
                  </svg>
                ) : (
                  <svg
                    className="block h-6 w-6"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                )}
              </button>
            </div>
          </div>
        </div>

        <Transition
          show={isOpen}
          enter="transition ease-out duration-100 transform"
          enterFrom="opacity-0 scale-95"
          enterTo="opacity-100 scale-100"
          leave="transition ease-in duration-75 transform"
          leaveFrom="opacity-100 scale-100"
          leaveTo="opacity-0 scale-95"
        >
          {(ref) => (
            <div className="md:hidden" id="mobile-menu">
              <div ref={ref} className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                { props.user &&
                <>
                <a
                  href="/dashboard"
                  className=" text-gray-300 active:text-white block px-3 py-2 rounded-md text-base font-medium"
                >
                  Dashboard
                </a>

                <a
                  href="/budgets"
                  className="text-gray-300  hover:text-white block px-3 py-2 rounded-md text-base font-medium"
                >
                  Budgets
                </a>
                </>
                }
                <a
                  href="/about"
                  className="text-gray-300  hover:text-white block px-3 py-2 rounded-md text-base font-medium"
                >
                  About
                </a>
                {
              props.user ?
            
                <a href="/logout" className="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white lg:mt-0">Logout</a>
            : 
            
                  <a href="/signup" className="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white lg:mt-0">Signup</a>
            
            }
              </div>
              
            </div>
          )}
        </Transition>
      </nav>
        <Header/>
        </>
  )
}
  
// const domContainer = document.querySelector('#nav');
// ReactDOM.render(React.createElement(Nav, {"user":user}), domContainer);

