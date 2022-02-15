import React from "react";

export default function Saved(props) {
  const [saved, setSaved] = React.useState(null);
  
    React.useEffect(() => {

      // Extract separate fetch call in new API request file

      fetch(`/api/saved`).then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            throw new Error("something's wrong...");
          }
      }).then(
          (resjson)=>{
           setSaved(resjson)
          }
        ).catch(
          error=>{console.log(error)}
        )
    }, [])
 
  React.useEffect(()=>{
    
  },[])



  return (
    <div class="flex flex-col p-4">
      {/* <section class="flex align-center items-center">
        <div class="flex">
          <div class="">
            <div class="input-group relative flex flex-wrap items-stretch w-full">
              <input type="search" class="form-control relative flex-auto min-w-0 block w-full px-3 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none" placeholder="Search" aria-label="Search" aria-describedby="button-addon2"/>
              <button class="btn inline-block px-6 bg-blue-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700  focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out flex items-center" type="button" id="button-addon2">
                <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="search" class="w-4" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                  <path fill="currentColor" d="M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </section> */}
      <div class="my-1 px-10 w-full grid grid-cols-3 p-50 gap-5">
        {/* Sort Search Section */}
        {/* Advice Card */}
        { saved && user && saved.length>0 ? saved.map( product=> {return(
        <article class="flex flex-col overflow-hidden rounded-lg shadow-lg">
       
            <a
              target="_blank"
              href="https://www.walmart.com/search?q={{product.advice_info_id}}"
            >
              <img
                alt="Placeholder"
                class="block h-auto w-full"
                src={product.img}
              />
            </a>

            <header class="flex direct flex-col justify-between leading-tight p-1">
              <h3 id="price" class="text-grey-darker text-md font-black p-2">
                ${product.price}
              </h3>
              <h2 class="text-md p-2">
                <a
                  class="no-underline hover:underline text-black font-medium"
                  target="_blank"
                  href="https://www.walmart.com/search?q={{product.advice_info_id}}"
                >
                  {product.name}
                </a>
              </h2>
            </header>

            <footer class="flex flex-col items-center justify-between leading-none p-1">
              {/* <ReadMore>
                {product.advice_description}
              </ReadMore> */}
              <p class="ml-2 text-sm p-2">
                {/* {% set budget_count = namespace(value=0) %} */}

                {/* {% for budget in budgets%} */}

                {/* <!-- {{budget.budget_amount}} --> */}
              </p>
              <p class="formula ml-2 text-sm p-2">
                {/* {% if percentages[budget_count.value][count.value] >100 %}  */}
                {/* <span class="text-red-500"> {{percentages[budget_count.value][count.value]}}%  </span>
            of your {{budget.budget_frequency}} {{budget.budget_name}}budget</p>
            {% elif percentages[budget_count.value][count.value] < 100 and percentages[budget_count.value][count.value] > 50 %}
            <span class="text-yellow-500"> {{percentages[budget_count.value][count.value]}}%</span>
            of your {{budget.budget_frequency}} {{budget.budget_name}} budget</p>
            {% else %}
            <span class="text-green-500"> {{percentages[budget_count.value][count.value]}}%</span>
            of your {{budget.budget_frequency}} {{budget.budget_name}} budget</p>
            {% endif %}
          {% set budget_count.value = budget_count.value + 1 %}

          {% endfor %}
          
          {% set count.value = count.value + 1 %} */}
              </p>
            </footer>
          </article>)}): 
          <div class="container mx-auto px-4 flex flex-col lg:flex-row">
            <div class="juice relative lg:w-2/3 rounded-xl bg-secondary-lite bg-cover p-8 md:p-16 bg-gradient-to-r from-cyan-500 to-blue-500" style={{backgroundImage:"url(./static/img/conifer-payment-processed-1.png)"}}>
              <p class="max-w-sm text-secondary text-3xl md:text-4xl font-semibold" style={{background:"#f5eaf9"}}>You have no transactions, so no advice to show!</p>
              <a href="/dashboard#transactions"><button class="mt-20 bg-white font-semibold px-8 py-2 rounded">Start by creating transactions now</button></a>
            </div>
          </div>}
      </div>
   
    </div>
  )
}
