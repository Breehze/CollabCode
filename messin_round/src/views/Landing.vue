<script setup>
    import {ref} from 'vue'
    import axios from 'axios'
    import CodeEditor from '../components/CodeEditorContent.vue'
    import WavesBot from '../components/WavesBot.vue'
    import CircledButton from '../components/CircledButton.vue'
    
    const generatedCollabUrl = ref()
    axios.get('http://127.0.0.1:8000/generate_collab').then((response) => {
        generatedCollabUrl.value = response.data
    })
 
    const redirectToCollab = () =>{
        window.location.href =  `/collab?col_id=${generatedCollabUrl.value}` 
    }
    
</script>

<template>
    <div class="w-full h-screen bg-io_dark flex relative justify-center">
        <div class="flex-col items-center m-3 z-10">
            <div>
                <h1 class="text-3xl text-io_light  font-semibold animate-fade-right ">Welcome</h1>
                <h1 class="text-3xl text-io_light  mt-1 font-semibold animate-fade-right animate-delay-150">On </h1>
                <h1 class="text-3xl text-io_light  mt-1 mb-2 font-semibold animate-fade-right animate-delay-300">Io.</h1>
            </div>
            <CodeEditor class="animate-fade-up animate-delay-700"></CodeEditor>
            <div class=" text-io_light animate animate-fade-up animate-delay-700">
                <h1 class="text-2xl">Your collab is ready!</h1>
                <h1 class = "text-xl">Here is your link</h1>
                <h1 class="border-2 border-io_mid_light p-1 mt-2 rounded-lg text-xs">http://127.0.0.1:8000/collab?col_id={{generatedCollabUrl}}</h1>
            </div>
            <CircledButton @bClick="redirectToCollab" class="mt-9 animate-fade-up animate-delay-700"></CircledButton> 
        </div>
        <WavesBot class="z-0"></WavesBot>
    </div>
</template>
