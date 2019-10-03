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

export const getGraphData = (query) => {
  return (dispatch) => {
    let apis = []

    apis = query.map(q => {
      if(q !== ''){
        return {
          method: 'POST',
          url: '_api/cursor',
          data: { "query" : q}
        }
      }
    })


    Promise.all([apis.map(api => AUTHAPI(api))]).then(async res => {
        let data = []
      
        // res[0].map(d => {
        for (var index = 0; index < res[0].length; index += 1) {
          await res[0][index].then(r => {
            data.push(r.data.result)
          })
        }
        // })

        return dispatch({ type: DOCUMENT.GRAPH, payload: data })
    })
  }
}


//Get Project Names
export const getProjectName = (query) => {
  return (dispatch) => {
    if(query !== ''){
      let data = {
        method: 'POST',
        url: '_api/cursor',
        data: { "query" : query}
      }

      return AUTHAPI(data).then(res => {
        return dispatch({ type: DOCUMENT.PROJECT_NAME, payload: res.data.result })
      }).catch(err => {
        throw err
      })
    }
  }
}


//Get Assets Count
export const getAssetsCount = (query) => {
    let apis = []

    apis = query.map(q => {
      if(q !== ''){
        return {
          method: 'POST',
          url: '_api/cursor',
          data: { "query" : q}
        }
      }
    })


    return Promise.all([apis.map(api => AUTHAPI(api))]).then(async res => {
        let data = []
      
        for (var index = 0; index < res[0].length; index += 1) {
          await res[0][index].then(r => {
            data.push(r.data.result)
          })
        }

        return data
    })
}

