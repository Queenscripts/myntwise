import React from "react";

function BudgetForm(props) {
  const [state, setState] = React.useState({
    budget_name: null, 
    budget_amount: null, 
    budget_description: null, 
    budget_frequency: null, 
    category: null
  })
  const [categories, setCategories] = React.useState(null);
  const categoryFetch = async () => {
    const url = "/api/categories";
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`${res.status} ${res.statusText}`);
    } else {
      return await res.json();
    }
  };

  React.useEffect(() => {  
    categoryFetch().then((categories) => {
      setCategories(categories);
    });
  }, []);

  

  const postBudget = async (e) => {
    e.preventDefault()
    let {
      budget_name, 
      budget_amount, 
      budget_description, 
      budget_frequency, 
      category
    } = state;

    if(budget_frequency ==null)budget_frequency = "Monthly"
    if(category ==null)category = categories[0].name
    try {
        const url = "/api/budgets";
        const res = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            budget_name, 
            budget_amount, 
            budget_description, 
            budget_frequency, 
            category
          }),
        });
        if (!res.ok) {
          setOpen(true);
          setError(res.statusText);
          throw new Error(`${res.status}, ${res.statusText}`);
        } else {
          const budget = await res.json();
          console.log(budget)
          props.setBudgets([...props.budgets,budget])
          setState({
            budget_name:"", 
            budget_amount:"", 
            budget_description:"", 
            budget_frequency:"", 
            category:"",
          });
        }
    } catch (e) {
      throw new Error(`${e}`);
    }
  };

 

  return (
    <>
      <h2 class="text-2xl font-medium leading-tight mt-0 mb-2 text-teal-500">
        {" "}
        Create a new budget
      </h2>
      <form onSubmit={postBudget}>
        <div class="shadow overflow-hidden sm:rounded-md">
          <div class="px-4 py-5 bg-white sm:p-6">
            <div class="grid grid-cols-6 gap-6">
              <div class="col-span-6 sm:col-span-3">
                <label
                  for="budget_name"
                  class="block text-sm font-medium text-gray-700"
                >
                  Budget Name
                </label>
                <input
                  onChange={
                    (e)=>
                    setState({
                      ...state, 
                      budget_name: e.target.value
                    })
                  }
                  type="text"
                  name="budget_name"
                  id="budget_name"
                  autocomplete="given-name"
                  class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-lg sm:text-sm border-gray-300 rounded-md"
                />
              </div>

              <div class="col-span-6 sm:col-span-3">
                <label
                  for="budget_amount"
                  class="block text-sm font-medium text-gray-700"
                >
                  Budget Amount
                </label>
                <input
                  onChange={
                    (e)=>
                    setState({
                      ...state, 
                      budget_amount: e.target.value
                    })
                  }
                  type="number"
                  name="budget_amount"
                  id="budget_amount"
                  autocomplete="family-name"
                  class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-lg sm:text-sm border-gray-300 rounded-md"
                />
              </div>

              <div class="col-span-8">
                <label
                  for="budget_description"
                  class="block text-sm font-medium text-gray-700"
                >
                  Budget Description
                </label>
                <textarea
                  onChange={
                    (e)=>
                    setState({
                      ...state, 
                      budget_description: e.target.value
                    })
                  }
                  type="text"
                  name="budget_description"
                  id="budget_description"
                  autocomplete="email"
                  class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-lg sm:text-sm border-gray-300 rounded-md"
                >
                  {" "}
                </textarea>
              </div>

              <div class="col-span-6 sm:col-span-3">
                <label
                  for="budget_frequency"
                  class="block text-sm font-medium text-gray-700"
                >
                  Frequency
                </label>
                <select
                  onChange={
                    (e)=>
                    setState({
                      ...state, 
                      budget_frequency: e.target.value
                    })
                  }
                  id="budget_frequency"
                  name="budget_frequency"
                  autocomplete="budget_frequency-name"
                  class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-lg focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                >
                  <option>Monthly</option>
                  <option>Weekly</option>
                  <option>Annually</option>
                </select>
              </div>

              <div class="col-span-6 sm:col-span-3">
                <label
                  for="category"
                  class="block text-sm font-medium text-gray-700"
                >
                  Category
                </label>
                <select
                  onChange={
                    (e)=>
                    setState({
                      ...state, 
                      category: e.target.value
                    })
                  }
                  id="category"
                  name="category"
                  autocomplete="budget_category-name"
                  class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-lg focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                >
                  {categories && categories.map(
                    category=>
                    <option>{category.name}</option>
                  )}
                </select>
              </div>
            </div>
          </div>
          <div class="px-4 py-3 bg-gray-50 text-right sm:px-6">
            <button
              
              type="submit"
              class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Save
            </button>
          </div>
        </div>
      </form>
    </>
  );
}

function Budget(props) {
  const [categories, setCategories] = React.useState(null);
  const [budgets, setBudgets] = React.useState(null);
  const [budgetState, setBudgetState] = React.useState(null)

  let sorted = budgets?.reduce((hash, obj)=>{
    if(obj["category"]===undefined) return hash
    return Object.assign(hash, {[obj["category"]]:(hash[obj["category"]] || []).concat(obj)})
  },{})
  React.useEffect(()=>{
    sorted = budgets?.reduce((hash, obj)=>{
      if(obj["category"]===undefined) return hash
      return Object.assign(hash, {[obj["category"]]:(hash[obj["category"]] || []).concat(obj)})
    },{})
  },[budgets])

  React.useEffect(()=>{
    const statFetch = async()=>{
      const res = await fetch('/api/reports')
      if(!res.ok){
        throw new Error(`${res.status, res.statusText}`)
      }else{
        return await res.json()
      }
    }

    statFetch().then((data)=>{
      setBudgetState(data)
    })
  },[])

  React.useEffect(() => {
    const categoryFetch = async () => {
      const url = "/api/categories";
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`${res.status} ${res.statusText}`);
      } else {
        return await res.json();
      }
    };
    categoryFetch().then((categories) => {
      setCategories(categories);
    });
  }, []);

   React.useEffect(() => {
    const budgetFetch = async () => {
      const url = "/api/budgets";
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`${res.status}, ${res.statusText}`);
      } else {
        return await res.json();
      }
    };
    budgetFetch().then((budgets) => {
      setBudgets(budgets);
    });
  }, []);
  

  return (
    <div class="flex flex-col p-4">
      <h1 class="text-4xl font-medium leading-tight mt-0 mb-2 text-teal-500">
        Your Budgets
      </h1>

      <div
        class="hidden fixed z-10 inset-0 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
      >
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      
          <span
            class="hidden sm:inline-block sm:align-middle sm:h-screen"
            aria-hidden="true"
          >
            &#8203;
          </span>

          <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div class="sm:flex sm:items-start">
                <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                  <svg
                    class="h-6 w-6 text-red-600"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                    />
                  </svg>
                </div>
                <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                  <h3
                    class="text-lg leading-6 font-medium text-gray-900"
                    id="modal-title"
                  >
                    Deactivate account
                  </h3>
                  <div class="mt-2">
                    <p class="text-sm text-gray-500">
                      Are you sure you want to deactivate your account? All of
                      your data will be permanently removed. This action cannot
                      be undone.
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button
                type="button"
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm"
              >
                Deactivate
              </button>
              <button
                type="button"
                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
      {
        budgets && Object.keys(sorted).map(
          b=>
            <div className="accordion-item bg-white border border-gray-200">
              <h2 className="accordion-header mb-0" id="heading">
                <button
                  class="
                  accordion-button
                  relative
                  flex
                  items-center
                  w-full
                  py-4
                  px-5
                  text-base text-gray-800 text-left
                  bg-white
                  border-0
                  rounded-none
                  transition
                  focus:outline-none
                "
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#body"
                  aria-expanded="true"
                  aria-controls="body"
                >
                  Category: {b}
                </button>
              </h2>
              <div className="grid grid-cols-2">
              {sorted[b].map(
                sortedBudget=>
              <div
                id={`${sortedBudget.budget_id}`}
                class="accordion-collapse collapse show"
                aria-labelledby={`${sortedBudget}`}
                data-bs-parent="#accordionExample"
              >
                <div class="accordion-body">
                  
                
                  <div
                    tabindex="0"
                    aria-label="card 1"
                    class="focus:outline-none w-full mb-7 bg-white p-6 shadow rounded"
                  >
                    <div class="flex items-center border-b border-gray-200 pb-6">
                      <div class="flex items-start justify-between w-full">
                        <div class="pl-3 w-full">
                          <p tabindex="0" class="focus:outline-none text-xl font-medium leading-5 text-gray-800 w-1/2">{sortedBudget.budget_name}</p>
                          <p tabindex="0" class="focus:outline-none text-sm leading-normal pt-2 text-gray-500">{sortedBudget.budget_description}</p> 
                          {/* <!-- @TODO ADD # OF TRANSACTIONS -->
                              <!-- <p tabindex="0" class="focus:outline-none text-sm leading-normal pt-2 text-gray-500">36 members</p> --> */}
                        </div>
                        <a href={`/budget/${sortedBudget.budget_id}`}>
                          <div role="img" aria-label="trash">
                            <img
                              style={{margin: "-10px 60%"}}
                              onmouseover="if(this.style.opacity == 1){this.style.opacity=.5}else{this.style.opacity=1}"
                              onmouseout="if(this.style.opacity == .5){this.style.opacity=1}else{this.style.opacity=1}"
                              width="30%"
                              src="https://img.icons8.com/external-icongeek26-outline-colour-icongeek26/2x/external-trash-user-interface-icongeek26-outline-colour-icongeek26.png"
                              alt="trash"
                            />
                          </div>
                        </a>
                      </div>
                    </div>
                    <div class="px-2">
                      <div tabindex="0" class="focus:outline-none flex">
                        <div class="py-2 px-4 text-xs leading-3 text-indigo-700 rounded-full bg-indigo-100">${sortedBudget.budget_amount} {sortedBudget.budget_frequency}</div>
                        
                          
                         {
                          budgetState && budgetState?.budget_differences.filter(b=>b.budget===sortedBudget.budget_name)[0]?.diff == 0? <div class="py-2 px-4 ml-3 text-xs leading-3 text-red-700 rounded-full bg-stone-100">Remaining: $0 </div>: budgetState?.budget_differences.filter(b=>b.budget===sortedBudget.budget_name)[0]?.diff == undefined ? "": <div class="py-2 px-4 ml-3 text-xs leading-3 text-red-700 rounded-full bg-stone-100">Remaining: ${budgetState?.budget_differences.filter(b=>b.budget===sortedBudget.budget_name)[0]?.diff}</div>
                          }
                       
                      </div>
                    </div>
                  </div>
                </div>
              </div>)}
              </div>
            </div>)
      }
      <BudgetForm
        setBudgets={setBudgets}
        budgets={budgets}
      />
    </div>
  );
}

export default Budget;
