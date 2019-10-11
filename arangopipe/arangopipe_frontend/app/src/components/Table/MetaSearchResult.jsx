import React from 'react';
import { Table, Button } from 'antd';

const capitalizeFLetter = (str) => {
    return str[0].toUpperCase() +  
            str.slice(1); 
  }


const MetaSearchTable = (props) => {
  const unallowedColumns = ['_id', '_key', '_rev', 'key']
  const alternativeColumns = {'run_id': 'Experiment ID', 'generated_by':'GeneratedBy'}
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
          title: alternativeColumns[key]?alternativeColumns[key]:capitalizeFLetter(key),
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

    if(props.filter !== null) {
      columns.push(
      {
        title: 'Graph',
        key: 'graph',
        align: 'center',
        render: (text, record, index) => {
          return(
          <span>
            <Button type="primary" shape="circle" icon="line-chart" onClick={() => props.showGraph(record['_key'])}/>
          </span>
        )},
      })
    }
  }

  let data = (props.data || []).map(d => {
      d.key = d['_key']
      return d
    })

  return (<div>
            <Table columns={columns} 
             dataSource={data} 
             bordered={true}
             scroll={{x:true}}
             pagination={{ pageSize: 5 }}/>

          </div>)
}


export default MetaSearchTable;