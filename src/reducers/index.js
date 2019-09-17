import { combineReducers } from 'redux'

import AuthReducer from './auth'
import DocumentReducer from './document'

const rootReducer = combineReducers({
	auth: AuthReducer,
	document: DocumentReducer
})

export default rootReducer