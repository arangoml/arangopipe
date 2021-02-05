
import { QUERY } from '../type'


const initState = {default_query: [], saved_query: []}

const QueryReducer = (state = initState, action) => {
  const { type, payload} = action
  
  switch(type){

    case QUERY.QUERY_ALL:

      state.default_query = payload.dquery
      state.saved_query = payload.squery || []

      return {
        ...state
      }

    case QUERY.SAVED_QUERY:
      state.saved_query = payload || []

      return { ...state }

    case QUERY.QUERY_RESULT:
      return { ...state, ...payload }

    case QUERY.QUERY_EXPLAIN:
      return { ...state, explain: payload || null }

    case QUERY.CLEAR:
      return { ...state, explain: null, result: null }

    case QUERY.ERROR:
      return { ...state, error: payload || null }

    default:
        return state
  }
}

export default QueryReducer