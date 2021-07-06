<template>
    <input  class="md:text-center w-25 h-9 flex items-center justify-center bg-gray-100 rounded-lg" name="size" type="text" checked v-model="ticker">
    <button 
        class="w-1/2 bg-black flex items-center justify-center rounded-md border border-gray-300" type="button"
        @click="onSearch"
        >
            click search
        </button>
        {{ticker}}
        <div v-if="data">
            <Result :data={data}></Result>
        </div>
</template>

<script>

import axios from 'axios';
import Result from './Result.vue';

export default {
    name: 'Search',
    components: Result,
    data() {
        return {
            ticker: '',
            data: null
        }
    },
    methods: {
        onSearch() {
            const timestamp = +new Date()
            const url = '/api/stocks/getData/?name='+this.ticker+'&benchmark=1&period=3&break='+timestamp
            axios.get(url)
            .then((res)=>{
                console.log(res);
                this.data = res.data;
            })
            .then((error)=>{
                console.log(error);
            })
        }
    }
}

</script>