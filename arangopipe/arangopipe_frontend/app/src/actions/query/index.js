import { QUERY, GRAPH } from '../../reducers/type'
import AUTHAPI from '../AUTHAPI'
import moment from 'moment';
import { message } from 'antd'


//Get Default Query
export const getDefaultQuery = () => {
  return (dispatch) => {
    let default_query = {
      method: 'GET',
      url: '_admin/aardvark/js/arango/aqltemplates.json?_='+Date.now(),
    }

    let saved_query = {
      method: 'GET',
      url: '_api/user/root',
    }

    Promise.all([AUTHAPI(default_query), AUTHAPI(saved_query)]).then(([dquery, squery]) => {

        return dispatch({ 
            type: QUERY.QUERY_ALL, 
            payload: {
                dquery: dquery.data,
                squery: squery.data.extra.queries
            } 
        })
    })
  }
}

//Resave Query
export const reSaveQuery = (query) => {
  return (dispatch) => {
    let data = {
      method: 'PATCH',
      url: '_api/user/root',
      data: ({
        extra: { queries: query}
      })
    }

    return AUTHAPI(data).then(res => {
        return dispatch({ type: QUERY.SAVED_QUERY, payload: res.data.extra.queries })
      }).catch(err => {
        throw err
      })
  }
}

