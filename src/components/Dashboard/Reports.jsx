import React from 'react'; 
import BarChart from './BarChart'
import LineChart from './LineChart'
import PieChart from './PieChart'
import { CSVLink } from "react-csv";

function ReportForm() {
  
  const [state, setState] = React.useState({
    minPrice: "",
    maxPrice: "",
    startDate: "",
    endDate: ""
  })
  const [csvData, setCSVData] = React.useState([])
  const [pieData, setPieData] = React.useState(null)
  const [barData, setBarData] = React.useState(null)
  const [lineData, setLineData] = React.useState(null)
  const [reports, setReports] = React.useState(null)
  const [monthSpend, setMonthDateSpend] = React.useState(null)
  const [priceSpend, setPriceSpend] = React.useState(null)
  const [averageSpend, setAverageSpend] = React.useState(null)
  const [averageCategory, setAverageCategory] = React.useState(null)
  const newReport = ()=>{
    fetch(`/api/reports?min_price=${state.minPrice}&max_price=${state.maxPrice}&start_date=${state.startDate}&end_date=${state.endDate}`).then((res) => {
    if (res.ok) {
      return res.json();
    } else {
      throw new Error("something's wrong...");
    }
    }).then(
    (resjson)=>{
      let sum = 0
      let priceSum = 0
      let totalSpendNum = resjson.dated_transactions.length
      resjson.dated_transactions.map(i=>sum += parseInt(i.transaction_amount))
      resjson.price_ranged_transactions.map(p=>priceSum+=parseInt(p.transaction_amount))
      let categories = [...resjson.dated_transactions].map(c=>c.transaction_category)
      let average = Math.round(sum/totalSpendNum)
      function maxFreq(arr, n) {
        //using moore's voting algorithm
        var res = 0;
        var count = 1;
        for (var i = 1; i < n; i++) {
          if (arr[i] === arr[res]) {
            count++;
          } else {
            count--;
          }
 
          if (count === 0) {
            res = i;
            count = 1;
          }
        }
 
        return arr[res];
      }
      setPriceSpend(priceSum)
      setMonthDateSpend(sum)
      setAverageCategory(maxFreq(categories, categories.length))
      setAverageSpend(average)
      setReports(resjson)
      
    }
).catch(
    error=>{console.log(error)}
)}
  React.useEffect(() => {
    
    // Extract separate fetch call in new API request file
    const {startDate, endDate} = state
    setPieData({
      labels: reports?.budget_differences.map(b=>b.budget),
      datasets: [{
        label: 'Budget Spending',
        data: reports?.budget_differences.map(b=>b.total_transactions_amount),
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          
        ],
        hoverOffset: 4
      }]
    })
    if(reports && reports.budget_differences){
      let differences = reports.budget_differences.map(
        b=>{return([{"Budget":b.budget}, {"Remaining":b.diff}, {"Total Transactions":b.total_transactions}, {"Total Budget Spend": b.total_transactions_amount }])}
      )
      setCSVData([].concat.apply([], differences))
      // const uniqueBudgets = [...new Map(reports.budget_info.map(v => [v.name, v])).values()]
      // let budgetSum = 0
      // uniqueBudgets.map(b=> budgetSum+=b.amount)
      let transactionSum = 0
      reports?.dated_transactions.map(sum=>transactionSum+=sum.transaction_amount)
      reports?.price_ranged_transactions.map(sum=>transactionSum+=sum.transaction_amount)

    setBarData({
        labels: ['Budget Amount', 'Total Spend'],
        datasets: [{
          label: ['Budget Amount', 'Spending'],
          data: [`${reports.total_budget_amount}`,`${transactionSum}`],
          backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
          ],
          borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
          ],
          
        }],
          borderWidth: 1,
          options: {
            title: {
              display: true,
              fontStyle: 'bold',
              text: "Figure"
            },
            legend: {
              position: "bottom",
              labels: {}
            },
            tooltips: {
              mode: 'label',
              bodySpacing: 10,
              cornerRadius: 0,
              titleMarginBottom: 15,
            },
            scales: {
              xAxes: [{
                ticks: {}
              }],
              yAxes: [{
                ticks: {
                  beginAtZero: true,
                  stepSize: 500000,
                    // Return an empty string to draw the tick line but hide the tick label
                    // Return `null` or `undefined` to hide the tick line entirely
                    userCallback: function(value, index, values) {
                      // Convert the number to a string and split the string every 3 charaters from the end
                      value = value.toString();
                      value = value.split(/(?=(?:...)*$)/);
                      // Convert the array to a string and format the output
                      value = value.join('.');
                      return '?' + value;
                     }
                }
              }]
            },
            responsive: true,
          }
    })}
    if(startDate && endDate && reports){
    const getDays = function(s,e) {for(var a=[],d=new Date(s);d<=e;d.setDate(d.getDate()+1)){ a.push(new Date(d));}return a;};
    const daysArr = getDays(new Date(startDate), new Date(endDate));
    let dates = daysArr.map((v)=>v.toLocaleDateString())
    let lineDataset =reports?.price_ranged_transactions.map(t=>({x : new Date(t.transaction_date).toLocaleDateString(), y : t.transaction_amount})).concat(reports?.dated_transactions.map(t=>({x : new Date(t.transaction_date).toLocaleDateString(), y : t.transaction_amount})))
    setLineData({
      labels: dates,
      datasets: [{
        label: 'Spending Overtime',
        data: lineDataset,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }]
    })}
  }, [state, reports]);

  return (
    <div className="w-full">
      <div>
        <div className="md:grid md:grid-cols-2 md:gap-6">
          
          <div className="p-2 col-span-2">
            <h2 className="font-semibold text-gray-700 p-2"> View more reports by date or price range</h2>
            
              <div className="shadow sm:rounded-md sm:overflow-hidden">
                <div className="p-2 bg-white">
                  <div className="grid grid-cols-4 gap-6">
                    <div className="col-span-2">
                      <label htmlFor="start_date" className="block text-sm font-medium text-gray-700">
                        Start Date
                      </label>
                      <div className="mt-1 flex rounded-md shadow-sm">
                        <input
                          onChange={
                            (e)=>
                            setState({
                              ...state, 
                              startDate: e.target.value
                            })
                          }
                          type="date"
                          name="start_date"
                          id="start_date"
                          className="focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-gray-300"
                        />
                      </div>
                    </div>
                    <div className="col-span-2">
                      <label htmlFor="end_date" className="block text-sm font-medium text-gray-700">
                        End Date
                      </label>
                      <div className="mt-1 flex rounded-md shadow-sm">
                        <input
                          onChange={
                            (e)=>
                            setState({
                              ...state, 
                              endDate: e.target.value
                            })
                          }
                          type="date"
                          name="end_date"
                          id="end_date"
                          className="focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-gray-300"
                        />
                      </div>
                    </div>
                  </div>
                  <div className="grid grid-cols-4 gap-6">
                    <div className="col-span-2">
                      <label htmlFor="min_price" className="block text-sm font-medium text-gray-700">
                        Minimum Price
                      </label>
                      <div className="mt-1 flex rounded-md shadow-sm">
                        <input
                          onChange={
                            (e)=>
                            setState({
                              ...state, 
                              minPrice: e.target.value
                            })
                          }
                          type="number"
                          name="min_price"
                          id="min_price"
                          className="focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-gray-300"
                        />
                      </div>
                    </div>
                    <div className="col-span-2">
                      <label htmlFor="max_price" className="block text-sm font-medium text-gray-700">
                        Maximum Price
                      </label>
                      <div className="mt-1 flex rounded-md shadow-sm">
                        <input
                          onChange={
                            (e)=>
                            setState({
                              ...state, 
                              maxPrice: e.target.value
                            })
                          }
                          type="number"
                          name="max_price"
                          id="max_price"
                          className="focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-gray-300"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
                  <button
                    onClick={
                      newReport
                    }
                    className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    See report
                  </button>
                </div>
              </div>
           
          </div>
        </div>
      </div>
      { reports &&
      <div class="w-full rounded overflow-hidden shadow-lg">
      <div class="w-full">
      <div class="flex flex-row rounded-lg bg-white shadow-lg">
      <div id="carouselExampleCaptions" class="w-full h-auto object-cover carousel slide relative" data-bs-ride="carousel">
  <div class="carousel-indicators absolute right-0 bottom-0 left-0 flex justify-center p-0 mb-4">
    <button
      type="button"
      data-bs-target="#carouselExampleCaptions"
      data-bs-slide-to="0"
      class="active"
      aria-current="true"
      aria-label="Slide 1"
    ></button>
    <button
      type="button"
      data-bs-target="#carouselExampleCaptions"
      data-bs-slide-to="1"
      aria-label="Slide 2"
    ></button>
    <button
      type="button"
      data-bs-target="#carouselExampleCaptions"
      data-bs-slide-to="2"
      aria-label="Slide 3"
    ></button>
  </div>
  <div class="carousel-inner relative w-full overflow-hidden">
    <div class="carousel-item active relative float-left w-full">
      <div class="block w-full">
        <PieChart
          data={
            pieData
          }

        />
      </div>
      <div class="carousel-caption hidden md:block absolute text-center">
        <h5 class="text-xl">Spending by budget</h5>
        {/* <p>Some representative placeholder content for the first slide.</p> */}
      </div>
    </div>
    <div class="carousel-item relative float-left w-full">
    <div class="block w-full">
        {barData?
        <BarChart
          data={barData}
        />:<></>}
      </div>
      <div class="carousel-caption hidden md:block absolute text-center">
        <h5 class="text-xl">Total Spending</h5>
        {/* <p>Some representative placeholder content for the second slide.</p> */}
      </div>
    </div>
    <div class="carousel-item relative float-left w-full">
    <div class="block w-full">
    {lineData?
        <LineChart
        data={lineData}
      />:<></>}
        
      </div>
      <div class="carousel-caption hidden md:block absolute text-center">
        <h5 class="text-xl">Third slide label</h5>
        <p>Some representative placeholder content for the third slide.</p>
      </div>
    </div>
  </div>
  <button
    class="carousel-control-prev absolute top-0 bottom-0 flex items-center justify-center p-0 text-center border-0 hover:outline-none hover:no-underline focus:outline-none focus:no-underline left-0"
    type="button"
    data-bs-target="#carouselExampleCaptions"
    data-bs-slide="prev"
  >
    <span class="carousel-control-prev-icon inline-block bg-no-repeat" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button
    class="carousel-control-next absolute top-0 bottom-0 flex items-center justify-center p-0 text-center border-0 hover:outline-none hover:no-underline focus:outline-none focus:no-underline right-0"
    type="button"
    data-bs-target="#carouselExampleCaptions"
    data-bs-slide="next"
  >
    <span class="carousel-control-next-icon inline-block bg-no-repeat" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
      </div>
        <div class="p-6 flex flex-col justify-start">
          <h5 class="text-gray-900 text-xl font-medium mb-2"> Report Breakdown</h5>
          {reports &&csvData && csvData !==[] &&
          console.log(csvData, {...csvData}),
          <CSVLink 
            filename={`${user}-spending-report.csv`}
            className="rounded-md text-white p-2 bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" data={[
            {"Number of Budgets":reports.budget_count},
            {"Total Items Purchased": reports.transactions_count},
            {"Total Spend": reports.transactions_sum},
            ...csvData
           
            ]}>
            Download CSV Data
          </CSVLink>}
          <p class="text-gray-700 text-base mb-4">
           
          </p>
          {/* <p class="text-gray-600 text-xs">Last updated 3 mins ago</p> */}
          <div class="px-6 pt-4 pb-2">
              <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">{reports?.price_ranged_transactions.length + reports?.dated_transactions.length} total transactions</span>
              <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">${averageSpend.toLocaleString()} average spend</span>
              <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">${(monthSpend + priceSpend).toLocaleString()} total spend</span>
            </div>
        </div>
      </div>
    </div>             
      </div>
      }
    </div>)}
  

function Reports(){
  const [reports, setReports] = React.useState(null)
  const [monthSpend, setMonthSpend] = React.useState(null)
  const [averageSpend, setAverageSpend] = React.useState(null)
  const [averageCategory, setAverageCategory] = React.useState(null)
  const [priceRange, setPriceRange] = React.useState({
    minPrice: "", 
    maxPrice: "" 
  })
  const [dateRange, setDateRange] = React.useState({
    startDate: "", 
    endDate: "" 
  })
 
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Dec']
  const monthNow = months[new Date().getMonth()]
  const formatMonthNow = new Date().getMonth()+1

  const yearNow = new Date().getFullYear()
  const dayNow = new Date().getDate()
  
  React.useEffect(()=>{
    if(parseInt(formatMonthNow)==2){
      setDateRange({
        startDate:`0${formatMonthNow}-01-${yearNow}`,
        endDate: `0${formatMonthNow}-28-${yearNow}`
      })
    }
   
    else if(parseInt(formatMonthNow)!==2 && parseInt(formatMonthNow)<10){
        setDateRange({
          startDate:`0${formatMonthNow}-01-${yearNow}`,
          endDate: `0${formatMonthNow}-31-${yearNow}`
        })
     
    }else{
      setDateRange({
        startDate:`${formatMonthNow}-01-${yearNow}`,
        endDate: `${formatMonthNow}-30-${yearNow}`
      })
    }
    
  },[])


  React.useEffect(() => {
    // Extract separate fetch call in new API request file

    if(dateRange || priceRange)fetch(`/api/reports?min_price=${priceRange.minPrice}&max_price=${priceRange.maxPrice}&start_date=${dateRange.startDate}&end_date=${dateRange.endDate}`).then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          throw new Error("something's wrong...");
        }
    }).then(
        (resjson)=>{
          let sum = 0
          let totalSpendNum = resjson?.dated_transactions.length + resjson?.price_ranged_transactions.length
          resjson.dated_transactions.map(i=>sum += parseInt(i.transaction_amount))
          setMonthSpend(sum)
          let categories = [...resjson.dated_transactions].map(c=>c.transaction_category)
          let average = Math.round(sum/totalSpendNum)
          
          function maxFreq(arr, n) {
            //using moore's voting algorithm
            var res = 0;
            var count = 1;
            for (var i = 1; i < n; i++) {
              if (arr[i] === arr[res]) {
                count++;
              } else {
                count--;
              }
     
              if (count === 0) {
                res = i;
                count = 1;
              }
            }
     
            return arr[res];
          }

          setAverageCategory(maxFreq(categories, categories.length))
          setAverageSpend(average)
         setReports(resjson)
        }
    ).catch(
        error=>{console.log(error)}
    )
  }, [dateRange,priceRange]);

    return(
        <>
        {reports && averageSpend && dayNow && reports.dated_transactions ?

        <div className="flex flex-col w-full">
          <div class="w-full flex justify-evenly p-2 border-b-2">
          <div class="flex flex-col items-center p-2 ">
            <div class="stat-title">Total Monthly Spend</div> 
            <div class="font-black leading-tight text-4xl mt-0 mb-2 text-slate-600">${monthSpend.toLocaleString()}</div> 
            <div class="stat-desc">Up to {dayNow}.{monthNow}.{yearNow}</div>
          </div> 
          <div class="flex flex-col items-center p-2 border-l-2 border-r-2">
            <div class="stat-title">Average Spend This Month</div> 
            <div class="font-black leading-tight text-4xl mt-0 mb-2 text-blue-600">${averageSpend}</div> 
            <div class="stat-desc text-success">↗︎ Out of {reports.dated_transactions.length} transactions</div>
          </div> 
          <div class="flex flex-col items-center p-2">
            <div class="stat-title">Frequently Purchased Vertical</div> 
            <div class="font-black leading-tight text-4xl mt-0 mb-2 text-orange-500">{averageCategory}</div> 
            {/* <div class="stat-desc text-error">↘︎ 90 (14%)</div> */}
          </div>
          </div>
          <ReportForm/>
          
          

        </div>:
        <div class="flex justify-center items-center w-full">
                    <span class="order-2 text-teal text-4x-l">Please referesh page.</span>

        <div class="spinner-grow inline-block w-8 h-8 bg-current rounded-full opacity-0 text-green-500" role="status">
          <span class="visually-hidden">Referesh page.</span>
        </div>
      </div>
        }
        </>
    )
}

export default Reports