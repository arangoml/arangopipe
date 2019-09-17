import React from 'react';
import { Table } from 'antd';

const capitalizeFLetter = (str) => {
    return str[0].toUpperCase() +  
            str.slice(1); 
  }

const MetaSearchTable = (props) => {
  const unallowedColumns = ['_id', '_key', '_rev', 'key']
  const columns = []

  if((props.data || []).length > 0) {

    columns.push(
    {
      title: 'No',
      key: 'no',
      render: (text, record, index) => props.data.indexOf(record) + 1,
    })

    Object.entries(props.data?props.data[0]:{}).forEach(([key, value]) => {
      if(!unallowedColumns.includes(key)) {
        let newColumn = {
          key: key,
          title: capitalizeFLetter(key),
          dataIndex: key,
          sorter: (a, b) => {
            if(typeof(a[key]) == 'string')
              return a[key].localeCompare(b[key])
            else return a[key] - b[key]
          }
        }

        columns.push(newColumn)
      }
      
    });
  }

  let data = (props.data || []).map(d => {
      d.key = d['_key']
      return d
    })

  return (<Table columns={columns} 
           dataSource={data} 
           onChange={this.handleChange} 
           bordered={true}
           scroll={{x:true}}/>)
}


export default MetaSearchTable;