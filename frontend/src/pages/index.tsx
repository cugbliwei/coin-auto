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
    let response = await fetch('/coin/predict/ascend', params);
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

  const sleep = (ms: number) => {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  const columns = [
    {
      title: '币种',
      dataIndex: 'coin',
      key: 'coin',
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
      // dataIndex: 'one_minute_kline',
      // key: 'one_minute_kline',
      dataIndex: 'klines',
      key: 'klines',
      render: klines => {
        let config = {
          width: 200,
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
  ];

  return (
    <div className={styles.container}>
      <Table loading={spinning} dataSource={dataSource} columns={columns} />
    </div>
  );
}
