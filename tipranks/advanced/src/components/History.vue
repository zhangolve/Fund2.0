<template>
  <a-table :dataSource="dataSource" :columns="columns" />
</template>
<script>
  export default {
    props: ['dataSource'],
    setup() {
      return {
        columns: [
          {
            title: '日期',
            dataIndex: 'date',
            key: 'name',
          },
          {
            title: '评价人数',
            dataIndex: 'consensus',
            key: 'consensus',
          },
          {
            title: '目标价',
            dataIndex: 'priceTarget',
            key: 'priceTarget',
          },
        ],
      };
    },
  };
</script>