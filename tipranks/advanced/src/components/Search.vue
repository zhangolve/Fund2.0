<template>
        <a-row type="flex" justify="center">
            <a-col :xs="20" :lg="12">
                <a-input-search
                    v-model:value="ticker"
                    placeholder="input search ticker"
                    enter-button="Search"
                    size="large"
                    @search="onSearch"
                />   
            </a-col>
        </a-row>
        <div v-if="data && !loading">
            <Result :data="data"></Result>
        </div>
        <div v-if="loading">
            <a-spin tip="Loading...">
                <div class="spin-content">
                    正在加载中
                </div>
            </a-spin>
        </div>
</template>
<script>

import axios from 'axios';
import Result from './Result.vue';

export default {
    name: 'Search',
    components: {
        Result
    },
    data() {
        return {
            ticker: '',
            data: false,
            loading: false
        }
    },
    methods: {
        onSearch() {
            const timestamp = +new Date()
            this.loading=true;
            const url = '/api/stocks/getData/?name='+this.ticker+'&benchmark=1&period=3&break='+timestamp
            axios.get(url)
            .then((res)=>{
                console.log(res);
                this.data = res.data;
                this.loading=false;
            })
            .then((error)=>{
                this.loading=false;
                console.log(error);
            })
        }
    }
}

</script>