import React from 'react';
import { Table } from 'antd';

const data = [
  {
    key: '1',
    name: 'Housing Data Featureset',
    period: '01/01/2019 to 01/31/2019',
    source: 'Pipeline Housing Features',
    dataset_soucre: 'HD_01_01_2018_to_01_31_2018',
  },
  {
    key: '2',
    name: 'Housing Data Featureset',
    period: '01/01/2019 to 01/31/2019',
    source: 'Pipeline Housing Features',
    dataset_soucre: 'London No. 1 Lake Park',
  },
  {
    key: '3',
    name: 'Housing Data Featureset',
    period: '01/01/2019 to 01/31/2019',
    source: 'Pipeline Housing Features',
    dataset_soucre: 'HD_01_01_2018_to_01_31_2018',
  },
  {
    key: '4',
    name: 'Housing Data Featureset',
    period: '01/01/2019 to 01/31/2019',
    source: 'Pipeline Portial User Features',
    dataset_soucre: 'HD_01_01_2018_to_01_31_2018',
  },
];


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
          title: key,
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