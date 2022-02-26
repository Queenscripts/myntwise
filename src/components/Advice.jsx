import React from "react";
import Pagination from "./Dashboard/Pagination";
import Modal from "./Dashboard/Modal";

function Slider (props){
  
  const {min, max, onChange, visible} = props
  const [minVal, setMinVal] = React.useState(min);
  const [maxVal, setMaxVal] = React.useState(max);
  const minValRef = React.useRef(min);
  const maxValRef = React.useRef(max);
  const range = React.useRef(null);

  // Convert to percentage
  const getPercent = React.useCallback(
    (value) => Math.round(((value - min) / (max - min)) * 100),
    [min, max]
  );

  // Set width of the range to decrease from the left side
  React.useEffect(() => {
    const minPercent = getPercent(minVal);
    const maxPercent = getPercent(maxValRef.current);

    if (range.current) {
      range.current.style.left = `${minPercent}%`;
      range.current.style.width = `${maxPercent - minPercent}%`;
    }
  }, [minVal, getPercent]);

  // Set width of the range to decrease from the right side
  React.useEffect(() => {
    const minPercent = getPercent(minValRef.current);
    const maxPercent = getPercent(maxVal);

    if (range.current) {
      range.current.style.width = `${maxPercent - minPercent}%`;
    }
  }, [maxVal, getPercent]);

  // Get min and max values when their state changes
  React.useEffect(() => {
    onChange({ min: minVal, max: maxVal });
  }, [minVal, maxVal, onChange]);
 
  return(
    <div className="sliderContainer">
    <input
      type="range"
      min={min}
      max={max}
      value={minVal}
      onChange={(event) => {
        const value = Math.min(Number(event.target.value), maxVal - 1);
        setMinVal(value);
        minValRef.current = value;
      }}
      className="thumb thumb--left"
      style={{ zIndex: minVal > max - 100 && "5" }}
    />
    <input
      type="range"
      min={min}
      max={max}
      value={maxVal}
      onChange={(event) => {
        const value = Math.max(Number(event.target.value), minVal + 1);
        setMaxVal(value);
        maxValRef.current = value;
      }}
      className="thumb thumb--right"
    />

    <div className="slider">
      <div className="slider__track" />
      <div ref={range} className="slider__range" />
      <div className="slider__left-value">{minVal}</div>
      <div className="slider__right-value">{maxVal}</div>
    </div>
    </div>
  )

}
const ReadMore = ({ children }) => {
  const text = children;
  const [isReadMore, setIsReadMore] = React.useState(true);
  const toggleReadMore = () => {
    setIsReadMore(!isReadMore);
    return false
  };
  return (
    <p class="ml-2 text-sm p-2 truncate-2-lines">
      {isReadMore && text ? text.slice(0, 100) : text}
      <span onClick={toggleReadMore} className="read-or-hide text-orange-600" style={{cursor: "pointer"}} href="#"> 
        {isReadMore ? " ...read more" : " show less"}
      </span>
    </p>
  );
};
export default function Advice(props) {
  const [message, setMessage] = React.useState("Added!")
  const [open, setOpen] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [advice, setAdvice] = React.useState(null);
  const [filteredAdvice, setFilteredAdvice] = React.useState(advice)
  const [allPrices, setAllPrices] = React.useState(null);
  const [minPrice, setMinPrice] = React.useState(null);
  const [maxPrice, setMaxPrice] = React.useState(null);
  const [pageNumber, setPageNumber] = React.useState(null);
  const [searchVal, setSearchVal] = React.useState(null);
  const [visible, setVisible] = React.useState(false);
  const [currentPage, setCurrentPage] = React.useState(1)
  const [clickedPageNumber, setClickedPageNumber] = React.useState(1);
  const indexOfLast = clickedPageNumber * 9
  const indexOfFirst = indexOfLast - 9
  const paginate = (clickedPageNumber)=>setClickedPageNumber(clickedPageNumber)
   // Change page
  const paginateFront = () => setClickedPageNumber(clickedPageNumber + 1);
  const paginateBack = () => setClickedPageNumber(clickedPageNumber - 1);
  if(props.user){
    React.useEffect(() => {

      // Extract separate fetch call in new API request file

      fetch(`/api/user/advice?page=${clickedPageNumber?clickedPageNumber:1}`).then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            throw new Error("something's wrong...");
          }
      }).then(
          (resjson)=>{
           setAdvice(resjson)
           setFilteredAdvice(resjson)
          }
        ).catch(
          error=>{console.log(error)}
        )
    }, []);
    React.useEffect(() => {
      // Extract separate fetch call in new API request file

      fetch(`/api/user/advice?page=${clickedPageNumber?clickedPageNumber:1}`).then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            throw new Error("something's wrong...");
          }
      }).then(
          (resjson)=>{
           setAdvice(resjson)
           setFilteredAdvice(resjson)
          }
        ).catch(
          error=>{console.log(error)}
        )
    }, [clickedPageNumber]);
  } else{
    React.useEffect(() => {
    // Extract separate fetch call in new API request file
    fetch(`/api/advice?page=${clickedPageNumber}`).then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          throw new Error("something's wrong...");
        }
    }).then(
        (resjson)=>{
         setAdvice(resjson)
         setFilteredAdvice(resjson)
        }
    ).catch(
        error=>{console.log(error)}
    )
  }, [clickedPageNumber]);}

  // Fetch for all price max and in value
  React.useEffect(() => {
    // Extract separate fetch call in new API request file
    fetch(`/api/advice`).then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          throw new Error("something's wrong...");
        }
    }).then(
        (resjson)=>{
          setPageNumber(parseInt(resjson.length))
          setAllPrices(resjson)
        }
    ).catch(
        error=>{console.log(error)}
    )
  }, []);

  // Save Advice as unprocessed transaction
  const saveAdvice=(id)=>{
    const clickedSave = advice.filter(i=>i.advice_id==id)
    let user_transactions_name= clickedSave[0].advice_name
    let user_transactions_amount = clickedSave[0].advice_price
    let user_transactions_date = new Date(Date.now()).toISOString()
    let user_transactions_processed = false 
    let budget = null
    let category = null
    let img = clickedSave[0].advice_img
    let data={
    user_transactions_name,
    user_transactions_amount,
    user_transactions_date,
    budget, 
    category,
    user_id:user, 
    user_transactions_processed,
    img
    }
    const saveNewAdvice = async()=>{
    const res = await fetch('/api/transactions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (res.ok) {
    } else {
      throw new Error(`${res.status} ${res.statusText}`);
    }
    }
    saveNewAdvice()
  }

  React.useEffect(()=>{
    let filtered
    function filterByValue(array, string) {
      return array.filter(o =>
          Object.keys(o).some(k => o[k].toLowerCase().includes(string.toLowerCase())));
    }
    if(advice && allPrices) filtered =filterByValue(allPrices, searchVal)

    if(filtered && filtered.length>0){setFilteredAdvice(filtered)}
    if(searchVal=="" && advice) setFilteredAdvice(advice)
  },[searchVal])
  
  const showSortOptions=()=>{
    setVisible(!visible)
  }

  const filterAdvicePrice=()=>{
    fetch(`/api/advice/price?min=${minPrice}&max=${maxPrice}`).then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          throw new Error("something's wrong...");
        }
    }).then(
        (resjson)=>{
         setAdvice([resjson.length,...resjson])
         setFilteredAdvice([resjson.length,...resjson])
        }
    ).catch(
        error=>{console.log(error)}
    )
  }

  const filterUserAdvicePrice=()=>{
    fetch(`/api/user/advice?page=${clickedPageNumber?clickedPageNumber:1}&min=${minPrice}&max=${maxPrice}`).then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          throw new Error("something's wrong...");
        }
    }).then(
        (resjson)=>{
         setAdvice(resjson)
         setFilteredAdvice(resjson)
        }
    ).catch(
        error=>{console.log(error)}
    )
  }

  return (
    <>
    <Modal open={open} setOpen={setOpen} error={error} component={"Advice"} message={message}/>
    <div class="flex flex-col p-4">
      <section class="flex align-center items-center">
      <div className="flex flex-col">
      <button onClick={showSortOptions} class="bg-transparent border-blue-500 hover:bg-gray-100 text-gray-800 font-semibold px-1 my-1 border border-gray-400 rounded shadow">
        Price
      </button>
      { allPrices && visible && 
        <>
        <Slider
          min={Math.min(...allPrices.slice(1,allPrices.length+1).map(i=>i.advice_price))}
          max={Math.max(...allPrices.slice(1,allPrices.length+1).map(i=>i.advice_price))}
          onChange={({ min, max }) => {
            // /api/advice?min={min}&max={max}
            setMinPrice(min)
            setMaxPrice(max)
            // console.log(`min = ${min}, max = ${max}`)
            }
          }
          visible
        />
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white mt-10 border border-blue-700 rounded"
          onClick={window.location.hash==='#advice'?filterUserAdvicePrice:filterAdvicePrice}
        >View Results</button>
        </>
      }
      </div>
      {/** 
       @todo
       *Add sort on category and budget percentage 
        
       */}
      {/* <button onClick={showSortOptions} class="bg-transparent border-blue-500 hover:bg-gray-100 text-gray-800 font-semibold px-1 border border-gray-400 rounded shadow">
        Category
      </button>
      <button onClick={showSortOptions} class="bg-transparent border-blue-500 hover:bg-gray-100 text-gray-800 font-semibold px-1 border border-gray-400 rounded shadow">
        Percent of budget
      </button> */}

      <div class="flex">
        <div class="">
          <div class="input-group relative flex flex-wrap items-stretch w-full">
            <input onChange={e => setSearchVal(e.target.value)} type="search" class="form-control relative flex-auto min-w-0 block w-full px-3 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none" placeholder="Search" aria-label="Search" aria-describedby="button-addon2"/>
            {/* <button class="btn inline-block px-6 bg-blue-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700  focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out flex items-center" type="button" id="button-addon2">
              <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="search" class="w-4" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                <path fill="currentColor" d="M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z"></path>
              </svg>
            </button> */}
          </div>
        </div>
      </div>
      </section>
     
        {/* Sort Search Section */}
        {/* Advice Card */}
        { advice &&  filteredAdvice && filteredAdvice.length>0 ?  
        <div class="my-1 px-10 w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 p-50 gap-5">
          {filteredAdvice.slice(1,filteredAdvice.length).map(product=> {
          return(
          <article class="flex flex-col overflow-hidden rounded-lg shadow-lg">
            <button
              class="no-underline text-grey-darker hover:text-red-dark self-end p-4"
              href="#"
              onClick={()=>{
                user? saveAdvice(product.advice_id):
                setOpen(true)
              }}
            >
              <span class="dropdown" id="menu-button" aria-expanded="true" aria-haspopup="true">Add</span>

              <i class="fa fa-heart text-red-400 hover:text-red-500"></i>
              <ul class={`dropdown-menu absolute hidden text-gray-700 pt-1`}>
                <li class=""><a class="rounded-t bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap" href="#">One</a></li>
                <li class=""><a class="bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap" href="#">Two</a></li>
                <li class=""><a class="rounded-b bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap" href="#">Three is the magic number</a></li>
              </ul>
              {/* <!-- TODO
                  Add tooltip: https://tailwind-elements.com/docs/standard/components/tooltip/
                --> */}
            </button>
            <a
              target="_blank"
              href={`https://www.walmart.com/search?q=${product?.advice_info_id}`}
            >
              <img
                alt="Placeholder"
                class="block h-auto w-full"
                src={product.advice_img}
              />
            </a>

            <header class="flex direct flex-col justify-between leading-tight p-1">
              <h3 id="price" class="text-grey-darker text-md font-black p-2">
                ${product.advice_price}
              </h3>
              <h2 class="text-md p-2">
                <a
                  class="no-underline hover:underline text-black font-medium"
                  target="_blank"
                  href={`https://www.walmart.com/search?q=${product.advice_info_id}`}
                >
                  {product.advice_name}
                </a>
              </h2>
            </header>

            <footer class="flex flex-col items-center justify-between leading-none p-1">
              <ReadMore>
                {product.advice_description}
              </ReadMore>
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
          </article>
         )}) }</div>: 
          <div class="container mx-auto px-4 flex flex-col lg:flex-row">
            <div class="juice relative w-full rounded-xl bg-secondary-lite bg-cover bg-gradient-to-r from-cyan-500 to-blue-500" style={{backgroundImage:"url(./static/img/conifer-payment-processed-1.png)", height:"100vh"}}>
              <p class="max-w-sm text-secondary text-3xl md:text-4xl font-semibold" style={{background:"#f5eaf9"}}>You have no transactions, so no advice to show!</p>
              <a href="/dashboard#transactions"><button class="mt-20 bg-white font-semibold px-8 py-2 rounded">Start by creating transactions now</button></a>
            </div>
          </div>}
      
      {advice && filteredAdvice &&
      <Pagination
        advice={filteredAdvice}
        paginate={paginate}
        postsPerPage={advice[0]}
        totalPosts={advice[0]}
        paginateBack={paginateBack}
        paginateFront={paginateFront}
        clickedPageNumber={clickedPageNumber}
      />}

      {/* <nav aria-label="Page navigation">
        <ul class="inline-flex space-x-2">
        <li><button class="flex items-center justify-center w-10 h-10 text-indigo-600 transition-colors duration-150 rounded-full focus:shadow-outline hover:bg-indigo-100">
        <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20"><path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" fill-rule="evenodd"></path></svg></button>
        </li>
        {advice &&
          loopList.map(i=>i)
        } */}
        {/* 
        <li><button class="w-10 h-10 text-indigo-600 transition-colors duration-150 rounded-full focus:shadow-outline hover:bg-indigo-100">2</button></li>
        <li><button class="w-10 h-10 text-white transition-colors duration-150 bg-indigo-600 border border-r-0 border-indigo-600 rounded-full focus:shadow-outline">3</button></li>
       */}
        {/* <li><button class="flex items-center justify-center w-10 h-10 text-indigo-600 transition-colors duration-150 bg-white rounded-full focus:shadow-outline hover:bg-indigo-100">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20"><path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" fill-rule="evenodd"></path></svg></button>
        </li> 
      </ul>
    </nav> */}
    </div>
    </>
  )
}
