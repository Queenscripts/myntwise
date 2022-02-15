import React from 'react';

const PieChart = React.forwardRef((props) => {
  // @TODO Learn more on how useref works
  // https://reactjs.org/docs/hooks-reference.html
  const [chart, setChart] = React.useState(null);
  let chartRef = React.useRef(null);
  const DATA_COUNT = 5;
  const NUMBER_CFG = { count: DATA_COUNT, min: 0, max: 100 };

 const data = {
    labels: [
      'Red',
      'Blue',
      'Yellow'
    ],
    datasets: [{
      label: 'My First Dataset',
      data: [300, 50, 100],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
  };
  const CHART_COLORS = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
  };

    React.useEffect(() => {
      
    let ctx = chartRef.current.getContext("2d");
    const myChart = new Chart(ctx, {
      type: "pie",
      data: props?.data,
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
  }, [chartRef, props]);

  React.useEffect(() => {
    console.log(props.data)
  }, [props]);
  return <canvas ref={chartRef} width="400" height="400"></canvas>;
});

export default PieChart
// const domContainer = document.querySelector("#bar-chart");
// ReactDOM.render(React.createElement(PieChart), domContainer);
