<template>
    <div v-if="data">
     <a-row type="flex" justify="center">
            <a-col :span="12">
                <a-descriptions title="User Info" bordered>
                    <a-descriptions-item label="Ticker">{{data.ticker}}</a-descriptions-item>
                    <a-descriptions-item label="companyName">{{data.companyName}}</a-descriptions-item>
                </a-descriptions>
            </a-col>
        </a-row>
     <a-row type="flex" justify="center">
        <a-col :span="24" v-for="item in data.ptConsensus" :key="item">
                    <a-descriptions  bordered>
                    <a-descriptions-item label="target">{{item.priceTarget}}</a-descriptions-item>
                    <a-descriptions-item label="high">{{item.high}}</a-descriptions-item>
                    <a-descriptions-item label="low">{{item.low}}</a-descriptions-item>
                    </a-descriptions>
        </a-col>
        </a-row>

         <a-row type="flex" justify="center">
              
        <a-col :span="12">
            <History :dataSource="data.consensusOverTime"/>
        </a-col>
        </a-row>
    </div>
</template>

<script>
import { toRefs } from 'vue'
import History from './History.vue';
export default {
    name: 'Result',
    props: ['data'],
     data() {
        return {
            abc: '',
        }
    },
    components: {
        History
    }, 
    computed(props) {
        const { data } = toRefs(props);
        const {
            ticker,
            companyName,
            ptConsensus
        } = data;
        console.log(ticker,
            companyName,
            ptConsensus)
        return {
            ticker,
            companyName,
            ptConsensus
        };
    }
}


</script>