function Nav(props){
  // const [cookies, setCookies] = React-cookies.useCookies()
  console.log(props)
  return( 
 
        <ul className="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
            <div class="container flex flex-wrap justify-between items-center mx-auto">
            <a href="/" class="flex">
                <img src="./static/favicon_io/favicon-16x16.png"/>
                <span class="self-center text-lg font-semibold whitespace-nowrap text-white">MyntWise </span>
            </a>
            </div>
          
            <li className="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white mr-4">
                <a href="/dashboard">
                    Dashboard 
                </a>
            </li>
            { props.user  &&
              <li className="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white mr-4">
                  <a href="/budgets">
                      Budgets
                  </a>
              </li>
            }          
            <li className="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white mr-4">
                  <a href="/about">
                      About
                  </a>
              </li>
           
            {/* <li className="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white mr-4">
                <a href="/savings">
                    Savings
                </a>
            </li> */}
            {
              props.user ?
              <li>
                <a href="/logout" className="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white mt-4 lg:mt-0">Logout</a>
              </li> : 
              <li>
                  <a href="/signup" className="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white mt-4 lg:mt-0">Signup</a>
              </li> 
            }

        </ul>
  )
}
  
// console.log(session['user_email'])
const domContainer = document.querySelector('#nav');
ReactDOM.render(React.createElement(Nav, {"user":user}), domContainer);

