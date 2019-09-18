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

### Application Techs
* React
* Redux
* Ant Design

### Backend Dependencies
* ArangoDB
* ArangoML Pipeline
* Jupyter Notebook



# Getting Started

## Docker Install

```bash
apt update
apt-get install docker -y
apt-get install docker.io -y
apt-get install docker-compose -y
```

## Run

To start the project, just run:

```bash
docker-compose up
```

If you want to start containers in background (as a daemon), add the `-d` flag:

```bash
docker-compose up -d
```
Open http://localhost:3000 to view Application in the browser.
Open http://localhost:6529 to view ArangoDB UI  in the browser.
Open http://localhost:8888 to view Jupyter notebook  in the browser.

## Stop

You can stop containers by typing `Cmd + C` on Mac or `Ctrl + C` on Windows/Linux. 

If you started the project in background, then run:

```bash
docker-compose stop
```

## Available Scripts

In the `app` directory , you can run:

### `npm start`

Runs the app in the development mode.<br>
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br>
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br>
See the section about [running tests](#running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br>
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br>
Your app is ready to be deployed!

See the section about [deployment](#deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (Webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.