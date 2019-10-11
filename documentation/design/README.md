
# Overview
The Arangopipe UI is a single page application for its user community. <br>
The Arangopipe user community consists of the following groups:<br>

1. Arangopipe Administrators<br>
2. Arangopipe Users<br>

Arangopipe is a tool for managing metadata for machine learning projects. 
Projects and project artifacts are tracked in the Arangopipe datastore. 
Project data needs access control. 
It is tothis end that we have the above categories of users. 

Arangopipe Administrators can perform the following actions:<br>

1. Adding a project to Arangopipe<br>
2. Registering a deployment with Arangopipe. After a deploymentis registered, serving performance on the deployment can be logged and tracked.<br>
3. Adding a user to Arangopipe<br>

For the MVP, there is no division of user privileges. <br>
However, in the future, assigning privileges to users to control the actions is foreseen.

## Technologies Used:
#### Frameworks used
-   [React](https://github.com/facebook/react)
-   [Redux](https://github.com/rackt/redux)
-   [React Router](https://github.com/rackt/react-router)
-   [Ant Design](https://github.com/ant-design/ant-design)
#### Specific libraray
-   [React Ace](https://www.npmjs.com/package/react-ace)
Ace is an embeddable code editor written in JavaScript. It matches the features and performance of native editors such as Sublime, Vim and TextMate. It can be easily embedded in any web page and JavaScript application. Ace is maintained as the primary editor for [Cloud9 IDE](https://c9.io/) and is the successor of the Mozilla Skywriter (Bespin) project.

-    [GraphvizOnline](https://github.com/dreampuf/GraphvizOnline)
 GraphvizOnline could let you debug the graphviz languages online.
 Tracing lineage is frequently required from machine learning
meta-data. For a given deployment, we need to be able to trace
the computational artifacts related to it. Using this graphviz tool, you can get graph representation trace.

## Project Structure

### Basic Directory
```
arangopipe/arangopipe_frontend/app
```
### Root Component
```
arangopipe/arangopipe_frontend/app/src/index.js
```
```
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
```
### Main Pages and Children Components
#### -  Login Page
````
arangopipe/arangopipe_frontend/app/src/containers/Login/Login.jsx
````

#### - Meta Data Search Page
In this page, users can search meta data with name, tag and deployment tag. 
After search, users can see the graph representation of trace.
````
arangopipe/arangopipe_frontend/app/src/containers/Home/Home.jsx
````
````
// Search Bar Component
   arangopipe/arangopipe_frontend/app/src/components/Form/MetaSearchForm.jsx

// Search Result Component
   arangopipe/arangopipe_frontend/app/src/components/Table/MetaSearchResult.jsx

// Project Summary Component
   arangopipe/arangopipe_frontend/app/src/components/SummaryTree/SummaryTree.jsx

// Graph View Component
   arangopipe/arangopipe_frontend/app/src/components/Modal/TreeGraph.jsx

````





#### -  Adhoc Query Page
In this page, users can run AQL queries and get the result from the DB directly. Query page contains some sample queries and common query templates related to arangopipe.
Users can add their queries and update or delete them. 
````
arangopipe/arangopipe_frontend/app/src/containers/Query/Query.jsx
````
````
- Query Result Component
  arangopipe_frontend/app/src/components/Table/QueryResult.jsx

- Custom AQL Mode for ACE Editor
   arangopipe_frontend/app/src/containers/Query/AqlMode.jsx
   
  # Ace Editor Usage
    import brace from 'brace';
    import AceEditor from 'react-ace';
    import  AqlMode  from  './AqlMode'
	
	...
	componentDidMount() {
		const aqlMode = new AqlMode();
		this.refs.aceEditor.editor.getSession().setMode(aqlMode);
		this.refs.aceEditor.editor.getSession().setUseWrapMode(true);
	}
	
    render() {
	    ...
	    <AceEditor
			ref="aceEditor"
			mode="text"
			width = '100%'
			height = '300px'
			theme="xcode"
			fontSize = {16}
			name="AQL_EDITOR"
			value={this.state.currentQuery}
			editorProps={{
				$blockScrolling: true
			}}
		/>
    }
````
### Reducers
````
arangopipe/arangopipe_frontend/app/src/reducers/index.js
````
````
const rootReducer = combineReducers({
	auth: AuthReducer,
	document: DocumentReducer,
	query: QueryReducer
})
````
### API
````
arangopipe/arangopipe_frontend/app/src/actions/API.js
arangopipe/arangopipe_frontend/app/src/actions/AUTHAPI.js
````
Project is using JWT authentication for interacting with ArangoDB. Below code shows how to add token to request header. 
````
// JWT Authentication.

AUTHAPI.interceptors.request.use(
	config => {
		config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`
		return config
		},
	error => {
		return Promise.reject(error.response)
	},
)
````
#### API Configuration
##### To set the DB name and API root url,   please reference this file.
````
arangopipe/arangopipe_frontend/app/src/constants/utils.js
````

 ##### Example
````
export const DATABASE = 'arangopipe'
export const API_ROOT_URL = "http://localhost:6529/_db/arangopipe/";
````

## Getting Started
### Running with Docker Compose
````
// Install Docker
apt update
apt-get install docker -y
apt-get install docker.io -y
apt-get install docker-compose -y

// Start Project
docker-compose up

// If you want to start containers in background (as a daemon), add the `-d` flag
docker-compose up -d
````


### Running with Scripts

In the  `app`  directory , you can run:

### `npm start`

Runs the app in the development mode.  
Open  [http://localhost:3000](http://localhost:3000/)  to view it in the browser.

### `npm test`

Launches the test runner in the interactive watch mode.  
See the section about  [running tests](https://github.com/arangoml/arangopipe/tree/test/arangopipe/arangopipe_frontend#running-tests)  for more information.

### `npm run build`

Builds the app for production to the  `build`  folder.  
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.  
Your app is ready to be deployed!

See the section about  [deployment](https://github.com/arangoml/arangopipe/tree/test/arangopipe/arangopipe_frontend#deployment)  for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you  `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can  `eject`  at any time. This command will remove the single build dependency from your project.









  
