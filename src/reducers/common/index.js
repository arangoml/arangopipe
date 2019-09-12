
import { COMMON } from '../type'

const initState = {
  is_loading: false
}


const CommonReducer = (state = initState, action) => {
  const { type } = action
  
  switch(type){

    case COMMON.START_LOADING:
      return {
        ...state,
        is_loading: true,
      }
      
    case COMMON.END_LOADING:
      return {
        ...state,
        is_loading: false,
      }
    
    default:
        return state
  }
}

export default CommonReducer