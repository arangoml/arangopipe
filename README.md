This project is a simple boilerplate for React (v16), Redux, Router (v4), and Ant Design (UI components).

Elements of Boilerplate
1. Create React App and Ant Design without the need for npm eject
2. Add Redux for state management (see sample counter: action, reducers, store)
3. A basic Header, Content, Footer layout from Ant Design
4. React Router v4 + antd: Add breadcrumbs and connect with React Router v4 

## Ant Design

The first step (React + Ant Design) is based on the "Advanced Guides" section of the create react app with Ant Design, where we modify config-overrides to install antd on demand.
[Ant Design: Use with Create React App](https://ant.design/docs/react/use-with-create-react-app)

Instead of importing all styles of of the antd library (`@import '~antd/dist/antd.css';`) (which may cause network performance issues), we can just load the styles of the components used in our project.

Ant Design is a an out-of-box UI solution for enterprise applications used by 
* Ant Financial
* Alibaba
* Tencent
* Baidu
* Koubei
* Meituan
* Didi
* Eleme

It based on React and is minimalistic and themeable.

For the project to build, **these files must exist with exact filenames**:

* `public/index.html` is the page template;
* `src/index.js` is the JavaScript entry point.

You can delete or rename the other files.

You may create subdirectories inside `src`. For faster rebuilds, only files inside `src` are processed by Webpack.<br>
You need to **put any JS and CSS files inside `src`**, otherwise Webpack won’t see them.

Only files inside `public` can be used from `public/index.html`.<br>
Read instructions below for using assets from JavaScript and HTML.

You can, however, create more top-level directories.<br>
They will not be included in the production build so you can use them for things like documentation.

## Available Scripts

In the project directory, you can run:

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