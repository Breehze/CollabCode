<script setup>
    import CodeField from '../components/CodeField.vue'
    import CodeOutput from '../components/CodeOutput.vue'
    import {useRoute,useRouter} from 'vue-router'
    import {ref,onMounted,onUnmounted} from 'vue'

    const route = useRoute()
    const router = useRouter()

    const ws = ref(null)

    onMounted(() => {
        ws.value = new WebSocket(`ws://127.0.0.1:8000/collab/${route.query["col_id"]}`) 
        ws.onclose = () =>{
            alert("Oops something went wrong! You have been disconnected")
        }
    })

    onUnmounted(()=> {
        if(ws.value){
            ws.value.close()
        }
    })
     

</script>

<template>
    <div  class="bg-gradient-to-br from-io_dark to-io_mid_dark flex flex-col items-center w-full h-screen" >
        <div class="w-full flex flex-col items-center sm:w-1/3">
            <CodeField class="mt-2" v-if="ws" :webSocket = "ws" ></CodeField>
            <CodeOutput :collabId = "route.query['col_id']" class="mt-8"></CodeOutput>
        </div> 
    </div>
</template>
