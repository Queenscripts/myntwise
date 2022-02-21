
import React from 'react';
import ReactDOM from 'react-dom';
import { Routes, Route, IndexRoute  } from 'react-router'

import {
    About, 
    Advice, 
    Budget,
    Footer, 
    Menu,
    Login,
    Home, 
    Nav
} from './components/index.js'; 
import {BrowserRouter} from 'react-router-dom';
import SignUp from './components/SignUp.jsx';

function App(){
    return(
        <>
        <BrowserRouter>
            <Nav
                user={user}
            />
            <Routes>
                {/* <IndexRoute component = {Home} /> */}
                <Route path="/" element={<Home/>} title={"Home"}></Route>
                <Route exact path="/about" element={<About/>}></Route>
                <Route exact path="/budgets" element={<Budget/>}></Route>
                <Route path="/dashboard"  element={<Menu/>}></Route>
                <Route exact path="/signup"  element={<SignUp/>} title="Signup"></Route>
                <Route exact path="/login"  element={<Login/>} title="Login"></Route>
            </Routes>
            <Footer/>
        </BrowserRouter>
        </>

    )
}

ReactDOM.render(<App />, document.getElementById("root"));