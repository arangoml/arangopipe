import { DOCUMENT } from '../../reducers/type'
import AUTHAPI from '../AUTHAPI'
import moment from 'moment';
import { message } from 'antd'


//Get Collections
export const getCollections = (query) => {
  return (dispatch) => {
    if(query !== ''){
      let data = {
        method: 'POST',
        url: '_api/cursor',
        data: { "query" : query}
      }

      return AUTHAPI(data).then(res => {
        return dispatch({ type: DOCUMENT.DOC_ALL, payload: res.data.result })
      }).catch(err => {
        throw err
      })
    }
  }
}

