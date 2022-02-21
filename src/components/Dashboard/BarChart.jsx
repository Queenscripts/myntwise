import React from 'react';

const  BarChart = React.forwardRef((props)=>{
    /**
     * @todo
     * Deep dive on useRef
     * https://reactjs.org/docs/hooks-reference.html
     *  */  
   
    const [chart, setChart] = React.useState(null)
    let chartRef = React.useRef(null)
    // 
    let data = props.data? props.data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    }
    React.useEffect(()=>{
        
        let ctx = chartRef.current.getContext('2d')
        const myChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            title: {
              display: false,
              fontStyle: 'bold',
              text: "SPENDING"
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
                  // beginAtZero: true,
                  // stepSize: 100,
                     // Return an empty string to draw the tick line but hide the tick label
                     // Return `null` or `undefined` to hide the tick line entirely
                     userCallback: function(value, index, values) {
                      // Convert the number to a string and splite the string every 3 charaters from the end
                      value = value.toString();
                      value = value.split(/(?=(?:...)*$)/);
                      
                      // Convert the array to a string and format the output
                      value = value.join(',');
                      return '$' + value;
                      }
                }
              }]
            },
            responsive: true,
          }
        }); 

        setChart(myChart)
    },[chartRef])

  
    return(
        <canvas ref={chartRef} width="400" height="600">
        </canvas>
    )
})

export default BarChart; 
