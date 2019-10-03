
import { DOCUMENT } from '../type'


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

    case DOCUMENT.PROJECT_NAME:
    
      let treeData = payload.map(d => {
        return {title: d, key:d}
      })

      return {
        ...state,
        projects: treeData
      }

    default:
        return state
  }
}

export default DocumentReducer