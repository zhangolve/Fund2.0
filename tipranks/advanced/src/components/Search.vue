<template>
    <input  class="md:text-center w-25 h-9 flex items-center justify-center bg-gray-100 rounded-lg" name="size" type="text" checked v-model="ticker">
    <button 
        class="w-1/2 bg-black flex items-center justify-center rounded-md border border-gray-300" type="button"
        @click="onSearch"
        >
            click search
        </button>
        {{ticker}}
</template>

<script>

export default {
    name: 'Search',
    data() {
        return {
            ticker: '',
            test: 'abc'
        }
    },
    methods: {
        onSearch() {
            console.log(this)
            console.log(this.ticker)
            console.log(this.test)
            console.log('console');
        }
    }
}

</script>