import 'regenerator-runtime/runtime'
import React from "react";
import Modal from "./Modal"

export default function Table(props) {

  const [open, setOpen] = React.useState(false);
  const [error, setError] = React.useState(null);

  const [state, setState] = React.useState({
    user_transactions_name: null,
    user_transactions_amount: null,
    budget: null,
    category: null,
    user_transactions_date: null,
  });

  const [categories, setCategories] = React.useState(null);
  const [budgets, setBudgets] = React.useState(null);
  const [userTransactions, setUserTransactions] = React.useState([]);
  const [sortProp, setSortProp] = React.useState(null)
  const [isEditting, setIsEditting] = React.useState({
                                        editting: false,
                                        key: null,

                                      })
  
  let sortedTransactions = [...userTransactions]

  const useSortableData = (transactions) => {  
    const sortedItems = React.useMemo(
      () => {
      if (sortProp !== null) {
        sortedTransactions.sort((a, b) => {
          if(sortProp.key=="transaction_amount"){
            if (parseInt(a[sortProp.key]) < parseInt(b[sortProp.key])) {
              return sortProp.direction === 'ascending' ? -1 : 1;
            }
            if (parseInt(a[sortProp.key]) > parseInt(b[sortProp.key])) {
              return sortProp.direction === 'ascending' ? 1 : -1;
            }
            return 0;
          }
          if (a[sortProp.key] < b[sortProp.key]) {
            return sortProp.direction === 'ascending' ? -1 : 1;
          }
          if (a[sortProp.key] > b[sortProp.key]) {
            return sortProp.direction === 'ascending' ? 1 : -1;
          }
          return 0;
        });
      }
      return sortedTransactions;
    }, [transactions, setSortProp]);
    
    const requestSort = key => {
      let direction = 'ascending';
      if(sortProp && sortProp.key === key && sortProp.direction === 'ascending') {
        direction = 'descending';
      }
      setSortProp({ key, direction });
    }
  
    return { transactions: sortedItems, requestSort};
  };


  React.useEffect(()=>{
     sortedTransactions = [...userTransactions]
  },[userTransactions, state])

  let {transactions, requestSort} = useSortableData(sortedTransactions)

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

  React.useEffect(() => {
    setState({
      user_transactions_name: "",
      user_transactions_amount: "",
      user_transactions_date: "",
    })
    const transactionsFetch = async () => {
      const url = "/api/transactions";
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`${res.status}, ${res.statusText}`);
      } else {
        const transactions = await res.json();
        return transactions;
      }
    };

    transactionsFetch().then((userTransactions) =>
      setUserTransactions(userTransactions)
    );
  }, []);

  const postTransaction = (e) => {
    let {
      user_transactions_name,
      user_transactions_amount,
      user_transactions_date,
      budget,
      category,
    } = state;

    if(budget ==null)budget = budgets[0].budget_name
    if(category ==null)category = categories[0].name
    const user_transactions_processed = true;
    try {
      e.preventDefault();
      const newTransaction = async () => {
        const url = "/api/transactions";
        const res = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_transactions_name,
            user_transactions_amount,
            user_transactions_date,
            user_transactions_processed,
            budget,
            category,
            img:null
          }),
        });
        // ${'http://localhost:5000'}
        fetch(`/?query=${user_transactions_name}`)
        if (!res.ok) {
          setOpen(true);
          setError(res.statusText);
          throw new Error(`${res.status}, ${res.statusText}`);
        } else {
        return await res.json()
        }
      };
      newTransaction().then(
        async (data) => {
        
        setState({
          categories,
          budgets,
        });
       
        setUserTransactions([...userTransactions,data])
      });
    } catch (e) {
      throw new Error(`${e}`);
    }
  };

  const updateTransaction = (id) => {
    let {
      user_transactions_name,
      user_transactions_amount,
      user_transactions_date,
      budget,
      category,
    } = state;
    if(user_transactions_name == null || user_transactions_name== "") user_transactions_name = id.transaction_name
    if(user_transactions_amount == null || user_transactions_amount== "") user_transactions_amount = id.transaction_amount
    if(user_transactions_date == null || user_transactions_date== "") user_transactions_date = id.transaction_date
    if(budget ==null  || budget== undefined|| !budget)budget = id.budget
    if(category == null || category== undefined|| !category) category = id.category
    const user_transactions_processed = true;
    try {
      const updatedTransaction = async () => {
        const url = "/api/transactions";
        const res = await fetch(url, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            transaction_id:parseInt(id.transaction_id),
            user_transactions_name,
            user_transactions_amount,
            user_transactions_date,
            user_transactions_processed,
            budget,
            category,
          }),
        });
        // fetch(`${'http://localhost:5000'}?query=${user_transactions_name}`)
        if (!res.ok) {
          setOpen(true);
          setError(res.statusText);
          throw new Error(`${res.status}, ${res.statusText}`);
        } else {
          return await res.json();
        }
      };
      updatedTransaction().then((data) => {
        let newArr = [...userTransactions]
        let transactionIndex = newArr.findIndex(item=>item.transaction_id === data.transaction_id)
        newArr.splice(transactionIndex,1,data)
        setUserTransactions(
          newArr
        )
        setState({
          user_transactions_name: null,
          user_transactions_amount: null,
          budget: null,
          category: null,
          user_transactions_date: null,
        })
      });
    } catch (e) {
      throw new Error(`${e}`);
    }
  };

  return (
    <>
      <Modal open={open} setOpen={setOpen} error={error} />

      <div class="table w-full p-2">
        <div
          class="hidden overflow-y-auto overflow-x-hidden fixed right-0 left-0 top-4 z-50 justify-center items-center md:inset-0 h-modal sm:h-full"
          id="popup-modal"
        >
          <div class="relative px-4 w-full max-w-md h-full md:h-auto">
            {/* <!-- Modal content --> */}
            <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
              {/* <!-- Modal header --> */}
              <div class="flex justify-end p-2">
                <button
                  type="button"
                  class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-800 dark:hover:text-white"
                  data-modal-toggle="popup-modal"
                >
                  <svg
                    class="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                </button>
              </div>
              {/* <!-- Modal body --> */}
              <div class="p-6 pt-0 text-center">
                <svg
                  class="mx-auto mb-4 w-14 h-14 text-gray-400 dark:text-gray-200"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  ></path>
                </svg>
                <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
                  Are you sure you want to delete this product?
                </h3>
                <button
                  data-modal-toggle="popup-modal"
                  type="button"
                  class="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center mr-2"
                >
                  Yes, I'm sure
                </button>
                <button
                  data-modal-toggle="popup-modal"
                  type="button"
                  class="text-gray-500 bg-white hover:bg-gray-100 focus:ring-4 focus:ring-gray-300 rounded-lg border border-gray-200 text-sm font-medium px-5 py-2.5 hover:text-gray-900 focus:z-10 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-500 dark:hover:text-white dark:hover:bg-gray-600"
                >
                  No, cancel
                </button>
              </div>
            </div>
          </div>
        </div>
        <table class="border flex flex-row flex-no-wrap sm:bg-white rounded-lg overflow-hidden sm:shadow-lg w-full">
          <thead>
            <tr class="bg-gray-50 border-b flex flex-col flex-no wrap lg:table-col lg:table-row rounded-l-lg sm:rounded-none mb-2 sm:mb-0">
              {/* <th class="border-r p-2">
                <input type="checkbox" />
              </th> */}

              <th onClick={() => requestSort('transaction_name')}  class="p-2 border-r cursor-pointer text-sm font-thin text-gray-500">
                <div  class="flex items-center justify-center">
                  Name
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M8 9l4-4 4 4m0 6l-4 4-4-4"
                    />
                  </svg>
                </div>
              </th>
              <th class="p-2 border-r cursor-pointer text-sm font-thin text-gray-500" onClick={() => requestSort('transaction_amount')}>
                <div class="flex items-center justify-center">
                  Amount
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M8 9l4-4 4 4m0 6l-4 4-4-4"
                    />
                  </svg>
                </div>
              </th>
              <th class="p-2 border-r cursor-pointer text-sm font-thin text-gray-500" onClick={() => requestSort('budget')}>
                <div class="flex items-center justify-center">
                  Budget
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M8 9l4-4 4 4m0 6l-4 4-4-4"
                    />
                  </svg>
                </div>
              </th>
              <th class="p-2 border-r cursor-pointer text-sm font-thin text-gray-500" onClick={() => requestSort('category')}>
                <div class="flex items-center justify-center">
                  Category
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M8 9l4-4 4 4m0 6l-4 4-4-4"
                    />
                  </svg>
                </div>
              </th>
              <th class="p-2 border-r cursor-pointer text-sm font-thin text-gray-500" onClick={() => requestSort('transaction_date')}>
                <div class="flex items-center justify-center">
                  Date
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M8 9l4-4 4 4m0 6l-4 4-4-4"
                    />
                  </svg>
                </div>
              </th>
              <th class="p-10 border-r cursor-pointer text-sm font-thin text-gray-500">
                <div class="flex items-center justify-center">
                  Action
                  {/* <!-- <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l4-4 4 4m0 6l-4 4-4-4" />
                      </svg> --> */}
                </div>
              </th>
            </tr>
          </thead>
          <tbody class="flex-1">
            <tr class="bg-gray-50 text-center flex flex-col flex-no wrap lg:flex-col  lg:table-col lg:table-row rounded-l-lg sm:rounded-none mb-2 sm:mb-0">
              {/* <td class="p-2 border-r"></td> */}
              <td class="p-2 border-r">
                <input
                  onChange={(e) =>
                    setState({
                      ...state,
                      user_transactions_name: e.target.value,
                    })
                  }
                  form="transaction"
                  id="tname"
                  type="text"
                  class="border p-1 w-full"
                  required
                />
              </td>
              <td class="p-2 border-r">
                <input
                  onChange={(e) =>
                    setState({
                      ...state,
                      user_transactions_amount: e.target.value,
                    })
                  }
                  form="transaction"
                  id="tamount"
                  type="number"
                  class="border p-1 w-full"
                />
              </td>
              <td class="p-2 border-r">
                <select
                  onChange={(e) =>
                    setState({
                      ...state,
                      budget: e.target.value,
                    })
                  }
                  id="budget"
                  name="budget"
                  autocomplete="user_transaction_frequency-name"
                  class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                >
                  {budgets &&
                    budgets.length > 0 &&
                    budgets.map((b) => <option>{b.budget_name}</option>)}
                  {/* {% for budget in budgets%}
                        <option>
                            {{budget.budget_name}}
                        </option>
                    {% endfor %} */}
                </select>
              </td>
              <td class="p-2 border-r">
                <select
                  onChange={(e) =>
                    setState({
                      ...state,
                      category: e.target.value,
                    })
                  }
                  id="category"
                  name="category"
                  autocomplete="user_transaction_category-name"
                  className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                >
                  {categories &&
                    categories.length > 0 &&
                    categories.map((c) => <option>{c.name}</option>)}

                </select>
              </td>
              <td class="p-2 border-r">
                <input
                  onChange={(e) =>
                    setState({
                      ...state,
                      user_transactions_date: e.target.value,
                    })
                  }
                  form="transaction"
                  id="tdate"
                  type="date"
                  class="border p-1 w-full"
                  required
                />
              </td>

              <td>
                <button
                  onClick={postTransaction}
                  type="submit"
                  form="transaction"
                  class="bg-blue-500 p-2 text-white hover:shadow-lg text-xs font-thin"
                >
                  Add
                </button>
              </td>
            </tr>
            {transactions &&
              transactions.length > 0 &&
              transactions.map((t) => (
                <tr class="odd:bg-white even:bg-teal-100 bg-gray-100 text-center border-b text-sm text-gray-600 flex flex-col flex-no wrap  lg:table-col lg:flex-col lg:table-row rounded-l-lg sm:rounded-none mb-2 sm:mb-0">
                  {/* <td class="p-2 border-r">
                    <input type="checkbox" />
                  </td> */}
                  { isEditting.editting && isEditting.key == t.transaction_id
                   ? <td class="p-2 border-r">
                   <input
                     onChange={(e) =>
                       setState({
                         ...state,
                         user_transactions_name: e.target.value,
                       })
                     }
                     defaultValue={t.transaction_name}
                     form="transaction"
                     id="tname"
                     type="text"
                     class="border p-1"
                     required
                   />
                 </td> :
                    <td class="p-2 border-r">{t.transaction_name}</td>
                  }
                  { isEditting.editting && isEditting.key == t.transaction_id
                   ? <td class="p-2 border-r">
                   <input
                     onChange={(e) =>
                       setState({
                         ...state,
                         user_transactions_amount: e.target.value,
                       })
                     }
                     defaultValue={t.transaction_amount}
                     form="transaction"
                     id="tamount"
                     type="number"
                     class="border p-1"
                   />
                 </td> :
                   <td class="p-2 border-r">${t.transaction_amount}</td>
                  }
                  
                  { isEditting.editting && isEditting.key == t.transaction_id?
                    <td class="p-2 border-r">
                      <select
                        onChange={(e) =>
                          setState({
                            ...state,
                            budget: e.target.value,
                          })
                        }
                        id="budget"
                        name="budget"
                        autocomplete="user_transaction_frequency-name"
                        class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      >
                        <option>{t.budget}</option>
                        {budgets &&
                          budgets.length > 0 &&
                          budgets.filter(bname=>bname.budget_name!==t.budget).map((b) =>  <option>{b.budget_name}</option>)}
                      </select>
                    </td>:
                    <td class="p-2 border-r">{t.budget}</td>
                  }
            
                  { isEditting.editting && isEditting.key == t.transaction_id?
                    <td class="p-2 border-r">
                    <select
                      onChange={(e) =>
                        setState({
                          ...state,
                          category: e.target.value,
                        })
                      }
                      id="category"
                      name="category"
                      autocomplete="user_transaction_category-name"
                      className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    >
                      {categories &&
                        categories.length > 0 &&
                        categories.map((c) => <option>{c.name}</option>)}
                      {/* {% for category in categories%}
                        <option>{{category.category_name}}</option>
                        {% endfor %} */}
                    </select>
                    </td>: <td class="p-2 border-r">{t.category}</td>}
                    { isEditting.editting && isEditting.key == t.transaction_id?
                  <td class="p-2 border-r">
                    <input
                      onChange={(e) =>
                        setState({
                          ...state,
                          user_transactions_date: e.target.value,
                        })
                      }
                      form="transaction"
                      id="tdate"
                      type="date"
                      class="border p-1"
                      defaultValue={t.transaction_date}
                      required
                    />
                  </td> :
                  <td class="p-2 border-r">{t.transaction_date}</td>}
                  <td>
                    { isEditting.editting && isEditting.key == t.transaction_id?
                      <button
                        class="bg-blue-500 p-2 text-white hover:shadow-lg text-xs font-thin"
                        onClick={()=>{
                          if(t)
                          updateTransaction(t),
                          setIsEditting({editting:false, key:t.transaction_id})
                        }}
                      >
                      Save
                      </button>:
                    <button
                    class="bg-blue-500 p-2 text-white hover:shadow-lg text-xs font-thin"
                    onClick={()=>
                      setIsEditting({editting:true, key:t.transaction_id})
                    }
                  >
                    Edit
                  </button>
                    }
                    <a
                      href={`/api/transaction/${t.transaction_id}`}
                      class="bg-red-500 p-2 text-white hover:shadow-lg text-xs font-thin"
                    >
                      Remove
                    </a>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
