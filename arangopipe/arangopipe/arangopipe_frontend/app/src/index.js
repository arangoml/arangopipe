import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import configureStore, { history } from './store/configureStore';
import { Router, Route, Switch } from 'react-router-dom'

import App from './containers/App/App';
import Login from './containers/Login/Login';

import 'antd/dist/antd.css';

const target = document.querySelector('#root');

render(
  <Provider store={configureStore}>
    <Router history={history}>
    	<Switch>
    		<Route path="/login" component={Login}/>
	        <Route path="/" component={App}/>
	    </Switch>
    </Router>
  </Provider>,
  target
);