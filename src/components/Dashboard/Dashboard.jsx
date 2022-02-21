import React from 'react'; 
import BarChart from './BarChart';

export default function Dashboard(props){
    const [reports, setReports] = React.useState(null)
    const [data, setData] = React.useState(null)
    React.useEffect(()=>{
      const reportsFetch = async()=>{
        try{
          const url= "/api/reports"
          const res = await fetch(url)
          if(!res.ok){
            console.log(res.status)
          } else{
            return await res.json()
          }
        } catch(e){
          throw new Error(`${e}`)
        }
      }
      reportsFetch().then(
        (data)=> {
          setReports(data)}
      )
    },[])
    
    React.useEffect(()=>{
      if(reports){
      let bardata = {
        labels: ['Budget Amount', 'Total Spend'],
        datasets: [{
          label: ['Budget Amount', 'Spending'],
          data: [`${reports.total_budget_amount}`,`${reports.transactions_sum}`],
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
      }
      setData(bardata)

    }

    },[reports])

    return(
      <div class="flex flex-col p-4">
      { reports ? 
      <div class="p-10 ">
        <div class=" w-full lg:max-w-full lg:flex">
          <div class="h-48 lg:h-auto w-1/3 flex-none bg-cover rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden" title="Money">
          {data && 
          <BarChart
            data={data}
          />}
          </div>
          <div class="border-r border-b border-l border-gray-400 lg:border-l-0 lg:border-t lg:border-gray-400 bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal">
            <div class="mb-8">
              <div class="text-gray-900 font-bold text-xl mb-2">Your budgets and transactions breakdown</div>
              <div className="border-t border-gray-200">
        <dl>
          <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500"> Number of budgets</dt>
            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{reports.budget_count}</dd>
          </div>
          <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500"> Total budget amount</dt>
            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">${reports?.total_budget_amount?.toLocaleString()}</dd>
          </div>
          <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">Total number of transactions</dt>
            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{reports?.transactions_count?.toLocaleString()}</dd>
          </div>
          <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">Total Spend</dt>
            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">${reports?.transactions_sum?.toLocaleString()}</dd>
          </div>
          <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">Budget - Transaction Breakdown</dt>
            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
            <ul role="list" className="border border-gray-200 rounded-md divide-y divide-gray-200">
                
              {reports.budget_differences && reports.budget_differences.length>0 && reports.budget_differences.map(
                r=>
                <>
                <li className="pl-3 pr-4 py-3 flex items-center justify-between text-sm grid grid-cols-4">
                  <div className="w-0 flex-1 flex items-center">
                    {/* <PaperClipIcon className="flex-shrink-0 h-5 w-5 text-gray-400" aria-hidden="true" /> */}
                    <a href="/budgets" className="font-medium text-indigo-600 hover:text-indigo-500 flex flex-col">
                    <span className="ml-2 flex-1 w-0 "><b>Budget</b>: {r.budget}</span>
                    </a>
                  </div>
                  <div className="ml-4 flex flex-col flex-shrink-0">
                    <b>Budget Remaining</b>:${r.diff.toLocaleString()}
                  </div>
                  <div className="ml-4 flex flex-col flex-shrink-0">
                    <b>Spend Count</b>: {r.total_transactions.toLocaleString()}
                  </div>
                  <div className="ml-4 flex-shrink-0">
                    <b>Spend Total</b>: ${r.total_transactions_amount.toLocaleString()}
                  </div>
                </li>
                </>

                )}
           
                </ul>
                    </dd>
          </div>
          {/* <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">Attachments</dt>
            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <ul role="list" className="border border-gray-200 rounded-md divide-y divide-gray-200">
                <li className="pl-3 pr-4 py-3 flex items-center justify-between text-sm">
                  <div className="w-0 flex-1 flex items-center"> */}
                    {/* <PaperClipIcon className="flex-shrink-0 h-5 w-5 text-gray-400" aria-hidden="true" /> */}
                    {/* <span className="ml-2 flex-1 w-0 truncate">resume_back_end_developer.pdf</span>
                  </div>
                  <div className="ml-4 flex-shrink-0">
                    <a href="#" className="font-medium text-indigo-600 hover:text-indigo-500">
                      Download
                    </a>
                  </div>
                </li>
                <li className="pl-3 pr-4 py-3 flex items-center justify-between text-sm">
                  <div className="w-0 flex-1 flex items-center"> */}
                    {/* <PaperClipIcon className="flex-shrink-0 h-5 w-5 text-gray-400" aria-hidden="true" /> */}
                    {/* <span className="ml-2 flex-1 w-0 truncate">coverletter_back_end_developer.pdf</span>
                  </div>
                  <div className="ml-4 flex-shrink-0">
                    <a href="#" className="font-medium text-indigo-600 hover:text-indigo-500">
                      Download
                    </a> */}
                  {/* </div>
                </li>
              </ul>
            </dd> */}
          {/* </div> */}
        </dl>
      </div>
              {/* <p class="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, Nonea! Maiores et perferendis eaque, exercitationem praesentium nihil.</p> */}
            </div>
            {/* <div class="flex items-center">
              <img class="w-10 h-10 rounded-full mr-4" src='https://images.unsplash.com/photo-1592495989226-03f88104f8cc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NjB8fG1vbmV5fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60' alt="Avatar of Writer"/>
              <div class="text-sm">
                <p class="text-gray-900 leading-none">John Smith</p>
                <p class="text-gray-600">Aug 18</p>
              </div>
            </div> */}
          </div>
        </div>
      </div>: 
      <div class="container mx-auto w-full flex flex-col lg:flex-row">
        <div class="juice relative w-full rounded-xl bg-secondary-lite bg-cover bg-gradient-to-r from-cyan-500 to-blue-500" style={{backgroundImage:"url(./static/img/conifer-mining.png)", height: "100vh", width: "40vw"}}>
          <p class="max-w-sm text-secondary text-3xl md:text-4xl font-semibold" style={{background:"#f5eaf9"}}>You have no budget transactions to show</p>
          <a href="/budgets"><button class="mt-20 bg-white font-semibold px-8 py-2 rounded hover:bg-slate text-teal font-semibold hover:text-slate border border-slate">Start by creating budgets now</button></a>
        </div>
        {/* <div class="juice2 mt-6 lg:mt-0 lg:ml-6 lg:w-1/3 rounded-xl bg-primary-lite bg-cover p-8 md:p-16">
          <div class="max-w-sm">
            <p class="text-3xl md:text-4xl font-semibold uppercase">20% sale off</p>
            <p class="mt-8 font-semibold">Syncthetic seeds<br />2.0 OZ</p>
          </div>
        </div> */}
      </div>}
      </div>
    )
}
