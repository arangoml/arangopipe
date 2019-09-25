
import { QUERY, GRAPH } from '../type'


const initState = {default_query: [], saved_query: []}

const QueryReducer = (state = initState, action) => {
  const { type, payload} = action
  
  switch(type){

    case QUERY.QUERY_ALL:

      state.default_query = payload.dquery
      state.saved_query = payload.squery

      return {
        ...state
      }

    case QUERY.SAVED_QUERY:
      state.saved_query = payload || []

      return { ...state }

    default:
        return state
  }
}

export default QueryReducer