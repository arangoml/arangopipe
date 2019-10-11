import React from 'react';
import { Table } from 'antd';

const capitalizeFLetter = (str) => {
    return str[0].toUpperCase() +  
            str.slice(1); 
  }


const QueryResultTable = (props) => {
  const unallowedColumns = ['key']
  const columns = []

  //Get table headers from keys
  if((props.data || []).length > 0) {

    Object.entries(props.data?props.data[0]:{}).forEach(([key, value]) => {
      if(!unallowedColumns.includes(key)) {
        let newColumn = {
          key: key,
          title: capitalizeFLetter(key),
          dataIndex: key,
          maxWidth: 100,
          sorter: (a, b) => {
            if(typeof(a[key]) == 'string')
              return a[key].localeCompare(b[key])
            else return a[key] - b[key]
          },
          render: (text, record) => {
            if(typeof(record[key]) === 'object')
              return JSON.stringify(record[key])
            else if(typeof(record[key]) === 'array')
              return record[key].toString()
            else return record[key]
          }
        }

        columns.push(newColumn)
      }
      
    });
  }

  let data = (props.data || []).map((d, index) => {
      if(typeof(d) === 'object' )
        d.key = index

      return d
    })

  return (<div>
            <Table columns={columns} 
             dataSource={data} 
             bordered={true}
             scroll={{x:true}}
             pagination={{ pageSize: 5 }} />

          </div>)
}


export default QueryResultTable;