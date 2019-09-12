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


export const getUploadedDocuments = () => {
  return (dispatch) => {
    let data = {
      method: 'get',
      url: '_api/view',
    }

    return AUTHAPI(data).then(res => {
      res.data = res.data.map((obj, index) => {
        return {
          'key': index,
          'title': obj['file'].split('/')[obj['file'].split('/').length - 1],
          'id': obj['id'],
          'upload_date': moment(new Date(obj['uploaded_at'])).format('lll'),
          'author': obj['Uploaded_user']!=undefined?obj['Uploaded_user']: '',
          'process_date': obj['processed_date']!=null?moment(new Date(obj['processed_date'])).format('lll'):'',
        }
      })

      return dispatch({ type: DOCUMENT.DOC_ALL, payload: res.data.result })
    }).catch(err => {
      throw err
    })
  }
}


export const getDetailDocument = (doc_id) => {
  return (dispatch) => {
    const data1 = {
      method: 'get',
      url: 'api/detail/' + doc_id,
    }

    const data2 = {
      method: 'get',
      url: 'api/displacy/' + doc_id,
    }

    const data3 = {
      method: 'get',
      url: 'api/role/'
    }

    let result = {type: null, payload: {data: null, html: null, roles: []}}

    return AUTHAPI(data1).then(res => {
      result.type = DOCUMENT.DETAIL_INFO;
      result.payload.data = res.data[0]

      return AUTHAPI(data2).then(res => {
        result.payload.html = res.data

        return AUTHAPI(data3).then(res => {
          result.payload.roles = res.data
          return dispatch(result)
        }).catch(err => {
          throw err
        })
        return dispatch(result)
      }).catch(err => {
        throw err
      })
    }).catch(err => {
      throw err
    })
  }
}


export const saveToCSV = () => {  
  return (dispatch) => {

      var element = document.createElement('a');
      element.setAttribute('href', 'http://localhost:8001/UploadMulti/csv/');
      element.setAttribute('download', '');
      element.style.display = 'none';
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    }
}

export const clearDB = () => {
  return (dispatch) => {
    let data = {
      method: 'GET',
      url: 'api/clear/'
    }

    return AUTHAPI(data).then(res => {
      message.success('Database is cleared successfully!');
      return dispatch({ type: DOCUMENT.DOC_ALL, payload: []})
    }).catch(err => {
      throw err
    })
  }
}


export const deleteDocument = (doc_id) => {
  return (dispatch) => {
    let data = {
      method: 'GET',
      url: 'api/clear/'+doc_id
    }

    return AUTHAPI(data).then(res => {
      message.success('Document is deleted successfully!');
      return dispatch({ type: DOCUMENT.DOC_DELETED, payload: {'doc_id': doc_id}})
    }).catch(err => {
      throw err
    })
  }
}

export const processDocument = () => {
  return (dispatch) => {
    let data = {
      method: 'GET',
      url: 'api/process/'
    }

    return AUTHAPI(data).then(res => {
      message.success('Documents are processed successfully!');
      return dispatch({ type: DOCUMENT.PROCESSED })
    }).catch(err => {
       message.error('Sorry! Document processing failed');
      return dispatch({ type: DOCUMENT.PROCESSED })
    })
  }
}

export const updateDetailInfo = (values) => {
  return (dispatch) => {

    var fd = new FormData();
    fd.append('_401k', values['401k'])
    fd.append('Document_Name', values['document'])
    fd.append('Address_of_Company', values['com_address'])
    fd.append('Address_of_Employee', values['emp_address'])
    fd.append('Date_of_Agreement', values['agreement'].format('YYYY-MM-DD'))
    fd.append('Bonus', values['bonus'])
    fd.append('Company_Name', values['company'])
    fd.append('Employee_Name', values['employee'])
    fd.append('End_Date', values['end'].format('YYYY-MM-DD'))
    fd.append('Health_Insurance', values['health'])
    fd.append('Non_Monetary_Benefits', values['monetary'])
    fd.append('Notice_Period', values['notice'])
    fd.append('Other_Compensation', values['other'])
    fd.append('Roles', values['role'])
    fd.append('Base_Salary', values['salary'])
    fd.append('Start_Date', values['start'].format('YYYY-MM-DD'))
    fd.append('Stock', values['stock'])
    fd.append('Supervisor_Information', values['supervisor'])
    fd.append('Vacation', values['vacation'])
    fd.append('At_will', values['will'])

    let data = {
      method: 'POST',
      url: 'api/form_post/',
      contentType: false,
      processData: false,
      data: fd
    }

    return AUTHAPI(data).then(res => {
      message.success('Documents are updated successfully!');
      // message.success('Document is deleted successfully!');
      // return dispatch({ type: DOCUMENT.DOC_DELETED, payload: {'doc_id': doc_id}})
    }).catch(err => {
      throw err
    })
  }
}
