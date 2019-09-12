
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

    case DOCUMENT.DB_CLEARED:
      return {
        ...state
      }

    case DOCUMENT.DETAIL_INFO:
      return {
        ...state,
        detail_info: payload
      }

    case DOCUMENT.DOC_DELETED:
      state.documents = state.documents.filter((e) => {
        return e.id !== payload.doc_id
      })

      return {
        ...state
      }

    default:
        return state
  }
}

export default DocumentReducer