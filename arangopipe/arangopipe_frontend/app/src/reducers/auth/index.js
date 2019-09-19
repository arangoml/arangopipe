
import { USER } from '../type'


const initState = { is_authed: localStorage.getItem('token') ? true : false, user: '' };


const AuthReducer = (state = initState, action) => {
  const { type, payload} = action
  
  switch(type){

    case USER.SIGNED_IN:
      state.is_authed  = true;
      state.user = payload;

      return {
        ...state,
      }

    case USER.SIGNED_OUT:
      state.is_authed = false;

      return {
        ...state,
        
      }

    default:
        return state
  }
}

export default AuthReducer