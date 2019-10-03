import { USER } from '../../reducers/type'
import API from '../API'
import AUTHAPI from '../AUTHAPI'
import { message } from 'antd'

export const signin = (obj) => {
  return (dispatch) => {
    let data = {
      method: 'POST',
      url: '_open/auth',
      data: JSON.stringify(obj)
    }
    return API(data).then(res => {
      localStorage.setItem('token', res.data.jwt);

      let get_dbs = {
        method: 'GET',
        url: '_api/database/user?_='+Date.now()
      }

      const username = res.data.user

      return AUTHAPI(get_dbs).then(res => {
        return dispatch({ 
          type: USER.SIGNED_IN, 
          payload: { name: username, isAdmin: res.data.result.includes('_system') }})
      })

    }).catch(err => {
      message.error('Wrong ID or Password!');
      throw err
    })
  }
}


export const currentUser = () => {
  return (dispatch) => {
    let get_token = {
      method: 'GET',
      url: '_admin/aardvark/whoAmI?_='+Date.now()
    }

    return AUTHAPI(get_token).then(res => {
      
      let get_dbs = {
        method: 'GET',
        url: '_api/database/user?_='+Date.now()
      }

      const username = res.data.user

      return AUTHAPI(get_dbs).then(res => {
        return dispatch({ 
          type: USER.SIGNED_IN, 
          payload: { name: username, isAdmin: res.data.result.includes('_system') }})
      })
      
    }).catch(err => {
      localStorage.removeItem('token');
      return dispatch({ type: USER.SIGNED_OUT })
    })
  }
}



export const signout = () => {
  return (dispatch) => {
    localStorage.removeItem('token');
    return dispatch({ type: USER.SIGNED_OUT })
  }
}