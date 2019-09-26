import { QUERY } from '../../reducers/type'
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

//Execute Query
export const executeQuery = (query) => {
  return (dispatch) => {
    let data = {
      method: 'POST',
      url: '_api/cursor',
      data: ({
        id: "currentFrontendQuery",
        options: {profile: true},
        query: query
      })
    }

    return AUTHAPI(data).then(res => {
        if(!res.data.error){
          return dispatch({ type: QUERY.QUERY_RESULT, payload: res.data })
        }
      }).catch(err => {
        return dispatch({ type: QUERY.ERROR, payload: err.data.errorMessage })
      })
  }
}

//Explain Query
export const explainQuery = (query) => {
  return (dispatch) => {
    let data = {
      method: 'POST',
      url: '_admin/aardvark/query/explain',
      data: ({
        id: "currentFrontendQuery",
        query: query
      })
    }

    return AUTHAPI(data).then(res => {
        if(!res.data.error){
          return dispatch({ type: QUERY.QUERY_EXPLAIN, payload: res.data.msg })
        }
      }).catch(err => {
        return dispatch({ type: QUERY.ERROR, payload: err.data.errorMessage })
      })
  }
}

