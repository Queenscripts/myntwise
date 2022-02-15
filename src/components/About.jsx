import React from "react";

export default function About() {
  return (
    <div class="flex flex-col p-4" style={{height:"100vh"}}>
      <h2 class="text-4xl font-medium leading-tight mt-0 mb-2 text-teal-500">
        About
      </h2>
      <p>
        Build budgets, track transactions, and know where to purchase goods and
        services based on your financial availability and personal finance
        goals.
      </p>
      <img src="static/img/arabica-finance.png" style={{position: "absolute",float: "left",top: "300px",right: "220px",zIndex: -1,opacity: .3}}/>

    </div>
  );
}
