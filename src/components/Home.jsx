import React from "react";
import Advice from "./Advice.jsx";

export default function Home() {
    return(
        <div class="flex flex-col p-4">
            <h2 className="text-4xl font-medium leading-tight mt-0 mb-2 text-teal-500">
                View Deals! 
            </h2>
            <Advice />
        </div>
    );
}
