import { combineReducers } from 'redux'

import AuthReducer from './auth'
import DocumentReducer from './document'
import QueryReducer from './query'

const rootReducer = combineReducers({
	auth: AuthReducer,
	document: DocumentReducer,
	query: QueryReducer
})

export default rootReducer