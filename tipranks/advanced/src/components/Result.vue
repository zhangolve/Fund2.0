<template>
    <div v:if="data">
        <div>
            <label>ticker</label>
            <div>{{data.ticker}}</div>
        </div>
        <div>
            <label>companyName</label>
            <div>{{data.companyName}}</div>
        </div>
    </div>
</template>

<script>
import { toRefs } from 'vue'

export default {
    name: 'Result',
    props: ['data'],
     data() {
        return {
            abc: '',
        }
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