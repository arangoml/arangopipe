import React from 'react';
import { Table } from 'antd';

const capitalizeFLetter = (str) => {
    return str[0].toUpperCase() +  
            str.slice(1); 
  }


const QueryResultTable = (props) => {
  const unallowedColumns = ['key']
  const columns = []

  if((props.data || []).length > 0) {

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

  let data = (props.data || []).map((d, index) => {
      if(typeof(d) === 'object' )
        d.key = index
      return d
    })

  return (<div>
            <Table columns={columns} 
             dataSource={data} 
             bordered={true}
             scroll={{x:true}}/>

          </div>)
}


export default QueryResultTable;