import React from 'react';

const LineChart = React.forwardRef((props) => {
    // @TODO Learn more on how useref works
    // https://reactjs.org/docs/hooks-reference.html
    const [chart, setChart] = React.useState(null);
    let chartRef = React.useRef(null);
    
    const labels = ["jan", "feb", "mar"];
    const data = props.data? props.data: {
      labels: labels,
      datasets: [{
        label: 'My First Dataset',
        data: [65, 59, 80, 81, 56, 55, 40],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }]
    };

    
   
      React.useEffect(() => {
      let ctx = chartRef.current.getContext("2d");
      const myChart = new Chart(ctx, {
        type: "line",
        data: data,
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Chart.js Pie Chart",
            },
          },
        },
      });
  
      setChart(myChart);
    }, [chartRef]);
  
    React.useEffect(() => {
      console.log("CHART", chartRef.current);
    }, [chart]);
    return <canvas ref={chartRef} width="400" height="400"></canvas>;
  });
export default LineChart;
  // const domContainer = document.querySelector("#bar-chart");
  // ReactDOM.render(React.createElement(LineChart), domContainer);
  