import React, { useEffect, useState } from 'react';
import { Table, message } from 'antd';
import { Stock } from '@ant-design/charts';
import styles from './index.less';


export default () => {
  const [spinning, setSpinning] = useState(false);
  const [dataSource, setDataSource] = useState([]);

  async function getPredictCoins() {
    let params = { 
      method: 'POST',
      headers: {
        Accept: 'application/json'
      }
    };
    let response = await fetch('/api/predict/ascend', params);
    let data = await response.json();
    if (data.status) {
      setDataSource(data.data);
    } else {
      message.error('获取数据失败');
    }
  }

  useEffect(() => {
    (async () => {
      setSpinning(true);
      await getPredictCoins();
      setSpinning(false);
    })();
  }, []);

  const columns = [
    {
      title: '排名',
      dataIndex: 'rank',
      key: 'rank',
      width: '4%',
    },
    {
      title: '币种',
      dataIndex: 'coin',
      key: 'coin',
      width: '4%',
    },
    {
      title: '初始价格',
      dataIndex: 'start_price',
      key: 'start_price',
      width: '4%',
    },
    {
      title: '当前价格',
      dataIndex: 'end_price',
      key: 'end_price',
      width: '4%',
    },
    {
      title: '涨幅',
      dataIndex: 'rate',
      key: 'rate',
      width: '4%',
    },
    {
      title: '1分钟k线',
      dataIndex: 'one_minute_kline',
      key: 'one_minute_kline',
      width: '40%',
      render: klines => {
        let config = {
          height: 200,
          data: klines,
          xField: 'id',
          yField: ['open', 'close', 'high', 'low'],
        };
        return (
          <Stock {...config} />
        )
      }
    },
    {
      title: '5分钟k线',
      dataIndex: 'five_minute_kline',
      key: 'five_minute_kline',
      width: '40%',
      render: klines => {
        let config = {
          height: 200,
          colorField: 'type',
          color: ['#2ca02c', '#d62728'],
          data: klines,
          xField: 'id',
          yField: ['open', 'close', 'high', 'low'],
        };
        return (
          <Stock {...config} />
        )
      }
    },
  ];

  return (
    <div className={styles.container}>
      <Table loading={spinning} dataSource={dataSource} columns={columns} pagination={{defaultPageSize: 20}} />
    </div>
  );
}
