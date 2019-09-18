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

      return dispatch({ type: USER.SIGNED_IN, payload: res.data.username })
    }).catch(err => {
      message.error('Wrong ID or Password!');
      throw err
    })
  }
}


export const currentUser = () => {
  return (dispatch) => {
    let data = {
      method: 'GET',
      url: '_admin/aardvark/whoAmI?_='+Date.now()
    }
    return AUTHAPI(data).then(res => {
      console.log('success')
      return dispatch({ type: USER.SIGNED_IN, payload: res.data.user })
    }).catch(err => {
      console.log(err)
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