
import { DOCUMENT, GRAPH } from '../type'


const initState = {}

const DocumentReducer = (state = initState, action) => {
  const { type, payload} = action
  
  switch(type){

    case DOCUMENT.DOC_ALL:
      return {
        ...state,
        documents: payload
      }

    case DOCUMENT.GRAPH:
      return {
        ...state,
        graph: payload
      }

    default:
        return state
  }
}

export default DocumentReducer