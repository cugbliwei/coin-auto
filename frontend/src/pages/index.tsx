import React, { useEffect, useState } from 'react';
import { Table } from 'antd';
import { Stock } from '@ant-design/charts';
import styles from './index.less';


export default () => {
  const [spinning, setSpinning] = useState(false);

  async function getPredictCoins() {
    let params = { 
      method: 'POST',
      headers: {
        Accept: 'application/json'
      }
    };
    let response = await fetch('/coin/predict/ascend', params);
    let data = await response.json();
  }

  useEffect(() => {
    (async () => {
      setSpinning(true);
      await getPredictCoins();
      setSpinning(false);
    })();
  }, []);

  const sleep = (ms: number) => {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  const dataSource = [
    {
      key: '1',
      coin_name: '胡彦斌',
      start_price: 32,
      end_price: 32,
      rate: 0.1,
      one_minute_kline: [],
    },
    {
      key: '2',
      coin_name: '胡彦祖',
      start_price: 42,
      end_price: 32,
      rate: 0.1,
    },
  ];
  
  const columns = [
    {
      title: '姓名',
      dataIndex: 'coin_name',
      key: 'coin_name',
    },
    {
      title: '初始价格',
      dataIndex: 'start_price',
      key: 'start_price',
    },
    {
      title: '当前价格',
      dataIndex: 'end_price',
      key: 'end_price',
    },
    {
      title: '涨幅',
      dataIndex: 'rate',
      key: 'rate',
    },
    {
      title: '1分钟k线',
      dataIndex: 'one_minute_kline',
      key: 'one_minute_kline',
      render: klines => {
        let config = {
          width: 400,
          height: 500,
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
      <Table loading={spinning} dataSource={dataSource} columns={columns} />
    </div>
  );
}
