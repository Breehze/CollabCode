<script setup>
    import {ref} from 'vue'
    import axios from 'axios'  

    const codeRunOutput = ref()
    const props = defineProps(['collabId']) 
    
    const runCode = (collabId) => {
        axios.post(`http://127.0.0.1:8000/run/${props.collabId}`).then((response) =>{
            codeRunOutput.value = response.data
        })
    }

</script>

<template>
    <div class=" flex  items-center  w-11/12 h-72">
        <div class=" h-full flex flex-col items-center rounded-lg border-io_mid_light border-2 w-1/5">
            <button @click="runCode(props.collabId)" class="mt-2 border-2 w-2/3 border-io_mid_light text-io_mid_light rounded-md p-1 ">Run</button>
            <button class="mt-2 border-2 border-io_mid_light text-io_mid_light w-2/3 rounded-md p-1">py</button>
        </div>
        <div class="w-4/5 flex justify-end  h-full"> 
            <div class="h-full w-11/12 bg-transparent border-io_mid_light border-2 outline-none overflow-auto rounded-lg p-1 "> 
                <pre class="whitespace-pre-wrap text-xs text-io_light ">{{codeRunOutput}}</pre>  
            </div> 
        </div>
           
    </div>
</template>
