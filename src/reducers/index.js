import { combineReducers } from 'redux'

import AuthReducer from './auth'
import CommonReducer from './common'
import DocumentReducer from './document'
import counter from './counter'

const rootReducer = combineReducers({
	auth: AuthReducer,
	common: CommonReducer,
	counter: counter,
	document: DocumentReducer
})

export default rootReducer